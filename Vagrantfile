# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  # export TERM=xterm

  # export DISPLAY=:99.0
  # /usr/bin/Xvfb $DISPLAY -screen 0 1024x768x24 &
  # sublime_text --wait &
  # ps ax | grep sublime

  # VAGRANT: --add . opens new instances no matter what (Vagrant)
  # 5363 ?        Ssl    0:00 /opt/sublime_text/sublime_text --add .
  # 5371 ?        Sl     0:00 /opt/sublime_text/plugin_host 5363
  # 5395 ?        Ssl    0:02 /opt/sublime_text/sublime_text --add .
  # 5403 ?        Sl     0:00 /opt/sublime_text/plugin_host 5395

  # NORMAL: --crawl appears via --add
  # 26029 pts/3    Sl     0:03 sublime_text3 --wait
  # 26067 pts/3    Sl     0:00 /home/todd/Downloads/sublime_text_3/plugin_host 26029
  # 26170 pts/3    RNl    0:05 /home/todd/Downloads/sublime_text_3/sublime_text --crawl 26029:crawl:2

  # --wait returns only when Sublime is closed. Normally, it starts another process on the side.
  # This might be practical over the sleep loop.
  # If Sublime is already open, it does not wait to return

  # Okay... so command line invocation doesn't work. Maybe we can try the technique of package control?
end
