from django.urls import path
from .views import EventView, EventDetailView, PurchaseTicketView, TicketListView, TicketDetailView

urlpatterns = [
    path('events/', EventView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('tickets/<int:id>/purchase/', PurchaseTicketView.as_view(), name='purchase-ticket'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
]
