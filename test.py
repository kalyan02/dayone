from do.models import *
User = auth.models.User
u=User.objects.get(pk=2)
ff = Status.factory(u)
