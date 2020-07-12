from django.urls import path
from . import views

urlpatterns = [
	path('postlogin', views.postLogin, name="login-output"),
	path('signup', views.signup, name="signup"),	
	path('postsignup', views.postSignup, name="signup"),	
	path('', views.welcome, name="index"),
	path('update_task/<str:pk>/', views.updateTask, name="update_task"),
	path('delete/<str:pk>/', views.deleteTask, name="delete"),
]