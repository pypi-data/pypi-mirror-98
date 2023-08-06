# Toolchains

Toolchains can be specified only by their name, or with a version number
attached. For example, `clang` will use whatever `clang` binary you have in
your `$PATH`, while `clang-10` will specifically use `clang` version 10.

## gcc

This toolchain will use `gcc` as compiler. It is the default if you don't
request a specific toolchain. Specify `gcc-N` for requesting specific `gcc`
versions.

## clang

This toolchain uses `clang` as compiler, but the GNU binutils tools for
assembling and linking. Specify `clang-N` for specific versions.

## llvm

This toolchain does a full LLBV build, i.e. one with `LLVM=1`: compile with
clang, and assemble/link with the LLVM tools. Specify `llvm-N` for requesting
specific LLVM versions.
