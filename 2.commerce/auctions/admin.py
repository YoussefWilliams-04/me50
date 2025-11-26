from django.contrib import admin
from .models import User, Listing, Bid, Comment,Watchlist

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display=("id","title","description","currentPrice","user","user_id","category","imageLink")

class BidAdmin(admin.ModelAdmin):
    list_display=("id","bidder","bid","listing","bidder_id")

class UserAdmin(admin.ModelAdmin):
    list_display=("id","username","is_staff")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id","user","listing","description")
    
admin.site.register(User,UserAdmin) 
admin.site.register(Listing ,ListingAdmin )
admin.site.register(Bid, BidAdmin ) 
admin.site.register( Comment, CommentAdmin)
admin.site.register( Watchlist)
