# Generated by Django 3.2.5 on 2021-07-23 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services_app', '0011_auto_20210718_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicenote',
            name='status',
            field=models.IntegerField(choices=[(0, 'Свободно'), (1, 'Ожидает подтверждения'), (2, 'Занято'), (3, 'Прошло')], default=0),
        ),
    ]