import csv, io
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCheDp61H3U49ZPCLhgHJJI6M6iqzhxsCQ"
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import mapData, schoolPerformance, UserProfile
from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from school.forms import ContactForm, SignupForm,LoginForm, UserUpdate
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from datetime import date
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

import datetime

import geocoder

# Create your views here.

#This is the view that i used to read the csv files
#this is the main data regarding each of the schools
@permission_required('admin.can_add_log_entry')
def contact_upload(request):

    prompt = {
        'order' : 'order of csv should be ...'

             }
    if request.method == "GET":
        return render(request, 'school/contact_upload.html', prompt)

    csv_file = request.FILES['file']

    #Error message if the user is not uploading a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'this aint csv')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #Geocoding and populating the longitude and latitude values in the model
        g = geocoder.google("" + column[11] + " " + column[13] + " " + column[14] + " " + column[15])
        _, created = mapData.objects.update_or_create(
            URN = column[0],
            LA = column[1],
            EstablishmentName = column[2],
            TypeOfEstablishment  = column[3],
            PhaseOfEducation = column[4],
            OfficialSixthForm = column[5],
            Gender = column[6],
            AdmissionsPolicy = column[7],
            NumberOfPupils = column[8],
            NumberOfBoys = column[9],
            NumberOfGirls = column[10],
            Street = column[11],
            Locality= column[12],
            Town = column[13],
            County = column[14],
            Postcode = column[15],
            SchoolWebsite = column[16],
            TelephoneNum = column[17],
            HeadTitle = column[18],
            HeadFirstName = column[19],
            HeadLastName = column[20],
            OfstedRating = column[21],
            Longitude = g.lng,
            Latitude = g.lat,
        )
    context = {}
    return render(request, 'school/contact_upload.html', context)


#this uploads the model that data for the league tables
@permission_required('admin.can_add_log_entry')
def performance_upload(request):

    prompt = {
        'order' : 'order of csv should be ...'

             }
    if request.method == "GET":
        return render(request, 'school/performance_upload.html', prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'this aint csv')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #checking if the mapdata has the school, if discard that row
        if(mapData.objects.filter(EstablishmentName=column[1])):
            _, created = schoolPerformance.objects.update_or_create(
                URN = column[0],
                EstablishmentName = column[1],
                Gcse_average_low  = column[2],
                Gcse_average_high = column[3],
                Average_Ebacc = column[4],
        )
    context = {}
    return render(request, 'school/performance_upload.html', context)

#home page view, this also handles the contact section at the bottom
def index(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            #django emailing, structuring the message to contain the
            #email address of the user in the message
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '    ' + 'recontact me at:' ' ' + from_email
            try:
                send_mail(subject, message, 'finalyearprojliiban@hotmail.com', ['finalyearprojliiban@hotmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "school/index.html", {'form': form})

#email success view
def success(request):
    return render_to_response('school/emailsent.html')

#this the google map view, sending the context dictionary of all objects to be displayed
#also sending the schools that have been saved on the users profile to format the add button
@login_required(login_url='/login/')
def mapdetails(request):
    mapdata1 = mapData.objects.all()
    current_user = UserProfile.objects.get(user=request.user)
    schoolsadded = current_user.list.all()

    return render(request, 'school/map.html', {'mapdata1': mapdata1, 'schoolsadded': schoolsadded})
@login_required(login_url='/login/')


#league table view sending all objects to be displayed in table
def leaguetable(request):
    tabledata = schoolPerformance.objects.all()
    return render(request, 'school/leaguetable.html', {'tabledata': tabledata})

#user object creation view
def signup_view(request):
    #checking if the user is sending the form to create account
    if request.method == 'POST':
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username'] #this gets data from the form.
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            # validation to check if the passwords match
            if password == password1:
                user, created = User.objects.get_or_create(username=username)
                if created:
                    first_name = form.cleaned_data['first_name']
                    surname = form.cleaned_data['surname']
                    email = form.cleaned_data['email']
                    user.first_name = first_name
                    user.last_name = surname
                    user.email = email
                    user.set_password(password) #saves and sets password for the user model provided by django
                    user.save()
                    user1 = UserProfile.objects.get(user=user)
                    user1.gender = form.cleaned_data['gender']
                    user1.dob = form.cleaned_data['dob']
                    user1.save()
                    return HttpResponseRedirect('/login/',{'user':user})
                #validation checks are below in the following else statements
                else:
                    messages.error(request,"User already exists")
            else:
                messages.error(request,"Password doesn't match")
        else:
            print("Form not valid")
    else:
        form = SignupForm()

    return render(request,'school/signup.html',{'form':form})

#log in view
def login_view(request):
    #POST to send data
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
            #checking to see if the username and password are same
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home') #redirects us to home page
        else:
                #messge will be displayed in the case where the account doesn't exist
            messages.error(request,"Password doesn't match or User doesn't exist")
    return render(request,'school/login.html',{'form':form})

#view used to add the school to user profile
@login_required(login_url='/login/')
def add_view(request):
    #ajax is making a post request, checking this
    if request.method == 'POST':
        current_user = UserProfile.objects.get(user=request.user)
        #sending the ID of the school from the ajax and saving it to compare with
        school_id = request.POST.get('school_id','')
        #getting the corresponding ID of the one we sent from ajax to the school in mapData model
        school = mapData.objects.get(URN=school_id)
        #adding and saving the school to the user profile
        current_user.list.add(school)
        current_user.save()
        print(school_id)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#view for deleteing a row from the user profile
#same concept for addding a row, just removing it with diff method
@login_required(login_url='/login/')
def deleteRow_view(request):
    if request.method == 'POST':
        current_user = UserProfile.objects.get(user=request.user)
        school_id = request.POST.get('school_id','')

        school = mapData.objects.get(URN=school_id)
        current_user.list.remove(school)
        current_user.save()
        print(school_id)
        return HttpResponseRedirect('/mylist')
    return HttpResponseRedirect('/mylist')

#view ofr displaying the users list,
#sending a context dictionary of the list field that has a relationship to MapData model
@login_required(login_url='/login/')
def display_mylist(request):

    current_user = UserProfile.objects.get(user=request.user)
    schools = current_user.list.all()
    return render(request, 'school/mylist.html', {'schools': schools})


#view for loggin user out
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')

#view for updating user details
@login_required(login_url='/login/')
def userUpdateDetails(request):
    if request.method == 'POST':
        #updating the user profile from the request made
        user_form = UserUpdate(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('UserUpdateSuccess')
    else:
        user_form = UserUpdate(instance=request.user)
    # sending form to the template to display the fields
    context = {'user_form': user_form,}
    return render(request, 'school/editprofile.html', context)

#view for when succesful update is made
def UserUpdateSuccess(request):
    return render_to_response('school/detailschanged.html')
