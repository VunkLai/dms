from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def sign_in(request):
    # pylint:disable=broad-except,too-many-return-statements
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'server/sign_in.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            content = {'error': 'Username already exists'}
            return render(request, 'server/sign_in.html', content)
        if username not in settings.HRS:
            content = {'error': f'Username: {username} is invalid'}
            return render(request, 'server/sign_in.html', content)
        try:
            User.objects.create_user(
                username=username,
                password=password,
                email=f'{username}@{settings.FQDN}')
            # if user.username in settings.HRS:
            #     group = auth.Group.objects.get(name='HR')
            #     user.groups.add(group)
            return HttpResponseRedirect('/login/')
        except Exception as e:
            return HttpResponse(str(e), code=400)
    return HttpResponse('Method Not Allowed', code=405)


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'server/login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        content = {'error': 'Forbidden'}
        return render(request, 'server/login.html', content)
    return HttpResponse('Method Not Allowed', code=405)


def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    auth.logout(request)
    return HttpResponseRedirect('/')


def home(request):
    return HttpResponse('home')


@login_required(login_url='/login/')
def hello_world(request):
    return HttpResponse(f'hello {request.user.username}')
