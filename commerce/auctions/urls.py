from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makelisting", views.make_listing, name="makelisting"),
    path('<int:auction_id>/viewlisting', views.viewlisting, name='viewlisting'),
    path('<int:auction_id>/watchlist', views.watchlist, name='watchlist'),
    path('<str:username>', views.watchlist_page, name='watchlist_page')
]
