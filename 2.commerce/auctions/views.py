from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Watchlist, Comment


@login_required(login_url="/login")
def index(request):
    # Creating a new listing and bid
    if request.method == "POST":
        listing=Listing(title=request.POST["title"],
                        description=request.POST["description"],
                        currentPrice=request.POST["bid"],
                        user=request.user,
                        category=request.POST["category"],
                        imageLink=request.POST["imageLink"]
                        
                        )
        listing.save()

        bid=Bid(bidder= request.user,
                bid= listing.currentPrice,
                listing=listing)
        bid.save()
        
    # get all active listings
    listings=Listing.objects.all().filter(isActive=True)
            
    return render(request, "auctions/index.html",{
             "listings":listings
            })


def listing(request,listing_id):
    # get chosen listing
     listing=Listing.objects.get(pk=listing_id)

     #get corresponding bid
     bid=Bid.objects.get(listing=listing)
     
     #checks for the presence of a watchlist
     query=Watchlist.objects.filter(user=request.user).filter(listing=listing)

     message=None # contextual message
     comments=Comment.objects.filter(listing=listing)
     if request.method=="POST":
        
        if "bid" in request.POST:
                bid.bid= request.POST["bid"]
                listing.currentPrice=bid.bid
                listing.save()

                bid.bidder=request.user
                message="Succesfully made a bid"
                bid.save()

        elif "watchlist" in request.POST:
            if query:
                  #remove from watchlist
                  Watchlist.objects.filter(user=request.user).filter(listing=listing).delete()
                  message="Removed from watchlist"
            else: 
                # add to watchlist
                watchlist=Watchlist( user=request.user,
                                listing=listing)
                watchlist.save()
                message="Added to watchlist"

        elif "comment" in request.POST:
            # create a comment
            comment=Comment( description=request.POST["comment"],
                            listing=listing,
                            user=request.user)
            comment.save()

        elif "closed" in request.POST:
            #close the listing
            listing.isActive=False
            listing.save()
              
    # re-evaluate the query in the case of a change due to POST
     query=Watchlist.objects.filter(user=request.user).filter(listing=listing)

     return render(request, "auctions/listing.html",{
         "listing":listing,
         "message":message,
         "bid": bid,
         "query": query,
         "comments":comments
         })

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
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
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


@login_required(login_url="/login")
def addListing(request):
    return render(request, "auctions/addListing.html")


def categories(request):
    # define the categories
    categories=["Other",
    "Collectibles",
    "Electronics",
    "Fashion",
    "Health & Beauty",
    "Home & Garden",
    "Toys"]
   
    return render(request,"auctions/categories.html",{
                  "categories": categories})

def category(request,category): 
    # get all active listings with in the category
    listings=Listing.objects.filter(category=category).filter(isActive=True)
    return render(request, "auctions/category.html",{
         "listings": listings,
         "category": category
     }
     )

def watchlist(request):
    watchlists=Watchlist.objects.filter(user=request.user)
    
    return render(request,"auctions/watchlist.html",{
                  "watchlists": watchlists                
    }
    )
