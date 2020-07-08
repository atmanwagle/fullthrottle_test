from datetime import datetime

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from fullthrottle.forms import UserForm
from fullthrottle.models import User, ActivityPeriod


# View for the main menu screen, also records the timestamp while logging in
def index(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'],
                                    password=request.POST['password'])
            request.session['id'] = user.id
            request.session['start'] = datetime.timestamp(timezone.now())
            return render(request, 'home.html')
        except:
            return render(request, 'main.html')
    return render(request, 'main.html')


# records the logging out timestamp
# making ActivityPeriod entry along with login timestamp stored in session
def logout(request):
    try:
        user = User.objects.get(id=request.session['id'])
        activity = ActivityPeriod(user=user,
                                  start_time=datetime.fromtimestamp(
                                      request.session['start']),
                                  end_time=timezone.now())
        activity.save()
        del request.session['id']
        del request.session['start']
    except:
        pass
    return render(request, 'main.html')


# view for creating a new user
def create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/fullthrottle')
            except:
                pass
    else:
        form = UserForm()
    return render(request, 'create.html', {'form': form})


# rest API with GET method to serve requested data as mentioned in the requirement
def display(request):
    response = {'ok': True}
    members = []
    userData = User.objects.all()
    for user in userData:
        activity_periods = []
        use = model_to_dict(user)
        for activity in ActivityPeriod.objects.filter(user=user.id):
            act = model_to_dict(activity)
            act.pop('id')
            act.pop('user')
            use['tz'] = act['start_time'].tzinfo.zone
            act['start_time'] = act['start_time'].strftime("%b %d %Y %I:%M:%S %p")
            act['end_time'] = act['end_time'].strftime("%b %d %Y %I:%M:%S %p")
            activity_periods.append(act)
        use.pop('username')
        use.pop('password')
        use['activity_periods'] = activity_periods
        members.append(use)
    response['members'] = members
    return HttpResponse([response], content_type="application/json")


"""
def delete(request):
    return HttpResponse("Hello, world. You're at the Delete Page.")
"""

