from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Room

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    return Response(rooms)