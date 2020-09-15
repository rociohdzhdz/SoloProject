from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validator(self,postdata):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if len(postdata['fname'])<2:
            errors['fname']= "Your name must be more than 2 chars"
        if len(postdata['lname'])<2:
            errors['lname']="Your last name must be more than 2 chars"
        if not EMAIL_REGEX.match(postdata['mail']):
            errors['mail']="Email must be a valid format"
        if len(postdata['password'])<8:
            errors['password']="Password must be at least 8 characters"
        if postdata['password'] != postdata['confirmpass']:
            errors['confirmpass']="Your password and confirm password should match"
        return errors

class ReceiptManager(models.Manager):
    def validator(self,postdata):
        errors={}
        if len(postdata['category'])<1:
            errors['category']= "Your have to add a category"
        if len(postdata['amount'])<1:
            errors['amount']="Amount must be greater than one"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    userid=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    tpin=models.CharField(max_length=255)
    usertype=models.CharField(max_length=255)
    storename=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Receipt(models.Model):
    category=models.CharField(max_length=255)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    recfromuser=models.CharField(max_length=255, default='')
    creator=models.ForeignKey(User,related_name="receipts", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    objects=ReceiptManager()