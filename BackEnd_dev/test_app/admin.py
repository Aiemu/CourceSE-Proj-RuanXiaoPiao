from django.contrib import admin

from test_app.models import User, Activity, Ticket

# Register your models here.
admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Ticket)