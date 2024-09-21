from .serializers import SpeedReadingSerializer, RoadSegmentSerializer, SpeedIntervalSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets
from .models import SpeedReading, RoadSegment, SpeedInterval
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    RoadSegment API View
    ---
    List, create, retrieve, update, or delete road segments.
    Filters are applied based on traffic intensity.

    - **GET**: Retrieve road segments (filterable by traffic intensity).
    - **POST**: Create a new road segment (admin users only).
    - **PATCH**/**PUT**: Update a road segment (admin users only).
    - **DELETE**: Delete a road segment (admin users only).
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['speed_readings__traffic_intensity']  # Filtra pela intensidade de tráfego


class SpeedReadingViewSet(viewsets.ModelViewSet):
    """
    SpeedReading API View
    ---
    List, create, retrieve, update, or delete speed readings.

    - **GET**: Retrieve speed readings (filterable by traffic intensity).
    - **POST**: Create a new speed reading (admin users only).
    - **PATCH**/**PUT**: Update a speed reading (admin users only).
    - **DELETE**: Delete a speed reading (admin users only).
    """
    queryset = SpeedReading.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SpeedReadingSerializer
    
    def get_queryset(self):
        """
        Optionally filter speed readings by traffic intensity.
        """
        queryset = super().get_queryset()
        intensity = self.request.query_params.get('intensity')

        if intensity:
            if intensity == 'elevada':
                queryset = queryset.filter(speed__lte=20)
            elif intensity == 'média':
                queryset = queryset.filter(speed__gt=20, speed__lte=50)
            elif intensity == 'baixa':
                queryset = queryset.filter(speed__gt=50)

        return queryset


class SpeedIntervalViewSet(viewsets.ModelViewSet):
    """
    SpeedInterval API View
    ---
    List, create, retrieve, update, or delete speed intervals.

    - **GET**: Retrieve speed intervals.
    - **POST**: Create a new speed interval (admin users only).
    - **PATCH**/**PUT**: Update a speed interval (admin users only).
    - **DELETE**: Delete a speed interval (admin users only).
    """
    queryset = SpeedInterval.objects.all()
    serializer_class = SpeedIntervalSerializer
    permission_classes = [IsAdminOrReadOnly]
