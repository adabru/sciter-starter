# Sciter-Starter

Sciter-Starter tries to provide the simplest possible way to setup a sciter project that is developed on linux and targets windows and linux.

## Installation

To install execute following command:

```
curl -o- https://raw.githubusercontent.com/adabru/sciter-starter/master/install.sh | bash
```

The script clones the sciter-starter repository to ~/.sciter and adds the shell-script `sciter-start` to your ~/bin folder. Alternatively, you can paste its contents into your terminal:

```sh
DIR=$(mktemp -d)
wget -O $TMP/master.tar.gz https://codeload.github.com/adabru/sciter-starter/tar.gz/master
tar -xzf $TMP/master.tar.gz
mv $TMP/sciter-starter-master ~/.sciter
cp ~/.sciter/sciter-starter.sh ~/bin
```

## IDE

The template works without any IDE, i.e. just with a text editor. Though, for debugging, code hints and "go to definition" IDE settings are needed. You can specify an IDE during template initialization, but currently only vscode is supported.

## About

A more complete templating repository can be found on: <https://github.com/ramon-mendes/SciterBootstrap> . Please use that if it suits your needs. This tool is meant to be used on Linux to create a project-template that uses the [sciter-sdk](https://sciter.com) and can be compiled for windows (via mingw) and linux.

This tool depends on python, tup, mingw, curl, wget, git.
