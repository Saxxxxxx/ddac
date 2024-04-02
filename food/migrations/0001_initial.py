# Generated by Django 4.2.11 on 2024-04-01 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSharingCategory',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('delete_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=100)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_changed_by_user', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_retired_by_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'food_sharing_listing_category',
            },
        ),
        migrations.CreateModel(
            name='FoodSharingListingImage',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='food_images')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'db_table': 'food_sharing_listing_image',
            },
        ),
        migrations.CreateModel(
            name='FoodSharingListing',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('delete_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('listing_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('street_address', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=20)),
                ('held_date', models.DateTimeField(null=True)),
                ('expiration_date', models.DateField(null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Reserved', 'Reserved'), ('Claimed', 'Claimed')], max_length=50)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_sharing_category_id', to='food.foodsharingcategory')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_changed_by_user', to=settings.AUTH_USER_MODEL)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_sharing_listing_country_id', to='general.country')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_retired_by_user', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(to='food.foodsharinglistingimage')),
                ('state_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_sharing_listing_state_id', to='general.state')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'food_sharing_listing',
            },
        ),
    ]
