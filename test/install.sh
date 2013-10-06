#!/bin/sh

# `ps ax | grep sublime` shows that ST3 is running in a VM but not in Vagrant
# TODO: See if we can get a plugin to output a simple file (works in VM, not in Vagrant -- requires ST3 to be started first)
# TODO: See if it will run in a VM (totally fine)
# TODO: What happens if we connect an x11-forwarding?

# Made progress with --wait option
# (sublime_text:4947): Gtk-WARNING **: cannot open display: :99.0

# Fixed up Xvfb invocation and --wait is working @_@
# /usr/bin/Xvfb :99 -ac -screen 0 1024x768x24 &

# If we are to install Sublime Text 2
if test $SUBLIME_TEXT_VERSION = "2.0"; then
  # http://askubuntu.com/questions/172698/how-do-i-install-sublime-text-2
  sudo add-apt-repository ppa:webupd8team/sublime-text-2 -y
  sudo apt-get update
  sudo apt-get install sublime-text -y
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text
elif test $SUBLIME_TEXT_VERSION = "3.0"; then
  sudo add-apt-repository ppa:webupd8team/sublime-text-3 -y
  sudo apt-get update
  sudo apt-get install sublime-text-installer -y
  sudo ln -s /usr/bin/subl /usr/bin/sublime_text
fi