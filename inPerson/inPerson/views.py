from django.shortcuts import render
from schedule.models import Schedule
from schedule.serializers import SchedulesSerializer
from django.contrib.auth import get_user_model

CURRENT_TERM = "S2019"

def menu_view(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    schedule = Schedule.objects.filter(owner=request.user, term=CURRENT_TERM)
    create_user(request.user.username)
    if schedule.count() == 0:
        s = Schedule.objects.create(owner=request.user, term=CURRENT_TERM)
        s.save()
        serializer = SchedulesSerializer(s)
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

# create a user if not already present
def create_user(username):
    User = get_user_model()
    # information is 1) login system 2) university 3) netid
    info = username.split("-")
    if not User.objects.filter(netid=info[2]).exists():
        User.objects.create(netid=info[2], university=info[1])
        print("just created user")
        return 1
    return 0
