from django.apps import AppConfig

class TrafficApiConfig(AppConfig):
    """
    Configuration class for the traffic API application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traffic_api'

    def ready(self):
        """
        Overriding ready() allows for initialization tasks or registering signals.
        Called when the application starts.
        """
        pass
