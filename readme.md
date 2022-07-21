# OTH KDSP Project
This is an application for analyzing Twitter datasets and users. 

## Required modules
All the required modules can be found in the requirements.txt file.

## Setup
### 1. Start the virtual enviroment

*Linux Terminal:* \
In the project directory type `virtualenv env`

*Windows Powershell:* \
In the project directory type `env/Scripts/Activate.ps1`

### 2. Set all necessary environment variables
You will need to have a bearer token for the Twitter API v2.

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

### 3. Start the project
Type `flask run`
The Project should start now. Inside the terminal you should see a address to navigate to to use the application.
