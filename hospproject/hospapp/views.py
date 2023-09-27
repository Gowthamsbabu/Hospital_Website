from django.shortcuts import render, redirect
from django.http import HttpResponse


from .models import Departments, Doctors
from .forms import BookingForm, RegistrationForm

from django.contrib import messages, auth
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login

# Create your views here.
def index(request):
    person = {
        'name': 'John',
        'age': 30,
        'place': 'Calicut'
    }
    
    return render(request, 'index.html', person)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # Redirect to a different page after successful login
            return redirect('home')  # Replace 'dashboard' with your desired URL name
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Bind the form with POST data

        if form.is_valid():
            username = form.cleaned_data['patient_name']  # Use the form field name
            password = form.cleaned_data['password']
            cpassword = form.cleaned_data['password1']

            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    auth_login(request, user)  # Log in the user immediately after registration
                    # Redirect to a different page after successful registration
                    return redirect('home')  # Replace 'home' with your desired URL name
            else:
                messages.info(request, "Passwords do not match")
        else:
            messages.error(request, "Invalid registration data. Please try again.")
    else:
        form = RegistrationForm()  # Create a new empty form for GET requests
    
    return render(request, "register.html", {'form': form})




def logout(request):
    auth.logout(request)
    return redirect('/')


def about(request):
    return render(request, 'about.html')

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'confirmation.html') 
    form =BookingForm()
    dict_form={
        'form': form
    }
    return render(request, 'booking.html', dict_form)

def doctors(request):
    dict_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request, 'doctors.html', dict_docs)

def contact(request):
    return render(request, 'contact.html')

def department(request):
    dict_dept={
        'dept': Departments.objects.all()
    }
    return render(request, 'department.html', dict_dept)

