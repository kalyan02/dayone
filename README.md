Dayone web journal
==================

Blog to the web directly from within your Dayone journal app. 

Login with your dropbox account and simply add #public tag to your journal entry to publish it to the web.
You can also make anonymous blog posts by using #anonymous tag.

Note: The tags are configurable from the edit profile interface

### Demo - coming soon

[http://Dayone.in](http://dayone.in)

## Prerequists

  * Python
  * Celery
  * Redis
  * (Mysql or sqlite)
  * python packages in requirements.txt

## Setup
Rename `do/private_config-sample.py` to `do/private_config.py`. This is your private configuration file for setup. 
Fill in the following information

  * `DROPBOX_APP_ID` - Your Dropbox API key
  * `DROPBOX_API_SECRET` - API secret
  * `SECRET_KEY` - Django app secret key for hashing cookies
  * `AUTO_ADMINS` - Admin username/password information for automatically creating admin login

Install required packages using virtualenv

  * run `$ virtualenv ENV`
  * run `$ source ./ENV/bin/activate`
  * run `$ pip install -r requirements.txt`

## How to run

  * install and start redis server
  * run `./migrate.sh` to setup databases
  * run `./celery-worker.sh` to start celery for background processing

## Todo

  * Support adding of permalink back to the content for easy reference
  * implement user profiles, pagination for dayroll, public posts
  * Improve the UI
  * Implement data update scheduler for all users in the system

## License
Please refer the `LICENSE` file.

