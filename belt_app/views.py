from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

## RENDERING

def index(request):
    return render(request, 'index.html')

def quotes(request):
    if 'user_id' in request.session:
        context = {
            'user' : User.objects.get(id = request.session['user_id']),
            'all_quotes' : Quote.objects.all().order_by("-created_at"),
        }
        return render(request, 'quotes.html', context)
    return redirect('/')

def user_profile(request, user_id):
    if 'user_id' in request.session:
        context = {
            'that_user' : User.objects.get(id=user_id),
            'user' : User.objects.get(id = request.session['user_id']),
        }
        return render(request, 'profile.html', context)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

## CREATING

def register(request):
    if request.method == 'POST':

        errors = User.objects.validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            logged_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
            request.session['user_id'] = logged_user.id
            return redirect('/quotes')
    else:
        return redirect('/')

def add_quote(request):
    if request.method == 'POST':

        errors = Quote.objects.validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
        else:
            Quote.objects.create(author = request.POST['author'], content = request.POST['content'], uploaded_by = User.objects.get(id=request.session['user_id']))
    return redirect('/quotes')

def like_quote(request, quote_id):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        this_quote = Quote.objects.get(id=quote_id)
        if this_user not in this_quote.users_who_like.all():
            this_quote.users_who_like.add(this_user)
            return redirect('/quotes')
        else:
            return redirect('/quotes')
    return redirect('/')

## UPDATING

def edit_account(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors = User.objects.update(request.POST)

            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/edit_account')
            else:
                this_user = User.objects.get(id=request.session['user_id'])
                this_user.first_name = request.POST['first_name']
                this_user.last_name = request.POST['last_name']
                this_user.email = request.POST['email']
                this_user.save()
                return redirect('/quotes')
        else:
            context = {
                'user' : User.objects.get(id=request.session['user_id']),
            }
            return render(request, 'edit_account.html', context)


## ACCESSING

def login(request):
    if request.method == 'POST':

            user = User.objects.filter(email = request.POST['email'])

            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    return redirect('/quotes')
                else:
                    messages.error(request, 'Invalid password')
                    return redirect('/')
            else:
                messages.error(request, 'Invalid email')
                return redirect('/')
    else:
        return redirect('/')

## DESTROYING

def delete_quote(request, quote_id):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        this_quote = Quote.objects.get(id=quote_id)
        if this_user == this_quote.uploaded_by:
            this_quote.delete()
        return redirect('/quotes')
    return redirect('/')