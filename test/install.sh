#!/bin/sh

# If we are to install Sublime Text 2
if test "$SUBLIME_TEXT_VERSION" = "2.0"; then
  # http://askubuntu.com/questions/172698/how-do-i-install-sublime-text-2
  sudo add-apt-repository ppa:webupd8team/sublime-text-2 -y
  sudo apt-get update
  sudo apt-get install sublime-text -y
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text
elif test "$SUBLIME_TEXT_VERSION" = "3.0"; then
  wget http://c758482.r82.cf2.rackcdn.com/sublime-text_build-3047_amd64.deb
  sudo dpkg --install sublime-text_build-3047_amd64.deb
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text
fi