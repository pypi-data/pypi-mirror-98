# vmake

This is a small wrapper for `make`, which captures `gcc` output and transforms errors/warnings to hyperlinks that open the Visual Studio Code editor for the referenced files at the respective locations.

It takes advantage of [OSC8 escape sequence for hyperlinks](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda) and the [VSCode URL handler](https://code.visualstudio.com/docs/editor/command-line#_opening-vs-code-with-urls).

## Why not just use the VSCode terminal?

The VSCode terminal is [bound to a VSCode instance](https://github.com/microsoft/vscode/issues/10121), and VSCode doesn't support multi-monitor operation - so it is not possible to edit source files on one monitor and run the build on a second monitor with direct links from compiler messages to the editor.

## TODOs / caveats

`tmux` doesn't support hyperlinks and requires special escape sequences to "passthrough" such things to the terminal emulator.

Unfortunately, the "passthrough" mechanism in `tmux` does not work reliably, so the only solution ATM is a [patched version of tmux](https://github.com/patrislav1/tmux/tree/fix-hyperlinks) with native support for hyperlinks.

## Prerequisites

* Python 3
* gcc, make
* Visual Studio Code or VSCodium
* A [terminal emulator with support for hyperlinks](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda#file-hyperlinks_in_terminal_emulators-md)

## Example

![Example](example.png)