from django.urls import path
from authentification import views

urlpatterns = [
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout_user, name="logout"),
    path('signin/<int:id_user>', views.signin, name="signin"),
    path('user', views.user, name="user")
]
