from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('catalog/', views.catalog, name='catalog'),
    path('members/', views.members, name='members'),
    path('circulation/', views.circulation, name='circulation'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("add-book/", views.add_book, name="add_book"),
    path("add-member/", views.add_member, name="add_member"),

]
