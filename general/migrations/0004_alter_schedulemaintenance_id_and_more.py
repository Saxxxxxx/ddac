# Generated by Django 4.2.11 on 2024-04-13 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_schedulemaintenance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulemaintenance',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='schedulemaintenance',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
