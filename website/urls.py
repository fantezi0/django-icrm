from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('signup/', views.signup_user, name = 'signup'),
    path('add_item/', views.add_item, name = 'add_item'),
    path('display/', views.display, name = 'display'),
    path('ed_item/<int:id>', views.ed_item, name = 'ed_item'),
    path('delete_item>', views.delete_item, name = 'delet_item'),
    path('search/', views.search_items, name='search_items'),
]

