  # -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from skipass.forms import  UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from skipass.models import  UserProfile
import stripe
import gda_test_project.settings

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage':'Hey Hey'}
    return render_to_response('skipass/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    return render_to_response('skipass/about.html', {}, context)

def register(request):
    context = RequestContext(request)

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered=True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form':user_form, 'profile_form':profile_form,
                    'registered':registered}
    return render_to_response('skipass/register.html', context_dict, context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/skipass/')
        else:
            return HttpResponse('არასწორი მონაცემები')
    else:
        return render_to_response('skipass/login.html',{},context)

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/skipass/')

@login_required
def user_balance(request):
    context = RequestContext(request)
    context_dict ={}
    try:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['user'] = request.user
        context_dict['profile'] = profile
    except UserProfile.DoesNotExist:
        pass

    return render_to_response('skipass/balance.html',context_dict,context)

@login_required
def payment(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method=='POST':
        context_dict['days'] = request.POST['days']
        amount = request.POST['amount']
        context_dict['amount'] = amount

        try:
            profile = UserProfile.objects.get(user=request.user)
            context_dict['user'] = request.user
            context_dict['profile'] = profile
            balance_after = str(profile.balance + int(amount))
            context_dict['balance_after'] = balance_after
        except UserProfile.DoesNotExist:
            pass

    return render_to_response('skipass/payment.html',context_dict,context)

@login_required()
def charge_card(request):
    context = RequestContext(request)

    charged = False

    stripe.api_key = 'sk_test_lXShtSPE6dS9qTY4skH8rUmr'
    if request.method =='POST':
        token = request.POST['stripeToken']
        amount_to_charge = int(request.POST['amount'])
        days_to_add = int(request.POST['days'])
        amount_to_charge_cents = amount_to_charge * 100
        if amount_to_charge > 100:
            #do not charge more than 100USD accidentally
            return HttpResponse('Error: too much money')

    # get user and his/her profile
    try:
        profile = UserProfile.objects.get(user=request.user)
        user = request.user
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        pass

    try:
        charge = stripe.Charge.create(
            amount=amount_to_charge_cents, # amount in cents, again
            currency="usd",
            card=token,
            description=user.email)
        charged = True
        profile.balance += amount_to_charge
        profile.days_left += days_to_add
        profile.save()
        return HttpResponseRedirect('/skipass/balance/')

    except  (stripe.CardError,stripe.InvalidRequestError):
        return HttpResponse("unsuccessful")


