Dayone web journal
==================

Blog to the web directly from within your Dayone journal app. 

Login with your dropbox account and simply add #public tag to your journal entry to publish it to the web.
You can also make anonymous blog posts by using #anonymous tag.

Note: The tags are configurable from the edit profile interface

### Demo - coming soon

[http://Dayone.in](http://dayone.in)

## Prerequists

  * Django
  * Celery
  * Redis
  * (Mysql or sqlite)
  * Python
  * markdown
  * python dropbox api/sdk

## How to run

  * run ./migrate.sh to setup databases
  * start redis server
  * run ./celery-worker.sh to start celery for background processing

## Todo

  * Sandbox and add virtual environment file
  * Support adding of permalink back to the content for easy reference
  * implement user profiles, pagination for dayroll, public posts
  * Improve the UI


