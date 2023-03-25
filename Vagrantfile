# vagrantfile is primaraly for testing production enviroment type things, though you can use it however you like
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    # install miscellaneous dependencies
    apt-get install -y python3-dev libpq-dev
    apt-get -y install postgresql postgresql-contrib
    # configure pip, venv and psycopg2
    apt-get -y install python3-pip
    pip install -U pip
    apt-get -y install python3-venv
    python3 -m venv /vagrant/venv
    /vagrant/venv/bin/pip install -r /vagrant/requirements.txt
    # configure postgresql
    sudo -u postgres psql -c "CREATE DATABASE mydb; CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypass'; ALTER ROLE myuser SET client_encoding TO 'utf8'; ALTER ROLE myuser SET default_transaction_isolation TO 'read committed'; ALTER ROLE myuser SET timezone TO 'UTC'; GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser; ALTER USER myuser CREATEDB;"
    /vagrant/venv/bin/python3 /vagrant/manage.py migrate
  SHELL
end