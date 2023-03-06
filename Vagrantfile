Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    # install postgresql
    apt-get -y install postgresql postgresql-contrib
    # configure pip
    apt-get -y install python-pip
    pip install -U pip
    # setup venv
    apt-get -y install python3-venv
    python3 -m venv /vagrant/venv
    /vagrant/venv/bin/pip install django
    # install psycopg2
    sudo apt install -y python3-dev libpq-dev
    /vagrant/venv/bin/pip install psycopg2
    # configure postgresql
    sudo -u postgres psql -f /vagrant/setup.sql
    /vagrant/venv/bin/python3 /vagrant/manage.py migrate
  SHELL
end