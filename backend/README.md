The Backend
===========
This is the REST service which supports the front-end application.


Quick Start for Development
---------------------------

###Requirements:
* (Optional) homebrew: http://brew.sh - if you are working on a Mac, this will make it easy to install the other requirements.  
  If you're on Linux, you already have a package manager so use that.
* Python 2.7: http://www.python.org 
  (brew install python / sudo apt-get install python)
* pip: https://pypi.python.org/pypi/pip 
  (already included if you do a brew install python / sudo apt-get install python-pip)
* foreman: https://github.com/ddollar/foreman
  (gem install foreman -- if you have Ruby installed)

You'll also need an database.
For light development or front-end work, sqlite is fine (http://www.sqlite.org brew install sqlite / sudo apt-get install sqlite3)
I would recomend using postgresql for real backend development, as that's what we'll be running in production and sqlite doesn't support things like migrations.

###First Run:
* pip install virtualenv
* git clone [git@github.com:freedomgamees/parklab.git](git@github.com:freedomgamees/parklab.git])
* cd parklab
* virtualenv venv
* source venv/bin/activate
* pip install -r backend/requirements.txt
* pip install -r backend/test-requirements.txt
* If you are using sqlite, change the DATABASE\_URL line in the .dev\_env file in this directory to read: "DATABASE\_URL=sqlite:///test.db"
* If you are using postgresql, then issue the command: "createdb parklab"
* foreman start create\_db -e .dev\_env
* foreman start dev\_server -e .dev\_env

The REST service is now available at [http://localhost:5000](http://localhost:5000)

###Subsequent Runs:
* cd parklab
  (if you aren't there already)
* source venv/bin/activate
  (if your shell has not already sourced this file)
* pip install --upgrade -r requirements.txt 
  (if requirements.txt has changed and you need to install new requirements)
* rm -f backend/src/backend/test.db; foreman start create\_db -e .dev\_env
  (if the db schema has changed and you need to flush and recreate your sqlite database)
* foreman start dev\_server -e .dev\_env

###Other Utilities:
* "foreman run tests -e .test\_env"
  runs the unit tests and outputs coverage information (the -e .test\_env bit is important!)
* "foreman run bash -e .dev\_env"
  gives you a shell session with your environment set up to run the REST service
