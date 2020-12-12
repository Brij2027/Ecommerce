from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core import mail 
from .models import profile
import os
import struct
import time

#global vars
email_field = ""

# Create your views here.

def signup(requests):

    context = {}

    if requests.method == 'POST':
        username = requests.POST.get('username')
        email = requests.POST.get('email')
        passwd = requests.POST.get('psswd')
        cnfpasswd = requests.POST.get('cnfpsswd')
        fname = requests.POST.get('fname')
        lname = requests.POST.get('lname')
        gender = requests.POST.get('selectgender')
        #constraints
        try:
            if passwd != cnfpasswd:
                messages.add_message(requests,messages.WARNING,"password mismatch")
                context['messges'] = messages
            else:
                user = User.objects.create_user(username=username,email=email,password=passwd)
                user.first_name = fname
                user.last_name = lname
                user.save()
                profileobj = profile.objects.create(user=user,gender=gender)
                profileobj.save()
                return render(requests,template_name = 'signin.html')
        except:
            messages.add_message(requests,messages.WARNING,"Username already exists")
            context['messges'] = messages
            

    if requests.user.is_authenticated:
        return redirect('/')
    else:
        return render(requests,template_name='signup.html',context=context)

def signin(requests):
    context = {}
    if requests.method == 'POST':
        username = requests.POST.get('username')
        passwd = requests.POST.get('psswd') 
        user = authenticate(username=username,password=passwd)
        if user is not None:
            if User.is_active:
                login(requests,user)
        else:
            messages.add_message(requests,messages.WARNING,"Invalid username or password")
            context['mssg'] = messages

    if requests.user.is_authenticated:
        return redirect('/')
    else:
        return render(requests,template_name='signin.html',context=context)

def forgot_pass(requests):
    global email_field
    if requests.method == 'POST':
        getotp = requests.POST.get('getotp')
        print("getotp",getotp)
        #forgot password page
        if getotp == "True":
            print("in true")
            while True:
                otp = struct.unpack("H",os.urandom(2))
                otp = otp[0]
                if len(str(otp)) == 4:
                    continue
                else:
                    break
            email = requests.POST.get('email')
            email_field = email
            userexist = User.objects.filter(email=email).count()
            print("usercount",userexist)
            if userexist:
                mailed = mail.send_mail("OTP","your otp is" + str(otp),'nyxkpjdk@sharklasers.com',[email])
                if mailed:
                    user_ = User.objects.get(email=email)
                    profile_user = profile(user=user_)
                    profile_user.totp = str(otp)
                    profile_user.save(update_fields=['totp'])
                    return render(requests,"otp.html",{"getotp":False})
            else:
                messages.add_message(requests,messages.WARNING,"User Not Found")
                return render(requests,"forgot_pass.html",{'messges':messages})
        #otp page
        elif getotp == "False" :
            print("in false")
            recieved_otp = requests.POST.get('otp')
            user_ = User.objects.get(email=email_field)
            print(user_)
            profile_user = profile.objects.get(user=user_)
            actual_otp = profile_user.totp
            print("received",recieved_otp,"actual",actual_otp,"otp",profile_user.gender)
            if recieved_otp == actual_otp:
                profile(user=user_).totp = 0                          #0 value set is a malpractice
                profile(user=user_).save()
                return render(requests,'change_pass.html',{"getotp" : None})
            else:
                messages.add_message(requests,messages.WARNING,"OTP Mismatched")
                return render(requests,'otp.html',{'messges':messages})

        #change_password page
        else:
            print("in None")
            passwd = requests.POST.get('psswd')
            cnfpasswd = requests.POST.get('cnfpsswd')
            if passwd != cnfpasswd:
                messages.add_message(requests,messages.WARNING,"password mismatch")
                return render(requests,'change_pass.html',{'messges':messages})
            else:
                user_ = User.objects.get(email=email_field)
                user_.set_password(passwd)
                return render(requests,'/signin/')

    return render(requests,'forgot_pass.html',{"getotp":True})



def signout(requests):
    logout(requests)
    return redirect('/')


