# Generated by Django 4.2.16 on 2024-09-20 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("traffic_api", "0002_alter_roadsegment_table_alter_speedreading_table"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="roadsegment",
            table="traffic_speed",
        ),
    ]
