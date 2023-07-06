from django.urls import path, include
from . import views

urlpatterns = [
   path("game", views.GameGroupAPIView.as_view()),
   path('users', views.UsersListApIView.as_view())
]