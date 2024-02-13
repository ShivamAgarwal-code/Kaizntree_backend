from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
# from .models import User
from validate_email import validate_email
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from itemDashboard.views import display_items

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

@csrf_exempt
def signup(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(pass1) < 6:
            messages.add_message(request, messages.ERROR,
                                            'Password should be at least 6 characters')
            context['has_error'] = True

        if pass1 != pass2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Enter a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            context['has_error'] = True

            return render(request, 'authentication/signup.html', context, status=409)

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True

            return render(request, 'authentication/signup.html', context, status=409)
        
        if context['has_error']:
            return render(request, 'authentication/signup.html', context)

        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname

        user.save()

        if not context['has_error']:        
            # send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                    'Your account has been created successfully.')           

            return redirect('home')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username = username, password = pass1)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials, try again')
            return render(request, 'authentication/index.html', status=401)

        login(request, user)
        fname = user.first_name
        
        token, _ = Token.objects.get_or_create(user=user)

        # Add tokens to the response
        response_data = {
            'username': user.username,
            'token': token.key,
            'fname': fname
        }
        # return render(request, 'authentication/index.html', response_data)     
        return redirect(display_items, fname=fname)

    return render(request, "authentication/index.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')