from django.contrib import admin
from .models import SpeedReading

@admin.register(SpeedReading)
class SpeedReadingAdmin(admin.ModelAdmin):
    """
    Admin view for SpeedReading model. This class customizes the admin interface 
    to display certain fields and ensures that the `traffic_intensity` field is 
    read-only.
    """
    list_display = ('id', 'speed', 'traffic_intensity')  # Display the id, speed, and traffic intensity in the admin interface.
    readonly_fields = ('id', 'traffic_intensity')  # Make 'traffic_intensity' and 'id' fields read-only in the admin interface.

    def traffic_intensity(self, obj):
        """
        Display the traffic intensity in the admin list view.
        :param obj: The SpeedReading object.
        :return: The traffic intensity string (elevated, medium, or low).
        """
        return obj.traffic_intensity

    traffic_intensity.short_description = 'Intensidade do Trânsito'  # Customize the column name in the admin interface.
