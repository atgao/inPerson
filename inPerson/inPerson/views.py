from django.shortcuts import render
from schedule.models import Schedule
from schedule.serializers import SchedulesSerializer

CURRENT_TERM = "S2019"

def menu_view(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    schedule = Schedule.objects.filter(owner=request.user, term=CURRENT_TERM)
    if schedule.count() == 0:
        s = Schedule.objects.create(owner=request.user, term=CURRENT_TERM)
        s.save()
        serializer = SchedulesSerializer(s)
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')