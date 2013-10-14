#!/bin/bash

# If we are to install Sublime Text 2
if test "$SUBLIME_TEXT_VERSION" = "2.0"; then
  # http://askubuntu.com/questions/172698/how-do-i-install-sublime-text-2
  sudo add-apt-repository ppa:webupd8team/sublime-text-2 -y
  sudo apt-get update
  sudo apt-get install sublime-text -y
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text
elif test "$SUBLIME_TEXT_VERSION" = "3.0"; then
  sudo add-apt-repository ppa:webupd8team/sublime-text-3 -y
  sudo apt-get update
  sudo apt-get install sublime-text-installer -y
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text

  # If we are in Travis, update shm. Fixes 'Unable to init shm' from `sublime_text --wait`
  # https://travis-ci.org/twolfson/sublime-plugin-tests/builds/12500309
  # https://github.com/travis-ci/travis-core/issues/187
  if test -n "$TRAVIS"; then
    sudo rmdir /dev/shm
    sudo ln -Tsf /{run,dev}/shm
  fi
fi