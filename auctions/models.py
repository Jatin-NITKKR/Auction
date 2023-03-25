from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName=models.CharField(max_length=50)
    def __str__(self):
        return self.categoryName
    
class Bid(models.Model):
    bid=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userbid") 
    def __str__(self):
        return f"{self.user} bids {self.bid}"   

class Listing(models.Model):
    name=models.CharField(max_length=25)
    descript=models.CharField(max_length=150)
    imageUrl=models.CharField(max_length=250)
    price=models.ForeignKey(Bid, on_delete=models.CASCADE,blank=True,null=True,related_name="userPrice")
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name="category")
    watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="userWatchlist")
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComment")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True,null=True,related_name="listingComment")
    message=models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.author} commment on {self.listing}"
    
    
 
    
    
        
    
