from django.urls import path
from . import views

urlpatterns = [
    path('', views.instructor_list, name='instructor_list'),
    path('<int:pk>/', views.instructor_detail, name='instructor_detail'),
    path('create/', views.instructor_create, name='instructor_create'),
    path('<int:pk>/edit/', views.instructor_edit, name='instructor_edit'),
    path('<int:pk>/delete/', views.instructor_delete, name='instructor_delete'),
]