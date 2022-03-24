# Sysadmin Setup Guide

This instruction manual is targeted at servers running `ubuntu server 20.4`. Other distributions will work but might require some extra modifications.

## Table Of Contents

[TOC]

## Installation

For the setup you can decide for yourself how to organize users. You can create a single user for the whole application, or create 2 separate users. One for the backend and one for the frontend. This last one is the option we will use in the rest of this guide.

### Frontend

#### Creating the user

First create the frontend user from an admin account.

```shell
[admin] $ sudo useradd -m frontend
```

#### Login as the user

This user should not have a password. This way only admins or people with the right ssh-key can login as the user.

##### Sysadmins

```shell
[admin] $ sudo su frontend
```

##### Ssh

To be able to login via ssh a sysadmin should add your ssh key to the `authorized_keys` file.

```shell
[frontend] $ echo "<ssh-key>" >> /home/frontend/.ssh/authorized_keys
```

See [Generating SSH Key]() for instructions on how to generate a ssh key. 

#### Installing Node and Yarn

The backend requires a version of node >= 16. Because apt repositories can be quite outdated and other services on the server might require another version of node we use [asdf](https://asdf-vm.com) to manage to node version for our user.

Instructions on how to install asdf for `ubuntu 20.4` can be found in their [documentation](https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies).

Once installed we can install the node plugin and install the required node version.

```shell
[frontend] $ asdf plugin add nodejs
[frontend] $ asdf install nodejs 16.14.2
[frontend] $ asdf global nodejs 16.14.2
```

Then verify the correct installation.

```shell
[frontend] $ node --version
v16.14.2
```

Once node is functioning propperly you can install yarn using:

```shell
[frontend] $ npm install --global yarn
```

#### Cloning the repository

If the repository is still private. Cloning using SSH should be used. If it is public HTTPS becomes the simpler option.

##### Via SSH

Before you can clone the repository you need to add a deploy key to the repository. So first generate a key on the server.

```shell
[frontend] $ ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/id_deploy
```

Make sure to leave the password empty. Adding a password makes the update flow later on require human interaction.

Then add the content of `/home/frontend/.ssh/id_deploy.pub` as a deploy key to the github repository. Last step before you can pull the repository is specifying in the SSH config which key we want to use for `github.com`.

Add the following to `/home/frontend/.ssh/config`.

```shell
Host github.com
    IdentityFile ~/.ssh/ide_deploy
```

Now you can clone the repository using:

```shell
[frontend] $ git clone git@github.com:SELab-2/OSOC-3.git osoc
```

##### Via HTTPS

clone the repository using:

```shell
[frontend] $ git clone https://github.com/SELab-2/OSOC-3.git osoc
```

#### Building the frontend

Navigate to the frontent folder in the cloned repository and install the dependencies.

```shell
[frontend] $ cd osoc/frontend
[frontend] $ yarn install
```

Then create the `.env` file.

```shell
[frontend] $ echo "REACT_APP_BASE_URL=https://<your domain>" > .env 
```

Then build the frontend.

```shell
[frontend] $ yarn build
```

The static build of the site is now located at `/home/frontend/osoc/frontend/build`.

For more information and options about the frontend please refer to the frontend [documentation]().

### Mariadb

The application requires a running instance of mariadb >= 10.4. There are 2 general ways to host a mariadb server that would be viable for us. The first one would be to install mariadb on our system. The second one would to be use docker.

For this guide we chose the first option.

#### Installing Mariadb

The maraidb version available in the apt repositories (Currently 10.3) is too outdated for our application. You should follow the installation as described [here](https://mariadb.com/docs/operations/upgrades/upgrade-community-server-cs10-5-ubuntu20/). A plain command overview of how to install maraidb 10.5.

```shell
[admin] $ sudo apt install wget
[admin] $ wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
# The following might get outdated
[admin] $ echo "b9e90cde27affc2a44f9fc60e302ccfcacf71f4ae02071f30d570e6048c28597 mariadb_repo_setup" | sha256sum -c -
[admin] $ chmod +x mariadb_repo_setup
[admin] $ sudo ./mariadb_repo_setup --mariadb-server-version="mariadb-10.5"
[admin] $ sudo apt update
[admin] $ sudo apt install mariadb-server
```

Once the server is installed **make sure** to run the `mariadb-secure-instalation` script. This is **very important!** The database will be insecure if not run. 

#### Configuring Database

The next step is to create the database and add the backend user.

Open the database shell using `mariadb` and execute the following statements:

```sql
--Create the database for the backend
CREATE DATABASE osoc;

--Create the backend user and grant access
CREATE USER 'backend'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL PRIVILES ON osoc.* FOR 'backend'@'localhost';

FLUSH PRIVILEGES;
```

Afther executing these you shoud be able to login as the backen user.

```shell
[admin] $ mariadb -u backend -p
```

### Backend

#### Creating the user

First create the frontend user from an admin account.

```shell
[admin] $ sudo useradd -m backend
```

#### Login as the user

This user should not have a password. This way only admins or people with the right ssh-key can login as the user.

##### Sysadmins

```shell
[admin] $ sudo su backend
```

##### Ssh

To be able to login via ssh a sysadmin should add your ssh key to the `authorized_keys` file.

```shell
[backend] $ echo "<ssh-key>" >> /home/backend/.ssh/authorized_keys
```

See [Generating SSH Key]() for instructions on how to generate a ssh key. 


#### Installing Python

The backend requires a version of node >= 16. Because apt repositories can be quite outdated and other services on the server might require another version of node we use [asdf](https://asdf-vm.com) to manage to node version for our user. Installations are per user. So we also have to install asdf for the backend user.

Instructions on how to install asdf for `ubuntu 20.4` can be found in their [documentation](https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies).

Once installed we can install the node plugin and install the required node version.

First you need to install the required dependecies to compile python.

```shell
[admin] $ sudo apt install zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

Then you can go on and install python.

```shell
[backend] $ asdf plugin add python
[backend] $ asdf install python 3.10.2
[backend] $ asdf global python 3.10.2
```

Then verify the correct installation.

```shell
[backend] $ python3 --version
Python 3.10.2
```

Once node is functioning propperly you can update pip using:

```shell
[backend] $ pip3 install -U pip
```

#### Cloning the repository

If the repository is still private. Cloning using SSH should be used. If it is public HTTPS becomes the simpler option.

##### Via SSH

Before you can clone the repository you need to add a deploy key to the repository. So first generate a key on the server.

```shell
[backend] $ ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/id_deploy
```

Make sure to leave the password empty. Adding a password makes the update flow later on require human interaction.

Then add the content of `/home/backend/.ssh/id_deploy.pub` as a deploy key to the github repository. Last step before you can pull the repository is specifying in the SSH config which key we want to use for `github.com`.

Add the following to `/home/backend/.ssh/config`.

```shell
Host github.com
    IdentityFile ~/.ssh/ide_deploy
```

Now you can clone the repository using:

```shell
[backend] $ git clone git@github.com:SELab-2/OSOC-3.git osoc
```

##### Via HTTPS

clone the repository using:

```shell
[backend] $ git clone https://github.com/SELab-2/OSOC-3.git osoc
```

#### Installing dependencies

We will be installing dependencies in a virtual envirionment. You can create and activate one using the following command:

```shell
[backend] $ python3 -m venv venv-osoc
[backend] $ . venv-osoc/bin/activate
```

To manage dependecies we currently use 2 separate requirements files. Only `requirements.txt` has to be installed. The other one is for development setups. 

Make sure the mariadb librairies are installed.

```shell
[admin] $ sudo apt install libmariadb3 libmariadb-dev
```

```shell
(venv-osoc) [backend] $ cd osoc/backend
(venv-osoc) [backend] $ pip3 install -r requirements.txt
```

#### Configuring the application

All configuration of the application happend trough the `.env` file. Create one according to your needs.

```bash
DB_NAME=osoc
DB_USER=backend
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=3306
DB_USE_SQLITE=False

# Can be generated using openssl rand -hex 32
SECRET_KEY=<secet-key>
```

#### Running the application

Before running the backend the last step is to run the migrations.

```shell
(venv-osoc) [backend] $ alembic upgrade head
```

Afterwards you can start the application.

```shell
(venv-osoc) [backend] $ uvicorn --root-path /api src.app:app
```

To make sure the application starts on boot an restarts on failure you should run the application under a systemd user service. You can place the following file under `/home/backend/.config/systemd/user/backend.service`

```bash
[Unit]
Description=The OSOC backend
After=netwok.target

[Service]
Type=simple
WorkingDirectory=%h/develop/backend
ExecStart=bash -c ". ~/venv-osoc/bin/activate && uvicorn --root-path /api src.app:app"

[Install]
WantedBy=default.target
```

Enable lingering to make sure the user service is started even tho the user is not logged in.

```shell
[admin] $ sudo loginctl enable-linger backend
```

Then enable and start the service.

```shell
(venv-osoc) [backend] $ systemctl --user enable --now backend
```

The server is now accepting connections from localhost on port 8000.

### Nginx

First install Nginx.

```shell
[admin] $ sudo apt install nginx
```

Then add the config in `/etc/nginx/sites-eabled/domain.conf`.

```nginx
upstream backend {
	server 127.0.0.1:8000;
	keepalive 64;
}

server {
	server_name example.com;
    listen 80
        	
	location / {
		root /home/frontend/osoc/frontend/build;
		index index.html;
		
		try_files $uri $uri/ =404;
	}

	location = /api {
		return 302 /api/;
	}

	location /api/ {
		proxy_pass http://backend/;
	}
}
```

It is highly recomended to also install and configure certbot for ssl on your domain. [Guide](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal).

## Notes

### Generating SSH Keys

If u need to generate a ssh key in any of the stages we recomend u use a ed25519 key.

They can be generated using the following command.

```shell
$ ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/id_<name>
```