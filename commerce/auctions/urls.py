from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<slug:slug>/", views.listing, name="listing"),
    path("listing/<slug:slug>/delete", views.delete_listing, name="delete_listing"),
    path("listing/<slug:slug>/comment", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path('categories/<slug:slug>/', views.category_listings, name='category_listings'),
    path("watchlist", views.watchlist, name="watchlist"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
