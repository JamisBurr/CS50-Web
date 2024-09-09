from django.contrib.auth.models import AbstractUser
from django.db import models 
from django.utils.text import slugify
import itertools

# Extending the default Django User model
class User(AbstractUser):
    pass # Using the default user model as-is, for now

# Category model for grouping auction listings
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True) # Name of the category, must be unique
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True) # URL-friendly version of the name

    def save(self, *args, **kwargs):
        # Auto-generate the slug from the category name if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name # Display the category name when printing the object
    
# AuctionListing model represents each auction item   
class AuctionListing(models.Model):
    title = models.CharField(max_length=100) # Title of the listing
    slug = models.SlugField(unique=True, blank=True) # Unique slug for URLs, generated from title
    description = models.TextField() # Detailed description of the listing
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2) # Starting price of the auction
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Current highest bid
    image = models.ImageField(upload_to='images') # Image associated with the listing, saved in 'images' folder
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings") # Category this listing belongs to 
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the listing was created
    updated_at = models.DateTimeField(auto_now=True) # Timestamp for when the listing was last updated
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings") # User who created the listing
    is_active = models.BooleanField(default=True) # Whether the listing is active or closed

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a unique slug if it hasn't been set
            self.slug = slugify(self.title) # Start with a slugified version of the title
            # Check for uniqueness and append numbers if needed
            for x in itertools.count(1):
                if not AuctionListing.objects.filter(slug=self.slug).exists():
                    break
                # Append a number to the slug if the original is taken
                self.slug = f"{slugify(self.title)}-{x}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.username}" # Display the title and creator's username

# Bid model to track each bid on auction listings
class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2) # Amount of the bid
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids") # User who placed the bid
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids") # Listing the bid is for
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the bid was placed

    def __str__(self):
        return f"{self.user.username} bid {self.bid_amount} on {self.auction_listing.title}" # Display bid details

# Comment model for user comments on listings
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments") # User who made the comment
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments") # Listing the comment is for
    content = models.TextField() # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the comment was made

    def __str__(self):
        return f"Comment by {self.user.username} on {self.auction_listing.title}" # Display comment details
    
# Watchlist model to track listings users are watching    
class Watchlist(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist") # User who is watching the listing
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist_items") # Listing being watched