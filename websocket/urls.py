from django.urls import path, include
from . import views

urlpatterns = [
   path("groups/<int:group_id>/", views.GameGroupAPIView.as_view())
]