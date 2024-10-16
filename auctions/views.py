from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


from .models import User,Category,Listing,Bid,Comment


def viewProduct(request,id):
    productData=Listing.objects.get(pk=id)
    isOwner=productData.owner.username==request.user.username
    isInWatchlist=request.user in productData.watchlist.all()
    comments=Comment.objects.filter(listing=productData)
    now = timezone.now() 
    return render(request,"auctions/viewProduct.html",{
        "product":productData,
        "isInWatchlist":isInWatchlist,
        "comments":comments,
        "time":now,
        "isOwner":isOwner
    })
    
def closeBid(request,id):
    productData=Listing.objects.get(pk=id)
    isOwner=productData.owner.username==request.user.username
    isInWatchlist=request.user in productData.watchlist.all()
    comments=Comment.objects.filter(listing=productData)
    now = timezone.now() 
    productData.isActive=False
    productData.save()
    return render(request,"auctions/viewProduct.html",{
        "product":productData,
        "isInWatchlist":isInWatchlist,
        "comments":comments,
        "message":"Congrats!! your product is sold",
        "update":True,
        "time":now,
        "isOwner":isOwner
    })
       
    
def addBid(request,id):
    newBid=request.POST['newBid']
    productData=Listing.objects.get(pk=id)
    isOwner=productData.owner.username==request.user.username
    isInWatchlist=request.user in productData.watchlist.all()
    comments=Comment.objects.filter(listing=productData)
    now = timezone.now()
    if int(newBid)>productData.price.bid:
        updateBid=Bid(user=request.user,bid=int(newBid))
        updateBid.save()
        productData.price=updateBid
        productData.save()

        return render(request,"auctions/viewProduct.html",{
        "product":productData,
        "isInWatchlist":isInWatchlist,
        "comments":comments,
        "message":"Congrats!! You are current highest bidder right now",
        "update":True,
        "time":now,
        "isOwner":isOwner
            })

    else:
        return render(request,"auctions/viewProduct.html",{
        "product":productData,
        "isInWatchlist":isInWatchlist,
        "comments":comments,
        "message":"Oops!! your bid is lower than current bid,bid higher.",
        "update":False,
        "time":now,
        "isOwner":isOwner
    })
        
def addComment(request,id):
    author=request.user
    listing=Listing.objects.get(pk=id)
    message=request.POST['newComment']
    
    newComment=Comment(
        author=author,
        listing=listing,
        message=message
    )  
    newComment.save()
    return HttpResponseRedirect(reverse("viewProduct",args=(id, )))
   
    
def displayWatchList(request):
    currentUser=request.user
    listings=currentUser.userWatchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })
    
def removeWatchlist(request,id):
    productData=Listing.objects.get(pk=id)
    currentUser=request.user
    productData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("viewProduct",args=(id, )))
    

def addWatchlist(request,id):
    productData=Listing.objects.get(pk=id)
    currentUser=request.user
    productData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("viewProduct",args=(id, )))    

def index(request):
    activeListings=Listing.objects.all()
    allCategories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListings,
        "categories":allCategories,
    })
def active(request):
    activeListings=Listing.objects.filter(isActive=True)
    allCategories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListings,
        "categories":allCategories,
    })
    
    
def categoryWise(request):
    if request.method=="POST":
        categoryFromForm=request.POST['category']
        category=Category.objects.get(categoryName=categoryFromForm)
        activeListings=Listing.objects.filter(isActive=True,category=category)
        allCategories=Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings":activeListings,
            "categories":allCategories,
        })
        
    
def createListing(request):
    if request.method=="GET":
        allCategories=Category.objects.all()
        return render(request,"auctions/createListing.html",{
            "categories":allCategories
            
        })
    else:
        # get data from form
        title=request.POST["title"]
        descript=request.POST["descript"]
        imageUrl=request.POST["imageUrl"]
        price=request.POST["price"]
        category=request.POST["category"]
        currUser=request.user
        categoryData=Category.objects.get(categoryName=category)
        # create new Bid to place price
        bid=Bid(bid=int(price),user=currUser)
        bid.save()
        
        newListing=Listing(
        name=title,
        descript=descript,
        imageUrl=imageUrl,
        price=bid,
        owner=currUser, 
        category=categoryData 
        )
        # save
        newListing.save()
        
        return HttpResponseRedirect(reverse(index))
          
       

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        message=''
        confirmation = request.POST["confirmation"]

        if password != confirmation :
          return render(request, "auctions/register.html", {
                "message": "Password must match."
            })
            
        if len(password)<6:
            return render(request, "auctions/register.html", {
                "message": "Password must be alteast 6 char long."
            })
            
            
        

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
