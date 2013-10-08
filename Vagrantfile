# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  # export DISPLAY=:99.0
  # /usr/bin/Xvfb $DISPLAY -screen 0 1024x768x24 &
  # sublime_text --wait &
  # ps ax | grep sublime

  # --crawl appears via --add
  # 26029 pts/3    Sl     0:03 sublime_text3 --wait
  # 26067 pts/3    Sl     0:00 /home/todd/Downloads/sublime_text_3/plugin_host 26029
  # 26170 pts/3    RNl    0:05 /home/todd/Downloads/sublime_text_3/sublime_text --crawl 26029:crawl:2
end
