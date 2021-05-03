from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile,Device,DeviceTemp
from .configCalls import device
from django import forms
from django.core.validators import validate_ipv46_address, RegexValidator
from django.core import serializers
import json
from .models import DSUser
from . import adduser
from django.db.models import Q
import csv,io,os
import pathlib
from zipfile import ZipFile
import subprocess,sys,os,fabric,paramiko
import _thread
import shutil
import threading

# User login
def login_user(request):
    # Check rewquest method
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active: # Check if user is not disabled(banned)
                login(request,user)
                # pylint: disable=no-member
                allProfile = Profile.objects.filter(user=request.user) #Get all the user's profile and return them for render
                return render(request,'control/user_info.html',{'allProfile':allProfile})
            else:
                return render(request,'control/login.html',{'error_message': 'Account is disabled!'}) #Else notify them
        else:
            return render(request,'control/login.html',{'error_message': 'Account does not exist!'}) #Else notify them
    return render(request,'control/login.html') #Return login page if request method is GET

# Logout
def logout_user(request):
    logout(request) #Self explanatory
    form = UserForm(request.POST or None)
    return redirect('control:login')

# Create new user
def register(request):
    #Check request method
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid(): # Check valid form
            if request.POST['password'] == request.POST['password_confirm']:
                user = form.save(commit=False) #Temporary save the form 
                #clean the form
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save() #Save to database
                user = authenticate(username=username, password = password) #Authenticate the user
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return redirect('control:index')
            else:
                return render(request,'control/register.html',{'confirm_error':'Confirm password does not match'}) #Return error code
        return render(request,'control/register.html',{'form':form}) #Return if form is invalid
    else:
        logout(request) #logout and return to register page if request method is GET
        return render(request,'control/register.html')

# Profile is what used to access ssh
def make_profile(request):
    if not request.user.is_authenticated:
        return redirect('control:login') #Redirect user to login page if not already logged in
    else:
        if request.method == 'POST': #Check request method
            # pylint: disable=no-member
            allProfile = Profile.objects.filter(user=request.user) #Get all profiles that belong to the user
            form = ProfileForm(request.POST)
            if form.is_valid():# Check form
                profile = form.save(commit=False) # Temporary save the form
                profile.user = request.user
                profile.save() #Save to the database
                return render(request,'control/user_info.html',{'allProfile':allProfile}) #Return to the user's info page
            return render(request,'control/create_profile.html',{'form':form}) #Return if form is invalid
    return render(request,'control/create_profile.html') #Return this page if request method is GET

