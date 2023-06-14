# Install at your own risk!
This software is made by me for the purpose of learning better Django, and is not intended to actually be used anywhere, while it is intended to be secure and usable it is not guaranteed to be even a good thing to consider!
# Step 1: Update server
Switch to the root account before following the instructions listed here, you may also want to activate the virtual environment after it is created.

Run the commands 
```
sudo apt update
sudo apt upgrade
```
to update your server.
# Step 2: Install non-python dependencies
There aren't many, just run

```
sudo apt install -y python3-dev libpq-dev postgresql postgresql-contrib apache2
```

# Step 3: Clone the repository
Change directory to `/opt` and clone the repository with.

```
sudo git clone https://github.com/Callen44/pelican.git
``` 
Then use `cd` again and move into the new folder named `pelican`.
# Step 4: prepare for storing logs
This is easy,
```
sudo mkdir /var/log/gunicorn
sudo touch /var/log/gunicorn/test_app_error.log
```
gunicorn (once set up) will store it's logs here.
# Step 5: Make the virtual enviroment
This is where we make a place to store the python dependencies that were not installed earlier. And this last command installs the python dependencies from the reqirements.txt file

```
    sudo apt -y install python3-pip
    sudo pip install -U pip
    sudo apt -y install python3-venv
    sudo python3 -m venv /opt/pelican/venv
    sudo /opt/pelican/venv/bin/pip install -r /opt/pelican/requirements.txt
```
# Step 6: Prepare the database
This is where the security gets low, you should probobly install a firewall. But I don't really intend this to be actually deployed so use your own discression and be careful.
```
sudo -u postgres psql -c "CREATE DATABASE mydb;"
    sudo -u postgres psql -c "CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypass'; ALTER ROLE myuser SET client_encoding TO 'utf8'; ALTER ROLE myuser SET default_transaction_isolation TO 'read committed'; ALTER ROLE myuser SET timezone TO 'UTC'; GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser; ALTER USER myuser CREATEDB;"
    sudo /opt/pelican/venv/bin/python3 /opt/pelican/manage.py migrate --settings=pelican.settings.production
```
DEFINITELY DON'T USE THE PASSWORD HERE! It is anything but secure, so make sure to secure the database YOURSELF I am not responsible for any lost data.
# Step 7: configure apache
This will copy over the defualt configuration file and then set up apache as a reverse proxy. the configuration file will have apache respond to every request that comes in port 80, (ex. I will respond to false domain names, bare ip adresses, and legit domain names) you may want to change this.
```
sudo cp /opt/pelican/nocode/config-files/000-defualt.conf /etc/apache2/sites-available/000-default.conf
sudo mkdir /var/www/pelican
sudo a2enmod proxy proxy_http headers
sudo systemctl restart apache2
```
# Step: 8 make gunicorn a service
There is a service file in the repository folder `nocode`, just copy this over to `/etc/systemd/system`.
```
sudo cp /opt/pelican/nocode/config-files/pelican.service /etc/systemd/system
```
# Step 9: collect static files
This is a bit of a long one but here we make folders for static files to stay in, then save the static files to that folder.
```
sudo mkdir /var/cache/pelican
sudo mkdir /var/cache/pelican/static
```
Then we collect the files
```
sudo /opt/pelican/venv/bin/python3 /opt/pelican/manage.py collectstatic --settings=pelican.settings.production
```
# Step 10: enable services and reboot
We need to enable pelican so that it actually runs when you start the system, we can do that with the command.
```
sudo systemctl enable pelican
```
Now we can run the 2 commands
```
sudo systemctl restart apache2
sudo systemctl start pelican
```
which would apply configuration files, then start the back end. But just to be on the safe side I would reccomend you reboot with `reboot`.
