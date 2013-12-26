# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Start from closest model to Travis CI
  # http://about.travis-ci.org/docs/user/ci-environment/#CI-environment-OS
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Set up variables
  $install_user_vars = <<SCRIPT
    # Set the term to be xterm for SSH sessions
    if ! grep TERM /etc/environment > /dev/null; then
      echo "TERM=xterm" >> /etc/environment
    fi

    # Automatically terminate sublime for test runs
    if ! grep SUBLIME_AUTO_KILL /etc/environment > /dev/null; then
      echo "SUBLIME_AUTO_KILL=TRUE" >> /etc/environment
    fi

    # Specify the environment as Vagrant
    if ! grep VAGRANT /etc/environment > /dev/null; then
      echo "VAGRANT=TRUE" >> /etc/environment
    fi
SCRIPT
  config.vm.provision "shell", inline: $install_user_vars

  $install_xvfb = <<SCRIPT
    # If xvfb isn't installed, install it
    if ! test -f /usr/bin/Xvfb; then
      sudo apt-get update
      sudo apt-get install xvfb libgtk2.0-0 -y
    fi
SCRIPT
  config.vm.provision "shell", inline: $install_xvfb

  $install_package = <<SCRIPT
    # For Python 3 development
    if false; then
      # Install Python 3
      # DEV: Unfortunately, apt-get flavor is 3.2 which doesn't support our packages to well
      wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.xz
      tar xvf Python-3.3.2.tar.xz
      cd Python-3.3.2
      sudo apt-get install make -y
      ./configure
      make
      sudo make install
      sudo rm /usr/bin/python
      sudo ln -s $PWD/python /usr/bin/python

      # and use distribute over pip
      wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
      sudo python ez_setup.py
    else
    # Otherwise, install pip
      cd /vagrant
      sudo apt-get install python-pip -y
    fi

    # Install our package for development
    python setup.py develop

    # Install dev dependencies
    pip install -r requirements-dev.txt
SCRIPT
  config.vm.provision "shell", inline: $install_package

  $launch_xvfb = <<SCRIPT
    # Set and persist DISPLAY to :99.0
    export DISPLAY=:99.0
    if ! grep DISPLAY /etc/environment > /dev/null; then
      echo "DISPLAY=$DISPLAY" >> /etc/environment
    fi

    # Set up Xvfb
    /usr/bin/Xvfb $DISPLAY -screen 0 1024x768x24 &
SCRIPT
  config.vm.provision "shell", inline: $launch_xvfb

  $install_sublime = <<SCRIPT
    # If Sublime Text isn't installed, install it
    source /etc/environment
    if test -z "$(which subl)"; then
      if test -z "$(which add-apt-repository)"; then
        sudo apt-get install python-software-properties -y
      fi
      if test -z "$(which curl)"; then
        sudo apt-get install curl -y
      fi
      curl http://rawgithub.com/twolfson/sublime-installer/0.1.1/install.sh | sh -s $SUBLIME_TEXT_VERSION

      # Output the version
      subl --version
    fi
SCRIPT

  config.vm.define "st2" do |st2|
    $configure_st2 = <<SCRIPT
      # Set and persist SUBLIME_TEXT_VERSION
      export SUBLIME_TEXT_VERSION=2
      if ! grep SUBLIME_TEXT_VERSION /etc/environment > /dev/null; then
        echo "SUBLIME_TEXT_VERSION=$SUBLIME_TEXT_VERSION" >> /etc/environment
      fi
SCRIPT
    st2.vm.provision "shell", inline: $configure_st2
    st2.vm.provision "shell", inline: $install_sublime
  end

  config.vm.define "st3" do |st3|
    $configure_st3 = <<SCRIPT
      # Set and persist SUBLIME_TEXT_VERSION
      export SUBLIME_TEXT_VERSION=3
      if ! grep SUBLIME_TEXT_VERSION /etc/environment > /dev/null; then
        echo "SUBLIME_TEXT_VERSION=$SUBLIME_TEXT_VERSION" >> /etc/environment
      fi
SCRIPT
    st3.vm.provision "shell", inline: $configure_st3
    st3.vm.provision "shell", inline: $install_sublime
  end


  # When done, vagrant ssh
  # cd /vagrant
  # ./test.sh
end
