from django.urls import path
from generic import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('home', views.homepage, name="home"),
    path('legal', views.legal, name="legal")
]
