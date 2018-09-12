#!/bin/zsh
#
# Copyright (C) 2013-2018 Oliver Breitwieser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

PATH_DIR=$HOME/.local/bin

git clone https://git.joeyh.name/git/myrepos.git mr
mkdir -p ~/.local/bin
ln -s -f -v $(pwd)/mr/mr $PATH_DIR/mr

echo $PATH | grep "$PATH_DIR" > /dev/null

if [ $? -eq 1 ]; then
	export PATH=$PATH:$PATH_DIR
fi
