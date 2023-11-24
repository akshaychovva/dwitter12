from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('dweet_delete/<int:pk>', views.delete_dweet, name='dweet_delete'),
    path('dweet_update/<int:pk>', views.Update_dweet, name='dweet_update')
]