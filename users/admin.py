from django.contrib import admin
from users.models import User, UserConfirmation, Profile
from django.contrib.auth.models import Group

admin.site.unregister(Group)


admin.site.register(User)
admin.site.register(UserConfirmation)
admin.site.register(Profile)