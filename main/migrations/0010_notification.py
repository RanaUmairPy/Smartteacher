# Generated by Django 5.2.1 on 2025-07-21 01:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_assignment_dead_line'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('sent_time', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('classroom_id', models.CharField(blank=True, max_length=36, null=True)),
                ('assignment_id', models.CharField(blank=True, max_length=36, null=True)),
                ('type', models.CharField(default='new_assignment', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_time'],
            },
        ),
    ]
