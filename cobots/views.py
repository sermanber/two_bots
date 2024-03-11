from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cobots
from .serializers import CobotsSerializer


# Create your views here.
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Cobots.objects.all()
    serializer_class = CobotsSerializer


class UpdateEventApproval(APIView):
    def post(self, request, event_id):
        event = Cobots.objects.get(id=event_id)
        is_approved = request.data.get('is_approved', None)
        if is_approved is not None:
            event.is_approved = is_approved
            event.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



