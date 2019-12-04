from django.contrib import admin

from test_app.models import User, Activity, Ticket, HeatMode

# Register your models here.
admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Ticket)
admin.site.register(HeatMode)