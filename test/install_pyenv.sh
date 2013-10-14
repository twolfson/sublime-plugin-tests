sudo apt-get install git -y
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
exec $SHELL
