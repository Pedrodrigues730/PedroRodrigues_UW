from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadSegmentViewSet, SpeedReadingViewSet, SpeedIntervalViewSet

router = DefaultRouter()
router.register(r'road-segments', RoadSegmentViewSet)
router.register(r'speed-readings', SpeedReadingViewSet)
router.register(r'speed-intervals', SpeedIntervalViewSet)
router = DefaultRouter()
router.register(r'speed-readings', SpeedReadingViewSet)

router = DefaultRouter()
router.register(r'road-segments', SpeedReadingViewSet, basename='traffic_speed')
router.register(r'speedreading', SpeedReadingViewSet, basename='traffic_speedreading')



urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)),
]