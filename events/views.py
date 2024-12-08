from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,BasePermission
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.helper import IsAdminUser,IsUser




class EventView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]
    @swagger_auto_schema(
        operation_description="Get a list of all events",
        responses={200: EventSerializer(many=True)}
    )
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new event",
        request_body=EventSerializer,
        responses={201: EventSerializer}
    )
    def post(self, request):
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({'detail': 'User Does Not Exist'})
        print("user.role",user.email)
        if user.role != 'Admin':
            return Response({'detail': 'Only admins can create events'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    @swagger_auto_schema(
        operation_description="Get a specific event by its ID",
        responses={200: EventSerializer}
    )
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing event by its ID",
        request_body=EventSerializer,
        responses={200: EventSerializer, 400: 'Bad Request', 403: 'Forbidden'}
    )
    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({'detail': 'User Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.role != 'Admin':
            return Response({'detail': 'Only admins can update events'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an existing event by its ID",
        responses={204: 'No Content', 403: 'Forbidden'}
    )
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({'detail': 'User Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.role != 'Admin':
            return Response({'detail': 'Only admins can delete events'}, status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response({'detail': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class PurchaseTicketView(APIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(
        operation_description="Purchase tickets for a specific event",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of tickets to purchase', example=0)
            },
        ),
        responses={201: 'Ticket purchased successfully', 400: 'Not enough tickets available'}
    )
    def post(self, request, id):
        event = get_object_or_404(Event, id=id)
        quantity = int(request.data.get('quantity', 0))
        if quantity==0:
            return Response({'detail': 'Please select at least one ticket to proceed.'}, status=status.HTTP_400_BAD_REQUEST)
            pass
        elif event.tickets_sold + quantity > event.total_tickets:
            return Response({'detail': 'Not enough tickets available'}, status=status.HTTP_400_BAD_REQUEST)
        

        Ticket.objects.create(user=request.user, event=event, quantity=quantity)
        event.tickets_sold += quantity
        event.save()
        return Response({'detail': 'Tickets purchased successfully'}, status=status.HTTP_201_CREATED)


class TicketListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all tickets purchased by the authenticated user",
        responses={200: TicketSerializer(many=True)}
    )
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific ticket purchased by the authenticated user",
        responses={200: TicketSerializer}
    )
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
