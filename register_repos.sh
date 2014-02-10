
register_repo()
{
URL=$1
FOLDER=$2
git clone $URL $FOLDER
mr register $FOLDER
mr config $FOLDER update="git stash && git pull --rebase && git stash pop"
}

touch .mrconfig

TRUSTFILE=~/.mrtrust
echo "$(pwd)/.mrconfig" >> $TRUSTFILE

register_repo git@github.com:obreitwi/pydemx.git pydemx
register_repo git@github.com:obreitwi/dot_vim.git vim
register_repo git@github.com:obreitwi/dot_zsh.git zsh
register_repo git@github.com:obreitwi/dot_tmux.git tmux


