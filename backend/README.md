The Backend
===========
This is a REST service written in Python, Flask and SQLAlchemy
which supports the front-end PlanetLab application.

The full API spec is [available here.](API_DOCS.md)

Information on contributing is [available here.](CONTRIBUTING.md)


Quick Start for Development
---------------------------

###Requirements
* Python 2.7: http://www.python.org 
* pip: https://pypi.python.org/pypi/pip 
* Foreman: https://github.com/ddollar/foreman
* PostgreSQL 9.3: http://www.postgresql.org
* An AWS account, S3 bucket and CloudFront distribution for
hosting static content: http://aws.amazon.com
* (optional) graphviz for generating database schema diagrams

###Fulfilling the Requirements on a Mac
* Install the package manager Homebrew: http://brew.sh
* Install Python and pip: brew install python
* Install Ruby: brew install ruby
* Install Foreman: gem install foreman
* Install PostgreSQL: brew install postgresql
* Set PostgreSQL to start on boot:
  ln -s /usr/local/Cellar/postgresql/9.3.\*/homebrew.mxcl.postgresql.plist
  ~/Library/LaunchAgents/
* Start PostgreSQL now:
  launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
* (optional) Install graphviz: brew install graphviz

###Fulfilling the Requirements on Ubuntu
* Install Python: sudo apt-get install python
* Install pip: sudo apt-get install python-pip
* Install Ruby: sudo apt-get install ruby1.9.1
* Install Foreman: gem install foreman
* Install PostgreSQL: sudo apt-get install postgresql-9.3

If postgresql-9.3 is not available,
you need to update your apt repository sources as described here first:
http://www.postgresql.org/download/linux/ubuntu/

* Create a PostgreSQL user: sudo -u postgres createuser -rs \<your username\>

where 'your username' is your linux username (whatever pops out from a whoami)
* Install PostgreSQL and Python dev headers:
  sudo apt-get install libpq-dev postgresql-server-dev-9.3 python-dev
* (optional) Install graphviz: sudo apt-get install graphviz

###Creating your S3 Bucket
Please read https://devcenter.heroku.com/articles/s3 for an overview of
how we are using S3 with our application and Heroku.

The relevant steps are:
* Create an AWS account with amazon: http://aws.amazon.com
* Create an S3 bucket: https://console.aws.amazon.com/s3
* Select the bucket, click 'Properties,' 'Permissions,'
  'Edit CORS Configuration' and give it a policy like:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```
* Upload an image of your choice named 'default-avatar.jpg' into the bucket
* Right click 'default-avatar.jpg' and click the 'Make Public' button
* On the security credentials tab: https://console.aws.amazon.com/iam/#users
  create an IAM user with permissions to access S3 using a policy like:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::<your-bucket-name>/*"]
    },
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::<your-bucket-name>"]
    }
  ]
}
```
where 'your-bucket-name' is the bucket you created above
* Hold onto the access and secret keys for this IAM user --
  you'll need them soon

###Creating your CloudFront Distribution
* Go to https://console.aws.amazon.com/cloudfront/home
* Click 'Create Distribution'
* Click 'Continue'
* Click the 'Origin Domain Name' input box, a drop-down should appear.
Select the S3 bucket you just created.
* The default options are all fine, click 'Create Distribution' at the bottom.
* Take note of your distribution's domain name, you will need it soon.
It should be something like r5cqxy3728842.cloudfront.net

###First Run:
* pip install virtualenv
* git clone \<your fork of the repo\>
* cd Planet-Lab (or whatever you named your fork)
* virtualenv venv
* source venv/bin/activate
* pip install -r backend/requirements.txt
* pip install -r backend/test-requirements.txt
* createdb parklab
* edit the .dev\_env file so that it contains your correct CloudFront domain,
  bucket name and AWS credentials in the fields
  CLOUDFRONT\_URL,
  S3\_BUCKET,
  AWS\_ACCESS\_KEY\_ID and
  AWS\_SECRET\_ACCESS\_KEY

#####NEVER COMMIT YOUR KEYS INTO THE REPO
######issue this command to prevent you from accidentally doing so: git update-index --assume-unchanged .dev\_env

* foreman run --env .dev\_env create\_db
* foreman start dev\_server -e .dev\_env

The REST service is now available at [http://localhost:5000](http://localhost:5000)

###Subsequent Runs:
* cd parklab
  (if you aren't there already)
* source venv/bin/activate
  (if your shell has not already sourced this file)
* pip install --upgrade -r requirements.txt 
  (if requirements.txt has changed and you need to install new requirements)
* foreman run flush\_db -e .dev\_env
  (if the db schema has changed and you need to flush and recreate your database)
* foreman start dev\_server -e .dev\_env

###Other Utilities:
* "foreman run be_tests -e .test\_env"
  runs the unit tests and outputs coverage information (the -e .test\_env bit is important!)
* "foreman run bash -e .dev\_env"
  gives you a shell session with your environment set up to run the REST service
* "foreman run flush\_db -e .dev\_env" drops and recreates the db schema
* "bin/db\_diagram" generates database schema diagrams in PNG and
  graphviz's .dot formats in the current directory named
  'schema.png' and 'schema.dot' respectively
