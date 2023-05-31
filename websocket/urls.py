from django.urls import path, include
from . import views

urlpatterns = [
   path("groups/<int:owner_id>/", views.GameGroupAPIView.as_view()),
   path('users', views.UsersListApIView.as_view()),
   path('creategroup', views.CreateGroupAPIView.as_view()),
]