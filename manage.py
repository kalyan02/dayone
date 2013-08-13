#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "do.settings")

    from django.core.management import execute_from_command_line
    if len(sys.argv) == 2 and sys.argv[1] == 'syncdb':
        sys.argv.append('--noinput')

    execute_from_command_line(sys.argv)


    from django.contrib.auth.models import User
    if len(sys.argv) >= 2 and sys.argv[1] == 'syncdb':
        auto_admins = (
        		('kalyan','kalyan','kalyan@kalyan.com'),
        	)

        for admin in auto_admins:
        	username, password, email = admin
        	user = User.objects.filter(username=username)
        	if len(user) == 0:
        		print "Creating admin : %s" % username
        		User.objects.create_superuser( username, email, password )
        	