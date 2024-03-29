#!/usr/bin/env bash
#
# Copyright (C) 2013-2024 Oliver Breitwieser
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
#

set -Eeuo pipefail

register_repo()
{
URL=$1
FOLDER=$2
git clone $URL $FOLDER
mr register $FOLDER
mr config $FOLDER update="if [ \$(git status --porcelain | grep -v '^\?\?' | wc -l) -gt 0 ]; then git stash && git pull --rebase && git stash pop; else git pull; fi"
}

touch .mrconfig

TRUSTFILE=~/.mrtrust
CONFIGLOCATION="$(pwd)/.mrconfig" 
sed -i "\\:$CONFIGLOCATION:d" $TRUSTFILE
echo "$CONFIGLOCATION" >> $TRUSTFILE

register_repo git@github.com:obreitwi/pydemx.git pydemx
register_repo git@github.com:obreitwi/dot_vim.git vim
register_repo git@github.com:obreitwi/dot_zsh.git zsh
register_repo git@github.com:obreitwi/dot_tmux.git tmux
register_repo git@github.com:obreitwi/py-rpush.git small-tools/rpush
register_repo git@github.com:obreitwi/dot_nushell.git nushell


# register_repo https://github.com/obreitwi/pydemx.git pydemx
# register_repo https://github.com/obreitwi/dot_vim.git vim
# register_repo https://github.com/obreitwi/dot_zsh.git zsh
# register_repo https://github.com/obreitwi/dot_tmux.git tmux
# register_repo https://github.com/obreitwi/py-rpush.git small-tools/rpush
