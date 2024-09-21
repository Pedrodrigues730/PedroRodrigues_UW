from django.contrib.gis.geos import Point
from django.db import migrations, transaction

def populate_geom_fields(apps, schema_editor):
    RoadSegment = apps.get_model('traffic_api', 'RoadSegment')

    with transaction.atomic():
        for segment in RoadSegment.objects.all():
            # If geom_start or geom_end is None, create Point using long/lat fields
            if segment.geom_start is None:
                segment.geom_start = Point(segment.long_start, segment.lat_start, srid=4326)
            if segment.geom_end is None:
                segment.geom_end = Point(segment.long_end, segment.lat_end, srid=4326)

            # Save the updated segment with correct geom fields
            segment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('traffic_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_geom_fields),
    ]