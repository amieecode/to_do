from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home-page'),
   path('register/', views.register, name='register'),
   path('login/', views.loginpage, name='login'), 
   path('logout/', views.LogoutView, name='logout'),
   path('delete-task/<str:id>/', views.DeleteTask, name='delete'),
   path('update/<str:id>/', views.Update, name='update'),
   path('edit/<str:id>/', views.edit_task, name='edit-task'),
]
