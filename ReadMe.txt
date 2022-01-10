# OTH KDSP Project

## Setup
### Start the virtual enviroment

*Linux Terminal:* \
In the project directory type `virtualenv env`

*Windows Powershell:* \
In the project directory type `env/Scripts/Activate.ps1`

### Set all necessary environment variables

*Linux Terminal:* \
Type
`export FLASK_APP=run.py`
and 
`export BEARER_TOKEN=<your twitter api bearer token here>`

*Windows Powershell:* \
Type
`$env:FLASK_APP = 'run.py'`
and 
`$env:BEARER_TOKEN = '<your twitter api bearer token here>'`

### Start the project
Type `flask run`
