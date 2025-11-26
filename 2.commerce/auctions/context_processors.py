from auctions.models import *

def watchlist_count (request):
    
    try: 
        #get the watchlists associated with the user
        watchlists=Watchlist.objects.filter(user=request.user)
    except:
        # if there is an error, then this means the user isnt logged in 
        return { "watchlist_count":False} 
    
    watchlist_count=0
    for i in watchlists:
       watchlist_count=watchlist_count+1
    
    return{
        "watchlist_count":watchlist_count}