from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from classroom_reservation_app.EmailBackEnd import EmailBackEnd
from django.contrib import messages

# Create your views here.

def ShowLoginPage(request):
    return render(request, "login_page.html")

def doLogin(request):
    if request.method !="POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1": #SI C UN ADMIN
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":# SI C UN PROF
                return HttpResponseRedirect("/staff_home")
            else:
                return HttpResponseRedirect("/student_home")

        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("login/")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login/")