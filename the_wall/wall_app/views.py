from django.shortcuts import render, redirect
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user_in_db = User.objects.filter(email = request.POST['email']).first()

    print('%'*40)
    print(user_in_db)

    if user_in_db:
        messages.error(request, "Invalid cradentials")
        return redirect('/')
    
    hashed_password = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name= request.POST['fname'],
        last_name = request.POST['lname'],
        email = request.POST['email'],
        password = hashed_password
    )

    request.session['user_id'] = new_user.id

    return redirect('/success')

def success(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')

    context = {
        "user":User.objects.get(id=user_id),
        "all_messages": Message.objects.all(),
    }
    return render(request, 'success.html', context)

def login(request):
    found_user = User.objects.filter(email = request.POST['email'])
    print('&'*100)
    print(found_user)
    if len(found_user)>0:
        user_from_db = found_user[0]
        
        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(),
            user_from_db.password.encode()
        )
        if is_pw_correct:
            request.session['user_id'] = user_from_db.id
            return redirect('/success')
    messages.error(request, "Invalid cradentials")
    return redirect('/')

def new_message(request):
    errors = Message.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/success')
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')
    user_posted = User.objects.get(id=user_id)
    Message.objects.create(
        text = request.POST['message'],
        user_related = user_posted
    )
    return redirect('/success')

def new_comment(request, id):
    errors = Comment.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/success')
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')
    
    Comment.objects.create(
        text= request.POST['comment'],
        user_related = User.objects.get(id= user_id),
        message_related = Message.objects.get(id=id)
    )
    return redirect('/success')
    
def delete_message(request, id):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')
    msgdelete = Message.objects.get(id=id)
    msgdelete.delete()
    return redirect('/success')


def delete_comment(request, id):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')
    commentdelet = Comment.objects.get(id=id)
    commentdelet.delete()
    return redirect('/success')
