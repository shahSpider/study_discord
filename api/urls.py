from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('rooms/<str:pk>', views.get_room),
]