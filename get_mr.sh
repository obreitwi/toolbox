#!/bin/zsh

PATH_DIR=$HOME/.local/bin

git clone https://git.joeyh.name/git/myrepos.git mr
mkdir -p ~/.local/bin
ln -s -f -v $(pwd)/mr/mr $PATH_DIR/mr

echo $PATH | grep "$PATH_DIR" > /dev/null

if [ $? -eq 1 ]; then
	export PATH=$PATH:$PATH_DIR
fi
