
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
register_repo git@github.com:obreitwi/rpush.git small-tools/rpush


