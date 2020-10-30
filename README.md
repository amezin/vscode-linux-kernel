Visual Studio Code project for Linux kernel sources
===================================================

Ensure the kernel is built (at least, all `*.cmd` files should be generated):

    $ make defconfig
    $ make

Clone this repository as ".vscode":

    $ git clone git@github.com:amezin/vscode-linux-kernel.git .vscode

Generate compile_commands.json:

    $ python .vscode/generate_compdb.py

Open the project:

    $ code .

Out-of-tree builds
------------------

https://github.com/amezin/vscode-linux-kernel/issues/4

Kernel can be built with separate output directory:

    $ make O=../linux-build defconfig
    $ make O=../linux-build

In this case, you should pass the directory to `generate_compdb.py`:

    $ python .vscode/generate_compdb.py -O ../linux-build

`compile_commands.json` will still be generated in the `.vscode` directory (under root of the `linux` repository).
Unfortunately, `tasks.json` will not work out of the box in this configuration (TODO).
