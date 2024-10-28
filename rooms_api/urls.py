from django.urls import path
from .views import RoomListCreateView, RoomDetailUpdateView

urlpatterns = [
    path('rooms/', RoomListCreateView.as_view(), name = 'room-list-create'),
    path('rooms/<int:pk>/', RoomDetailUpdateView.as_view(), name = 'room-detail-update'),
]
