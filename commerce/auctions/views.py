from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from .models import User, AuctionListing, Category, Bid, Comment, Watchlist

def index(request):
    user = request.user
    # Show different listings based on whether the user is authenticated
    if user.is_authenticated:
        # Show active listings or closed ones where the user was the highest bidder
        listings = AuctionListing.objects.filter(
            Q(is_active=True) |
            Q(is_active=False, bids__user=user, bids__bid_amount=F('current_price'))
        ).distinct().order_by('-created_at')
    else:
        # Show only active listings for unauthenticated users
        listings = AuctionListing.objects.filter(is_active=True).order_by('-created_at')
    
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign in the user with provided credentials
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if login was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # If login fails, show an error message
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        # Display the login form
        return render(request, "auctions/login.html")


def logout_view(request):
    # Log the user out and redirect to the index page
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        # Gather registration details from the form
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            # If passwords don't match, show an error
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Try creating a new user account
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            # If username already exists, show an error
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        # Log the new user in and redirect to the index
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        # Display the registration form
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        # Gather listing details from the form
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.FILES["image"]
        category_name = request.POST.get("category", "")

        # Ensure that the specified category exists or create a new one
        category, created = Category.objects.get_or_create(name=category_name)

        # Create a new auction listing with the provided data
        auction_listing = AuctionListing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_price=starting_bid,
            image=image,
            category=category,
            user=request.user
        )
        auction_listing.save()

        # Redirect to the index page after the listing is created
        return redirect("index")  # Redirect to the index page after creation

    # Render the form to create a new listing
    return render(request, "auctions/create_listing.html")


def listing(request, slug):
    # Retrieve the auction listing by its slug
    listing = get_object_or_404(AuctionListing, slug=slug)
    user = request.user

    # Check if the user is watching this listing
    is_watching = user.is_authenticated and Watchlist.objects.filter(user=user, listing=listing).exists()

    if request.method == "POST":
        # Handle adding/removing the listing from the watchlist
        if "watchlist" in request.POST:
            if is_watching:
                # If already watching, remove it from the watchlist
                Watchlist.objects.filter(user=user, listing=listing).delete()
            else:
                # Add the listing to the watchlist
                Watchlist.objects.create(user=user, listing=listing)
            return redirect('listing', slug=listing.slug)

        # Handle placing a bid
        elif "bid" in request.POST:
            bid_amount = request.POST["bid_amount"]
            try:
                bid_amount = float(bid_amount) # Ensure the bid amount is a valid number
            except ValueError:
                # If the input is not a valid number, show an error
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "error": "Invalid bid amount.",
                    "is_watching": is_watching
                })
            
            else:
                # Check if the bid is high enough
                if bid_amount < listing.starting_bid or bid_amount <= listing.current_price:
                    error = "Bid must be greater than the current price and at least as large as the starting bid."
                else:
                    # Place the bid and update the current price
                    Bid.objects.create(
                        user=user,
                        auction_listing=listing,
                        bid_amount=bid_amount
                    )
                    listing.current_price = bid_amount
                    listing.save()
                    return redirect('listing', slug=listing.slug)
                
            # If there was an error, re-render the page with the error message
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "is_watching": is_watching,
                "error": error,
                "bids": listing.bids.all().order_by('-bid_amount'),
                "comments": listing.comments.all(),
            })

        # Handle closing the auction
        elif "close_auction" in request.POST and listing.user == user:
            listing.is_active = False
            listing.save()
            return redirect('listing', slug=listing.slug)

        # Handle adding a comment to the listing
        elif "add_comment" in request.POST:
            content = request.POST.get("content")
            if content:
                # Create a new comment with the provided content
                Comment.objects.create(
                    user=user,
                    auction_listing=listing,
                    content=content
                )
            return redirect('listing', slug=listing.slug)
    
    # Retrieve bids and comments to display on the page
    bids = listing.bids.all().order_by('-bid_amount')
    comments = listing.comments.all()
    # Check if the user is the highest bidder when the auction is closed
    is_winner = user.is_authenticated and not listing.is_active and bids.exists() and bids.first().user == user

    # Render the listing page with all the relevant details
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watching": is_watching,
        "bids": bids,
        "comments": comments,
        "is_winner": is_winner,
    })


@login_required
def delete_listing(request, slug):
     # Retrieve the listing that the user wants to delete
    listing = get_object_or_404(AuctionListing, slug=slug)

    # Check if the logged-in user is the creator of the listing
    if request.user != listing.user:
        return HttpResponseForbidden("You are not allowed to delete this listing.")

    # Delete the listing and redirect to the index
    listing.delete()
    return redirect("index")

def categories(request):
    # Retrieve and order all categories by name
    categories = Category.objects.all().order_by('name')
    # Render the categories page
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, slug):
    # Retrieve the category by its slug
    category = get_object_or_404(Category, slug=slug)
    # Show only active listings within the selected category
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    # Render the page with listings from this category
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

@login_required
def add_comment(request, slug):
    # Retrieve the listing for which the comment is being added
    listing = get_object_or_404(AuctionListing, slug=slug)
    if request.method == "POST":
        # Create a new comment with the provided content
        content = request.POST["content"]
        Comment.objects.create(user=request.user, auction_listing=listing, content=content)
        # Redirect back to the listing page
    return redirect('listing', slug=slug)

@login_required
def watchlist(request):
    user = request.user
    # Retrieve watchlist items, including closed listings where the user was the highest bidder
    watchlist_items = Watchlist.objects.filter(
        user=user,
        listing__is_active=True
    ) | Watchlist.objects.filter(
        user=user,
        listing__is_active=False,
        listing__bids__user=user,
        listing__bids__bid_amount=F('listing__current_price')
    )
    
    # Ensure the list is distinct to avoid duplicates
    watchlist_items = watchlist_items.distinct()

     # Render the watchlist page with the user's watchlist items
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })
