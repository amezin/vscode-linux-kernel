Visual Studio Code project for Linux kernel sources
---------------------------------------------------

Ensure the kernel is built (at least, all *.cmd files should be generated):

    $ make

Clone this repository as ".vscode":

    $ git clone git@github.com:amezin/vscode-linux-kernel.git .vscode

Generate compile_commands.json:

    $ python .vscode/generate_compdb.py

Open the project:

    $ code .
