# It-Portal use Django3 and Gunicorn

## Installation

### Debian, Ubuntu and other like.

$ `apt install -y python3 python3-pip python3-venv`

$ `git clone https://github.com/Vilocer/it-portal.git && cd it-portal`

$ `python3 -m venv env && source env/bin/activate`

$ `pip install -r requirements.txt`

$ `chmod +x bin/start_gunicorn.sh`

## Settings

- Now all settings in the it_portal/config/settings.py. But then we will use venv variables.

## Run Gunicorn Web-Server

### Debian, Ubuntu and other like.

$ `./bin/start_gunicorn.sh`


