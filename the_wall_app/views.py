from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager, Posted_Message, Posted_Comment
import bcrypt

def index(request):
    return render(request, 'index.html')

#Create/register a new user_________________________________
def register_user(request):
    if request.method == "POST":
        #validation before saving to DB
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/') 

        #hash the password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()
        ).decode()
        
        #create user
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            dob = request.POST['dob'],
            email = request.POST['email'],
            password = hashed_pw
        ) 
        #create a session
        request.session['logged_user'] = new_user.id
        return redirect("/wall")
    return redirect('/')    

#Login user_________________________________
def login_user(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        this_user = User.objects.filter(email=request.POST['email'])
        if this_user:
            log_user = this_user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()): 
                request.session['logged_user'] = log_user.id  
                return redirect('/wall')
            messages.error(request, "email or password are incorrect.")
    return redirect('/')

#Wall_________________________________
def wall(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'wall_messages': Posted_Message.objects.all()
    }
    return render(request, 'wall.html', context)

#Post message:
def post_message(request):
    Posted_Message.objects.create(
        message = request.POST['post_message'],
        posted_by = User.objects.get(id=request.session['logged_user'])
    )
    return redirect('/wall')

#Messages_________________________________
#Post comment:
def post_comment(request, post_id):
    posted_by = User.objects.get(id=request.session['logged_user'])
    message = Posted_Message.objects.get(id=post_id)
    Posted_Comment.objects.create(
        comment = request.POST['post_comment'],
        posted_by = posted_by, 
        posted_message = message
    )
    return redirect('/wall')

#Comments and comment update/delete__________________
#Edit comment:
def edit_comment(request, comment_id):
    context = {
        "edit_comment": Posted_Comment.objects.get(id=comment_id)
    }
    return render(request, 'edit_comment.html', context)
    # return redirect('/wall')

#Update comment:
def update_comment(request, comment_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    comment = Posted_Comment.objects.get(id=comment_id)
    comment.comment = request.POST['post_comment']
    comment.save()
    return redirect('/wall')

#Delete comment:
def delete_comment(request, comment_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    if request.method == "GET":
        return redirect('/wall')
    comment = Posted_Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('/wall')

#Logout user_________________________________
def logout_user(request):
    request.session.flush()
    return redirect('/')

