from .models import User, Activity, Ticket

dailydecrease = 1.0

def heatDecrease():
    actList = Activity.objects.all()
    for item in actList:
        item.heat -= dailydecrease