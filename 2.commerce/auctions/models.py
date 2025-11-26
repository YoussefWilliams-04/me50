from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f" {self.username} "
    # has an inherited "create_user()" method

class Listing(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=64)
    description =models.CharField(max_length=100)
    currentPrice=models.IntegerField()
    isActive=models.BooleanField(default=True)
    imageLink=models.CharField(max_length= 200,blank=True) 
    category=models.CharField(max_length=100,default="No Category Listed")
    date=models.DateField(auto_now_add=True , blank=True ) 

    def __str__(self):
        return f"{self.title}"
    

class Bid(models.Model):
    bidder=models.ForeignKey(User, on_delete=models.CASCADE,default=1) 
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE,default=1) 
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bid}"


class Comment (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE,default=1)

    description =models.CharField(max_length=500)
   
    def __str__(self):
        return f"{self.description}"


class Watchlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f" {self.user} added {self.listing} to their watchlist"


    
