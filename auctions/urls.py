from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListing,name="create"),
    path('categoryWise',views.categoryWise,name="categoryWise"),
    path('listing/<int:id>',views.viewProduct,name="viewProduct"),
    path('removeWatchlist/<int:id>',views.removeWatchlist,name="removeWatchlist"),
    path('addWatchlist/<int:id>',views.addWatchlist,name="addWatchlist"),
    path('Watchlist',views.displayWatchList,name="watchlist"),
    path('addBid/<int:id>',views.addBid,name="addBid"),
    path('addComment/<int:id>',views.addComment,name="addComment"),
    path('closeBid/<int:id>',views.closeBid,name="closeBid"),
    
    
    
    
    
    
]
