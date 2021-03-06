# Generated by Django 3.2.4 on 2021-06-18 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('status', models.IntegerField(choices=[(0, 'Свободно'), (1, 'Заято'), (2, 'Прошло'), (3, 'Отменено')], default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='services_app.service')),
            ],
        ),
    ]
