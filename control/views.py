from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile,Device,DeviceTemp
from .configCalls import device
from django import forms
import json
from django.core.validators import validate_ipv46_address, RegexValidator
# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                # pylint: disable=no-member
                allProfile = Profile.objects.filter(user=request.user)
                return render(request,'control/user_info.html',{'allProfile':allProfile})
            else:
                return render(request,'control/login.html',{'error_message': 'Account is disabled!'})
        else:
            return render(request,'control/login.html',{'error_message': 'Account does not exist!'})
    return render(request,'control/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return redirect('control:login')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['password_confirm']:
                user = form.save(commit=False)
                username = form.cleaned_data['username']
                print(username)
                password = form.cleaned_data['password']
                print(password)
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password = password)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return redirect('control:index')
            else:
                return render(request,'control/register.html',{'confirm_error':'Confirm password does not match'})
        return render(request,'control/register.html',{'form':form})
    else:
        logout(request)
        return render(request,'control/register.html')

def make_profile(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    else:
        if request.method == 'POST':
            # pylint: disable=no-member
            allProfile = Profile.objects.filter(user=request.user)
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return render(request,'control/user_info.html',{'allProfile':allProfile})
            return render(request,'control/create_profile.html',{'form':form})
    return render(request,'control/create_profile.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
        # pylint: disable=no-member
    allProfile = Profile.objects.filter(user=request.user)
    return render(request,'control/user_info.html',{'allProfile':allProfile})

def discover_form(request):
    if not request.user.is_authenticated:
       return redirect('control:login')
    # pylint: disable=no-member
    allProfiles = Profile.objects.filter(user=request.user)
    return render(request,'control/discover.html',{'allProfiles':allProfiles})

def discover(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
        # pylint: disable=no-member
    form = request.POST
    try:
        validate_ipv46_address(form['Target'])
        profile = get_object_or_404(Profile,pk=form['profile'])
        DeviceTemp.objects.all().delete()
        target = device(form['Target'],22,profile.profileName,profile.profilePassword)
        try:
            deviceList_output = target.discover()
            for each in deviceList_output:
                hostname = each['destination_host'] = each['destination_host'].split('.')[0]
                deviceType = ''
                if each['software_version'].split(',')[0] == 'Cisco IOS Software':
                    deviceType = 'cisco_ios'
                a = DeviceTemp(hostname=hostname,managementIP=each['management_ip'],localPort=each['local_port'],remotePort=each['remote_port'],platform = each['platform'],softwareVersion=each['software_version'],deviceType=deviceType)
                a.save()
            # print(json.dumps(deviceList_output,indent=4))
            deviceList = DeviceTemp.objects.filter(user=request.user)
            allProfiles = Profile.objects.filter(user=request.user)
            context = {'deviceList':deviceList,
                        'allProfiles':allProfiles}
            return render(request,'control/discover.html',context=context)
        except:
            allProfiles = Profile.objects.filter(user=request.user)
            context = {'allProfiles':allProfiles,
                        'timeout_error_message':'Timeout !'}
            return render(request,'control/discover.html',context=context)
    except ValueError as e:
        allProfiles = Profile.objects.filter(user=request.user)
        context = {'allProfiles':allProfiles,
                    'profile_error_message':'Choose a profile'}
        return render(request,'control/discover.html',context=context)
    except Exception as e:
        allProfiles = Profile.objects.filter(user=request.user)
        print(e)
        context = {'allProfiles':allProfiles,
                    'IP_error_message':'Enter a valid IP address'}
        return render(request,'control/discover.html',context=context)
    

def add_discovered(request):
    form = request.POST
    device_temp = get_object_or_404(DeviceTemp,pk=form['device_id'])
    device = Device(user=request.user,hostname=device_temp.hostname,managementIP=device_temp.managementIP,localPort=device_temp.localPort,remotePort=device_temp.remotePort,platform =device_temp.platform,softwareVersion=device_temp.softwareVersion,deviceType=device_temp.deviceType)
    device.save()
    device_temp.delete()
    # pylint: disable=no-member
    allProfiles = Profile.objects.filter(user=request.user)
    deviceList = DeviceTemp.objects.filter(user=request.user)

    print(device)
    context = {'deviceList':deviceList,
                'allProfiles':allProfiles}
    return render(request,'control/discover.html',context=context)

def account_info(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    # pylint: disable=no-member
    allProfile = Profile.objects.filter(user=request.user)
    return render(request,'control/user_info.html',{'allProfile':allProfile})

def delete_profile(request, profile_id):
    if not request.user.is_authenticated:
        return redirect('control:login')
    # pylint: disable=no-member
    profile = Profile.objects.get(pk=profile_id)
    profile.delete()
    return redirect('control:account_info')

def update_profile_form(request, profile_id):
    if not request.user.is_authenticated:
        return redirect('control:login')
    # pylint: disable=no-member
    profile = get_object_or_404(Profile, pk=profile_id)
    if profile.user == request.user:
        return render(request,'control/update_profile.html',{'profile':profile})
    return HttpResponseForbidden('<h1>Access denied</h1>')

def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        return redirect('control:account_info')
    else:
        # pylint: disable=no-member
        allProfiles = Profile.objects.filter(user=request.user)
        return render(request,'control/user_info.html',{'form':form,'allProfile':allProfiles})


def change_profile(request,profile_id): 
    if not request.user.is_authenticated:
        return redirect('control:login')
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, pk=profile_id)
            profile.profileName = form.cleaned_data['profileName']
            profile.profilePassword = form.cleaned_data['profilePassword']
            profile.profileEnablePassword = form.cleaned_data['profileEnablePassword']
            profile.save()
            return redirect('control:account_info')
    return redirect('control:account_info')