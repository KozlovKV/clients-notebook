# Generated by Django 3.2.5 on 2021-07-09 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services_app', '0007_servicenotegenerationpattern'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicenotegenerationpattern',
            old_name='time_end',
            new_name='day_time_end',
        ),
        migrations.RenameField(
            model_name='servicenotegenerationpattern',
            old_name='time_start',
            new_name='day_time_start',
        ),
        migrations.RenameField(
            model_name='servicenotegenerationpattern',
            old_name='addition',
            new_name='multi_addition',
        ),
    ]