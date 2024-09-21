from django.db import models
from django.contrib.gis.db import models as gis_models

class RoadSegment(models.Model):
    """
    Model representing a road segment with a name and geometric data.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Name of the road segment
    geometry = gis_models.LineStringField(srid=4326)  # Geospatial field storing road geometry

    class Meta:
        managed = False  # Do not let Django manage the table creation
        db_table = 'traffic_speed'  # Specify the actual database table name

    def __str__(self):
        """
        String representation of a road segment.
        """
        return self.name
    
class SpeedInterval(models.Model):
    """
    Model representing the speed intervals used for traffic intensity classification.
    """
    low_speed = models.FloatField(default=20)  # Speed threshold for high traffic intensity
    medium_speed = models.FloatField(default=50)  # Speed threshold for medium traffic intensity
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the intervals were last updated

    class Meta:
        ordering = ['-updated_at']  # Order by the most recently updated interval

    def __str__(self):
        """
        String representation of a speed interval.
        """
        return f"Interval updated at {self.updated_at}"

class SpeedReading(models.Model):
    """
    Model representing a speed reading for a particular road segment.
    """
    id = models.AutoField(primary_key=True)
    long_start = models.FloatField(blank=True, null=True)  # Longitude of the starting point
    lat_start = models.FloatField(blank=True, null=True)  # Latitude of the starting point
    long_end = models.FloatField(blank=True, null=True)  # Longitude of the ending point
    lat_end = models.FloatField(blank=True, null=True)  # Latitude of the ending point
    length = models.FloatField(blank=True, null=True)  # Length of the road segment
    speed = models.FloatField(blank=True, null=True)  # Speed recorded in the segment
    geom_start = gis_models.PointField(srid=4326, blank=True, null=True)  # Geospatial start point
    geom_end = gis_models.PointField(srid=4326, blank=True, null=True)  # Geospatial end point

    class Meta:
        managed = False  # Do not let Django manage the table creation
        db_table = 'traffic_speed'  # Specify the actual database table name

    @property
    def traffic_intensity(self):
        """
        Calculate the traffic intensity based on the recorded speed.
        :return: 'elevada' for high, 'média' for medium, 'baixa' for low, or 'desconhecida' if the speed is unknown.
        """
        if self.speed is not None:
            if self.speed <= 20:
                return 'elevada'
            elif 20 < self.speed <= 50:
                return 'média'
            else:
                return 'baixa'
        return 'desconhecida'  # Return unknown if speed is not recorded
    
    def __str__(self):
        """
        String representation of a speed reading.
        """
        return f"SpeedReading {self.id}"
