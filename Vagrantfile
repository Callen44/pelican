Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get -y install postgresql postgresql-contrib
    # add more commands here to install other dependencies
  SHELL
end