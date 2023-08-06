#!/usr/bin/env python3

import subprocess
import sys
import os
import select
import pty
import re

# GCC color formatting (non-matched group, optional)
R_FMT = r'(?:\x1b\[\d*;?\d*m\x1b\[K)?'

# Match file msg (text for hyperlink), file path, file location (row:column) and error msg. from GCC message
re_gcc_file_loc = [
    re.compile(r'^(?P<f_msg>' + R_FMT + r'(?P<f_path>.*?):(?P<f_loc>\d+:?\d*):' + R_FMT + r')(?P<err_msg>\s?' + R_FMT + msg + r'.+$)')
    for msg in (
        'error',
        'warning',
        'note',
        'undefined reference',
    )
]

# Create shell hyperlink
# https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
def shell_hyperlink(url, txt):
    result = '\x1b]8;;'
    result += url
    result += '\x1b\\'
    result += txt
    result += '\x1b]8;;\x1b\\'
    return result

# Display hyperlink for VSCode URL handler
# https://code.visualstudio.com/docs/editor/command-line#_opening-vs-code-with-urls
def vscode_link_msg(m):
    f_desc = m['f_path'] + ':' + m['f_loc']
    vsc_url = f'vscode://file/{f_desc}'
    l = shell_hyperlink(vsc_url, m['f_msg'])
    return l + m['err_msg'] + '\n'

def main():
    args = ['make'] + sys.argv[1:]

    # based on https://gist.github.com/hayd/4f46a68fc697ba8888a7b517a414583e
    mo, so = pty.openpty() # provide tty to enable line-buffering
    me, se = pty.openpty()
    mi, si = pty.openpty()
    fdmap = {
        mo: {
            'file': sys.stdout,
            'buf': b'',
        },
        me:  {
            'file': sys.stderr,
            'buf': b'',
        },
        mi: None
    }

    process = subprocess.Popen(
        args,
        bufsize=1, stdin=si, stdout=so, stderr=se,
        close_fds=True
    )

    timeout = .01
    while True:
        ready, _, _ = select.select([mo, me], [], [], timeout)
        if ready:
            for fd in ready:
                data = os.read(fd, 512)
                if not data:
                    break

                # Process line-wise
                buf_str = fdmap[fd]['buf'] + data
                while b'\n' in buf_str:
                    k = buf_str.index(b'\n')+1
                    line, buf_str = buf_str[:k], buf_str[k:]
                    line = line.decode('utf-8')

                    # Match regexes
                    m = list(filter(None, [r.match(line) for r in re_gcc_file_loc]))
                    if len(m):
                        line = vscode_link_msg(m[0].groupdict())
                    fdmap[fd]['file'].write(line)

                fdmap[fd]['buf'] = buf_str

        elif process.poll() is not None:  # select timed-out
            break  # p exited

    for fd in [si, so, se, mi, mo, me]:
        os.close(fd)  # can't do it sooner: it leads to errno.EIO error

    process.wait()
    sys.exit(process.returncode)

if __name__ == '__main__':
    main()
