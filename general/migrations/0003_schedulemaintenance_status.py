# Generated by Django 4.2.11 on 2024-04-13 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_schedulemaintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulemaintenance',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
