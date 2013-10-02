# If we are to install Sublime Text 2
if test $SUBLIME_TEXT_VERSION = "2.0"; then
  # http://askubuntu.com/questions/172698/how-do-i-install-sublime-text-2
  sudo add-apt-repository ppa:webupd8team/sublime-text-2 -y
  sudo apt-get update
  sudo apt-get install sublime-text -y
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text
fi