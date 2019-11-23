#!/usr/bin/sh

DIR=$(mktemp -d)
wget -O $TMP/master.tar.gz https://codeload.github.com/adabru/sciter-starter/tar.gz/master
tar -xzf $TMP/master.tar.gz
mv $TMP/sciter-starter-master ~/.sciter
cp ~/.sciter/sciter-starter.py ~/bin
