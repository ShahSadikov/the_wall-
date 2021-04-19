from django.db import models
from datetime import datetime
from datetime import timedelta
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        #names_____________________________
        if len(postData['first_name']) < 2:
            errors["first_name"] = "The first name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "The last name must be at least 2 characters"

        #check if the age > 13_______________ 
        today = datetime.today()
        eligible_age = today - timedelta(days=365*13)
        if len(postData['dob']) == 0:
            errors['enter_dob'] = "The date of birth must be entered."
        elif postData['dob'] > str(eligible_age): # CHECK THIS LOGIC!!! NOT SURE IF IT'S WORKING CORRECTLY
            errors['not_eligible'] = "Your age is not valid. Try again next year."

        #email______________________________
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "The valid email address must be entered."
        # #unique email check:
        current_user = User.objects.filter(email=postData['email'])
        if len(current_user) >= 1:
            errors['duplicate'] = "The email is already in use" 
        #password___________________________
        if len(postData['password']) < 8:
            errors["password"] = "The password must be at least 8 characters long"
        #password match:
        if postData['password'] != postData['confirm_password']:
            errors["mismatch"] = "The passwords must match!"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) == 0:
            errors['wrong_user'] = "Enter a valid email or password"
        #email check:
        elif len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        #password check:
        elif len(postData['password']) == 0:
            errors['password'] = "You must enter a password"
        elif len(postData['password']) < 8:
            errors['password'] = "The password isn't long enough."
        #check if the email is in DB
        # if so check to see if the email/password match
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors["password"] = "Email and password do not match"
            
        return errors

#a User model:
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    dob = models.DateTimeField()
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Posted_Message(models.Model):
    message = models.TextField()
    posted_by = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Posted_Comment(models.Model):
    comment = models.TextField()
    posted_by = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    #The field below had to be added after the initial creation of the model. Beware of errors it might create!
    posted_message = models.ForeignKey(Posted_Message, related_name='post_comments', on_delete=models.CASCADE, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
