from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from app.models import Position, Role
from app.serializers.position import PositionSerializer
from app.api.login import is_auth


class PositionListCreateView(generics.GenericAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get(self, request):
        positions = self.get_queryset()
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data)

    @is_auth({Role.ADMIN.value})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