#Main page
def index(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
        # pylint: disable=no-member
    allProfile = Profile.objects.filter(user=request.user)
    return render(request,'control/user_info.html',{'allProfile':allProfile})


#Discover devices using CDP
def discover_form(request):
    if not request.user.is_authenticated:
       return redirect('control:login') 
    # pylint: disable=no-member
    allProfiles = Profile.objects.filter(user=request.user)
    return render(request,'control/discover.html',{'allProfiles':allProfiles})

def discover(request):
    if not request.user.is_authenticated:
        return redirect('control:login')#Redirect user to login page if not already logged in
        # pylint: disable=no-member
    form = request.POST
    try:
        # validate_ipv46_address(form['Target'])
        profile = get_object_or_404(Profile,pk=form['profile'])
        DeviceTemp.objects.all().delete()
        target = device(form['Target'],22,profile.profileName,profile.profilePassword,profile.profileEnablePassword,'ios') #create a class to begin ssh
        try:
            deviceList_output = target.discover() #Begin discover
            for each in deviceList_output:
                hostname = each['destination_host'] = each['destination_host'].split('.')[0] #Extract device's hostname from FQDN
                deviceType = ''
                if each['software_version'].split(',')[0] == 'Cisco IOS Software':
                    deviceType = 'cisco_ios'
                a = DeviceTemp(hostname=hostname,managementIP=each['management_ip'],localPort=each['local_port'],remotePort=each['remote_port'],platform = each['platform'],softwareVersion=each['software_version'],deviceType=deviceType,capabilities=each['capabilities'])
                a.save()
            print(json.dumps(deviceList_output,indent=4))
            deviceList = DeviceTemp.objects.filter(user=request.user)
            allProfiles = Profile.objects.filter(user=request.user)
            context = {'deviceList':deviceList,
                        'allProfiles':allProfiles}
            return render(request,'control/discover.html',context=context)
        except Exception as e:
            print(e)
            allProfiles = Profile.objects.filter(user=request.user)
            context = {'allProfiles':allProfiles,
                        'timeout_error_message':'Timeout !'}
            return render(request,'control/discover.html',context=context)
    except ValueError as e:
        print(e)
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
    device = Device(user=request.user,hostname=device_temp.hostname,managementIP=device_temp.managementIP,localPort=device_temp.localPort,remotePort=device_temp.remotePort,platform =device_temp.platform,softwareVersion=device_temp.softwareVersion,deviceType=device_temp.deviceType,capabilities=device_temp.capabilities)
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
            # pylint: disable=no-member
            profile.profileName = form.cleaned_data['profileName']
            profile.profilePassword = form.cleaned_data['profilePassword']
            profile.profileEnablePassword = form.cleaned_data['profileEnablePassword']
            profile.save()
            return redirect('control:account_info')
        try:
            if request.POST['primary']:
                profile = get_object_or_404(Profile, pk=profile_id)
                allProfiles = Profile.objects.filter(user=request.user)
                for item in allProfiles:
                    item.primary = False
                    item.save()
                profile.primary = True
                profile.save()
        except:
            pass
    return redirect('control:account_info')

def diviceList(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    else:
        # pylint: disable=no-member
        allDevices = Device.objects.filter(user=request.user)
        allProfiles = Profile.objects.filter(user=request.user)
        # allDevices_json = json.loads(serializers.serialize('json',allDevices))
        # profile = Profile.objects.get(primary=True)
        # deviceList = []
        # for item in allDevices_json:
        #     networkDevice = device(item['fields']['managementIP'],22,profile.profileName,profile.profilePassword,profile.profileEnablePassword,'ios')
        #     if networkDevice.checkStatus()['is_alive']:
        #         item['fields']['status'] = 'up'
        #     deviceList.append(item['fields'])
        return render(request,'control/device_list.html',{'allDevices':allDevices,'allProfiles':allProfiles})

def remove_device(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    else:
        form=request.POST
        device_id = form['device_id']
        device = get_object_or_404(Device,pk=device_id)
        device.delete()
        return redirect('control:device_list')

def deviceDetail(request,device_id):
    if not request.user.is_authenticated:
        return redirect('control:login')
    else:
        try:
            device = get_object_or_404(Device,pk=device_id)
        except Exception as e:
            print(e)
        return render(request,'control/device_details.html', {'device':device})

def getInterfaceStatus(request,device_id):
    querySet = get_object_or_404(Device,pk=device_id)
    # pylint: disable=no-member
    profile = Profile.objects.get(primary=True)
    networkDevice = device(querySet.managementIP,22,profile.profileName,profile.profilePassword,profile.profileEnablePassword,'ios')
    intStat_ip, intStat = networkDevice.getInterfaceInfo()
    return intStat_ip, intStat

def getDeviceInfo(request,device_id):
    querySet = get_object_or_404(Device,pk=device_id)
    # pylint: disable=no-member
    profile = Profile.objects.get(primary=True)
    networkDevice = device(querySet.managementIP,22,profile.profileName,profile.profilePassword,profile.profileEnablePassword,'ios')
    return networkDevice.getDeviceFact()


def getDeviceInfoAPI(request,device_id):
    try:
        querySet = get_object_or_404(Device,pk=device_id)
        print(querySet.deviceType)
        # pylint: disable=no-member
        profile = Profile.objects.get(primary=True)
        response = []
        # networkDevice = device(querySet.managementIP,22,profile.profileName,profile.profilePassword,profile.profileEnablePassword,'ios')
        # print(profile.profileEnablePassword)
        networkDevice = device(querySet.managementIP,22,profile.profileName,profile.profilePassword,'cisco','ios')
        intStat_ip, intStat = networkDevice.getInterfaceInfo()
        fact = networkDevice.getDeviceFact()
        response = []
        response.append(intStat)
        response.append(intStat_ip)
        response.append(fact)
        querySet.hostname = fact['hostname']
        querySet.save()
    except Exception as e:
        print(e)
    return JsonResponse(response,safe=False)

def change_MgmtIP(request,device_id):
    if request.method == 'POST':
        form=request.POST
        try:
            validate_ipv46_address(form['new_IP'])
            device = get_object_or_404(Device,pk=device_id)
            device.managementIP = form['new_IP']
            device.save()
            return redirect('control:device_detail', device_id)
        except Exception as e:
            print(e)
            return redirect('control:device_detail', device_id)
    return redirect('control:device_detail', device_id)

def addUserPage(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    if checkDomain() != True:
        return redirect('control:block')
    allUser = DSUser.objects.all()
    ouList = adduser.getOU()
    domain = adduser.getDomain()
    context = {
        'allUser':allUser,
        'ouList':ouList,
        'domain':domain
    }
    
    if request.method == 'POST':
        status = adduser.addUser(request.POST['cn'],request.POST['ou'],request.POST['dc'],request.POST['password'])
        print(type(status))
        print(status == 0)
        if status == 0:
            a = DSUser(cn=request.POST['cn'],ou=request.POST['ou'],dc=request.POST['dc'],password=request.POST['password'])
            a.save()
        else:
            context = {'error_message': "Can't create user"}
            return render(request,'control/domain_user_list.html',context)
    return render(request,'control/domain_user_list.html',context)

def addCSVpage(request):
    if checkDomain() != True:
        return redirect('control:block')
    extension = 'csv'
    if request.method == 'POST':
        counter = 0
        failedUser = []
        myfile = request.FILES['file']
        fileType = myfile.name.split('.')[-1]
        if fileType != 'csv':
            allUser = DSUser.objects.all()
            ouList = adduser.getOU()
            domain = adduser.getDomain()
            context = {
                'allUser':allUser,
                'ouList':ouList,
                'domain':domain,
                'CSV_error_message':'Use *.csv'
                }
            return render(request,'control/domain_user_list.html',context)
        file = myfile.read().decode('utf-8')
        reader = csv.reader(io.StringIO(file))
        for item in reader:
            print(item[0])
            status = adduser.addUser(item[0],item[1],item[2],item[3])
            print(status)
            if status == 0:
                a = DSUser(cn=item[0],ou=item[1],dc=item[2],password=item[3])
                a.save()
            else:
                counter=counter+1
                failedUser.append(item[0])
        if counter>0:
            context = {
                'counter':counter,
                'failed_users':failedUser
            }
            return render(request,'pages/uploadCSV.html',context)
        return redirect('control:userList')
    return redirect('control:userList')

def DSUserList(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    if checkDomain() != True:
        return redirect('control:block')
    allUser = DSUser.objects.all()
    ouList = adduser.getOU()
    domain = adduser.getDomain()
    context = {
        'allUser':allUser,
        'ouList':ouList,
        'domain':domain
    }
    return render(request,'control/domain_user_list.html',context)

def shareFile(request):
    if checkDomain() != True:
        return redirect('control:block')
    
    if request.method == 'POST':
        myfile = request.FILES['file']
        file_name = default_storage.save(myfile.name, myfile)
        path = 'C:\\Home_folders'
        homeContents = os.listdir(path)
        for item in homeContents:
            if os.path.isdir(path + '\\' + item):
                shutil.copy('share\\'+myfile.name,path+'\\'+item)
        return render(request,'pages/shareFiles.html')
    return render(request,'pages/shareFiles.html')

# def userList(request):
#     if checkDomain() != True:
#         return redirect('control:block')
#     allUser = DSUser.objects.all()
#     context = {'allUser':allUser}
#     return render(request,'pages/userList.html',context)

def promoteDomain(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    # if checkDomain() == True:
    #     return redirect('control:promoted')
    if request.method == 'POST':
        try:
            validate_ipv46_address(request.POST['host'])
            host = request.POST['host']
            domain = request.POST['domain_name']
            NetbiosName = request.POST['net_name']
            safeModePass = '='+request.POST['safe_pass']
            profile = get_object_or_404(Profile,pk=request.POST['profile'])
            sshUsername = profile.profileName
            sshPassword = profile.profilePassword
            var = f'''
            Add-WindowsFeature RSAT-AD-Tools
            Add-WindowsFeature -Name "ad-domain-services" -IncludeAllSubFeature -IncludeManagementTools
            Add-WindowsFeature -Name "dns" -IncludeAllSubFeature -IncludeManagementTools 
            Add-WindowsFeature -Name "gpmc" -IncludeAllSubFeature -IncludeManagementTools
            REG ADD HKLM\Software\FTCAD /v Data /t Reg_SZ /d "Installed"
            $domainname = "{domain}" 
            $netbiosName = "{NetbiosName}" 
            $safemodepassword = "{safeModePass}" | ConvertTo-SecureString -AsPlainText -Force
            Import-Module ADDSDeployment
            Install-ADDSForest -DomainName $domainname -SafeModeAdministratorPassword $safemodepassword -InstallDns:$True -Force:$True
            '''
            with open('dcinstall.ps1','w') as f:
                f.write(var)
            cwd = os.getcwd()
            try:
                _thread.start_new_thread(runShell,(cwd,host,sshUsername,sshPassword,))
                context={
                'message':'Thiet bi se duoc khoi dong lai trong vai phut',
                'allProfiles':allProfiles
                }
                return render(request,'control/promoteDomain.html',context)
            except Exception as e:
                print(e)
            allProfiles = Profile.objects.filter(user=request.user)
            context={
                'allProfiles':allProfiles
            }
            return render(request,'control/promoteDomain.html',context)
        except Exception as e:
            print(e)
    allProfiles = Profile.objects.filter(user=request.user)
    return render(request,'control/promoteDomain.html',{'allProfiles': allProfiles})

def updateDSUser(request,user_id):
    if not request.user.is_authenticated:
        return redirect('control:login')
    if checkDomain() != True:
        return redirect('control:block')
    user = DSUser.objects.get(pk=user_id)
    if request.method == 'POST':
        # print(request.POST['enabled']==None)
        try:
            status = adduser.modUser(user.cn,user.ou,user.dc,request.POST['password'],request.POST['enabled'])
            if status == 0:
                user.password = request.POST['password']
                user.enabled=True
                user.save()
        except:
            status = adduser.modUser(user.cn,user.ou,user.dc,request.POST['password'],'false')
            if status == 0:
                user.password = request.POST['password']
                user.enabled=False
                user.save()
        return redirect('control:DSUserList')

    return render(request,'control/updateDSUser.html',{'DSuser':user})

def makeOU(request):
    if checkDomain() != True:
        return redirect('control:block')
    result = subprocess.check_output('wmic.exe ComputerSystem get Domain')
    domain = result.decode('utf-8').split('\n')[1]
    context = {
            "domain":domain,
        }
    if request.method == 'POST':
        ou = request.POST['ou']
        status = adduser.addOU(ou,domain)
        return render(request,'control/addOU.html',context)
    return render(request,'control/addOU.html',context)

def removeUser(request):
    user = DSUser.objects.get(pk=request.POST['user_id'])
    status = adduser.deleteUser(user.cn,user.ou,user.dc)
    if status == 0:
        user.delete()
    return redirect('control:DSUserList')

def findUser(request):
    query = request.GET.get('q')
    print(query)
    allUser = DSUser.objects.filter(Q(cn__icontains=query) |
                Q(ou__icontains=query)|Q(dc__icontains=query)).distinct()
    print(allUser)
    ouList = adduser.getOU()
    domain = adduser.getDomain()
    context = {
        'allUser':allUser,
        'ouList':ouList,
        'domain':domain
    }
    return render(request,'control/domain_user_List.html',context)

def block(request):
    return render(request,'control/block.html')

def promoted(request):
    return render(request,'control/promoted.html')

def runShell(cwd,host,username,password):
    print(f'{username}@{host}')
    client = fabric.Connection(f'{username}@{host}',connect_kwargs={'password':password})
    with open(cwd+'\\dcinstall.ps1') as f:
        client.run('echo > DCinstall.ps1')
        for line in f:
            scriptLine = line.strip(' ').strip('\n')
            cmd = f'''echo '{scriptLine}' >> DCinstall.ps1'''
            print(cmd)
            client.run(cmd)
    os.system(f'putty.exe -ssh {username}@{host} -pw {password} -m '+cwd+'\\aaa.txt')
    # try:
    #     # fabric.operations.put(cwd+'\\dcinstall.ps1', '', use_sudo=True,mirror_local_mode=False,mode=None)
    # except Exception as e:
    #     print(e)
    # with open(cwd+'\\dcinstall.ps1') as f:
    #     client.run('whoami')
    #     for line in f:
    #         client.(line.strip(' '),pty=True)
            
    # p = subprocess.Popen(["powershell.exe", cwd + "\\dcinstall.ps1"])
    # p.communicate()
    
def checkDomain():
    result = subprocess.check_output('wmic.exe ComputerSystem get DomainRole')
    role = result.decode('utf-8').split('\n')[1]
    if int(role) == 5:
        return True
    return False

def manual_config_form(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    form = request.POST
    threads = []
    try:
        for id in form.getlist('device'):
            querySet = get_object_or_404(Device,pk=id)
            profile = get_object_or_404(Profile,pk=form['profile'])
            networkDevice = device(querySet.managementIP,22,profile.profileName,profile.profilePassword,profile.profileEnablePassword,querySet.deviceType)
            
            t = threading.Thread(target=networkDevice.manual_config,args=[form['config']])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
    except Exception as e:
        print(e)      
    return(redirect('control:device_list'))

def create_config(request):
    if not request.user.is_authenticated:
        return redirect('control:login')
    return render(request,'control/configure_mainpage.html')