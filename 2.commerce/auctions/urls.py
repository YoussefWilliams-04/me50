from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addListing", views.addListing,name="addListing"),
    path("<int:listing_id>",views.listing, name="listing"),
    path("categories",views.categories,name="categories"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("category/<category>",views.category, name="category")
]

