from rest_framework import serializers
from .models import SpeedReading, RoadSegment, SpeedInterval

class RoadSegmentSerializer(serializers.ModelSerializer):
    """
    Serializer for RoadSegment model.
    
    - This serializer handles the representation of road segments,
      including start and end coordinates, the length, and the total 
      number of speed readings.
    - The geom_start and geom_end are returned in Well-Known Text (WKT) format.
    """
    geom_start = serializers.SerializerMethodField()
    geom_end = serializers.SerializerMethodField()
    total_readings = serializers.IntegerField(source='speed_readings.count', read_only=True)

    class Meta:
        model = RoadSegment
        fields = [
            'id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length',
            'geom_start', 'geom_end', 'total_readings'
        ]

    def get_geom_start(self, obj):
        """
        Get start geometry in WKT format.
        """
        return obj.geom_start.wkt  # Corrected: Access geom_start directly and return WKT format

    def get_geom_end(self, obj):
        """
        Get end geometry in WKT format.
        """
        return obj.geom_end.wkt 
    
class SpeedReadingSerializer(serializers.ModelSerializer):
    """
    Serializer for SpeedReading model.
    
    - Handles the representation of speed readings for road segments,
      including speed, intensity (e.g., high, medium, low), and the 
      total number of readings.
    - The intensity is calculated based on the speed value.
    """
    intensity = serializers.SerializerMethodField()
    total_speed_readings = serializers.SerializerMethodField()

    class Meta:
        model = SpeedReading
        fields = ['id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length', 'speed', 'intensity', 'total_speed_readings']

    def get_intensity(self, obj):
        """
        Calculate traffic intensity based on the speed value.
        
        - Speed <= 20 km/h: High intensity
        - Speed > 20 and <= 50 km/h: Medium intensity
        - Speed > 50 km/h: Low intensity
        """
        if obj.speed <= 20:
            return 'elevada'
        elif 20 < obj.speed <= 50:
            return 'média'
        else:
            return 'baixa'
        
    def get_total_speed_readings(self, obj):
        """
        Get the total number of speed readings for the segment.
        """
        return SpeedReading.objects.filter(id=obj.id).count()

class SpeedIntervalSerializer(serializers.ModelSerializer):
    """
    Serializer for SpeedInterval model.
    
    - Represents the speed interval configuration used to infer traffic intensity.
    """
    class Meta:
        model = SpeedInterval
        fields = '__all__'
