# vagrantfile is primaraly for testing production enviroment type things, though you can use it however you like
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "forwarded_port", guest: 80, host:8000
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    # install dependencies
    apt-get install -y python3-dev libpq-dev postgresql postgresql-contrib apache2
    # make required folders
    sudo mkdir /var/log/gunicorn
    sudo touch /var/log/gunicorn/test_app_error.log
    # configure pip, venv and psycopg2
    apt-get -y install python3-pip
    pip install -U pip
    apt-get -y install python3-venv
    python3 -m venv /vagrant/venv
    /vagrant/venv/bin/pip install -r /vagrant/requirements.txt
    # configure postgresql
    sudo -u postgres psql -c "CREATE DATABASE mydb;"
    sudo -u postgres psql -c "CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypass'; ALTER ROLE myuser SET client_encoding TO 'utf8'; ALTER ROLE myuser SET default_transaction_isolation TO 'read committed'; ALTER ROLE myuser SET timezone TO 'UTC'; GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser; ALTER USER myuser CREATEDB;"
    /vagrant/venv/bin/python3 /vagrant/manage.py migrate --settings=pelican.settings.production
    # configure sqlite
    /vagrant/venv/bin/python3 /vagrant/manage.py migrate --settings=pelican.settings.dev
    # configure apache
    cp /vagrant/nocode/config-files/000-defualt.conf /etc/apache2/sites-available/000-default.conf
    sudo mkdir /var/www/pelican
    a2enmod proxy proxy_http headers
    sudo systemctl restart apache2
    # set up gunicorn as a service
    sudo cp /vagrant/nocode/config-files/pelican.service /etc/systemd/system
    # collect static files
    mkdir /var/cache/pelican
    mkdir /var/cache/pelican/static
    /vagrant/venv/bin/python3 /vagrant/manage.py collectstatic --settings=pelican.settings.production
    # restart everything
    sudo systemctl restart apache2
  SHELL
end