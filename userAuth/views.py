from django.shortcuts import render, redirect
from .forms import CreateUserForm
from devdoot.models import Cities, States, ProblemType
from devdoot.models import ExtendedUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import close_old_connections


# from django.views.decorators.csrf import csrf_exempt

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            # print(username, password, user, request.POST)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        close_old_connections()

        return render(request, 'login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# @csrf_exempt
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        form.fields['username'].widget.attrs['onKeyPress'] = "if(this.value.length==10) return false;"
        form.fields['username'].widget.attrs['maxlength'] = '10'
        form.fields['username'].widget.attrs['type'] = 'tel'
        form.fields['username'].widget.attrs['placeholder'] = 'Enter 10 digit mobile number'
        form.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        form.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        form.fields['first_name'].widget.attrs['autofocus'] = 'True'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        form.fields['password1'].widget.attrs['placeholder'] = 'Ex. Pass@1234'
        form.fields['password2'].widget.attrs['placeholder'] = 'Re-Enter password'
        form.fields['username'].widget.attrs[
            'oninput'] = "this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');"

        # print(request.method)

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid() and request.POST.get('password1') == request.POST.get('password2'):
                try:
                    username_available = User.objects.get(username=request.POST.get('username'))
                    messages.info(request, 'Mobile number is already registered', extra_tags='alert-success')

                    email_present = User.objects.get(email=request.POST.get('email'))
                    messages.info(request, 'Mobile number is already registered', extra_tags='alert-success')

                    error_msg = 'Mobile number or email is already registered'
                    return render(request, 'login/register.html', {'error_msg': error_msg})

                except User.DoesNotExist:
                    username = form.cleaned_data.get('username')

                    if len(username) < 10:
                        messages.warning(request, 'Enter Valid Mobile Number', extra_tags='alert-success')

                    # print(username)
                    # userref = User.objects.get(username=username).pk

                    state1 = request.POST.get('state') if request.POST.get('state') != "" else 0
                    city1 = request.POST.get('city') if request.POST.get('city') != "" else 0
                    gender1 = request.POST.get('gender') if request.POST.get('gender') != "" else 0
                    account_type1 = request.POST.get('account_type') if request.POST.get('account_type') != "" else 0
                    address1 = request.POST.get('address') if request.POST.get('address1') != "" else 0
                    profession1 = request.POST.get('profession') if request.POST.get('profession') != "" else 0
                    group_name1 = request.POST.get('groupname') if request.POST.get('groupname') != "" else None
                    problem_types1 = request.POST.getlist('problemtypes[]')
                    if len(problem_types1) > 0:
                        problem_types1 = json.dumps(problem_types1)
                    else:
                        problem_types1 = None
                    # if any(state1, city1, gender1, account_type1, address1, profession1):
                    # print(state1, city1, gender1, account_type1, address1, profession1)

                    if state1 and city1 and gender1 and account_type1 and address1 and profession1:
                        userref = form.save()
                        state_instance = States.objects.get(id=state1)
                        city_instance = Cities.objects.get(id=city1)
                        extuser = ExtendedUser(user=userref, state=state_instance, city=city_instance, gender=gender1,
                                               account_type=account_type1, address=address1, profession=profession1,
                                               group_name=group_name1, problem_types=problem_types1)
                        extuser.save()
                        messages.success(request, 'Account created successfully for ' + username,
                                         extra_tags='alert-success')

                        return redirect('login')
                    else:
                        messages.info(request, 'Please fill valid details', extra_tags='alert-success')

            else:
                messages.info(request, 'Please fill valid details')
        states = States.get_all_states()
        all_problems = ProblemType.objects.all()
        context = {'form': form, 'states': states, 'all_problems': all_problems}
        close_old_connections()

        return render(request, 'login/register.html', context)


def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = Cities.objects.filter(state_id=state_id).order_by('name')
    close_old_connections()

    return render(request, 'login/cities.html', {'cities': cities})


def forgotPage(request):
    context = {}
    return render(request, 'forgot.html', context)


@login_required(login_url='login')
def resetPage(request):
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('oldpassword')

        newpass1 = request.POST.get('newpassword1')
        newpass2 = request.POST.get('newpassword2')
        if newpass1 == newpass2:
            user = authenticate(request, username=username, password=password)
            messages.info(request, 'Please enter your old password correctly')

            # print(username, password, user, request.POST)
            if user is not None:
                user.set_password(newpass1)
                user.save()
                messages.info(request, 'Now login with your new password')
                return redirect('/')
        else:
            messages.info(request, 'Make sure you entered new password correctly')
    context = {}
    close_old_connections()

    return render(request, 'login/password_change.html', context)
