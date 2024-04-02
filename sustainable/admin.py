# sustainable_marketplace/admin.py
from django.utils.html import format_html
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.forms import BaseInlineFormSet
from .models import SustainableMarketplaceListing, SustainableMarketplaceCategory, SustainableMarketplaceListingImage

class SustainableMarketplaceListingAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'description','price','get_state_name','get_country_name','get_category_name','get_status','creator')
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        (_('Listing Information'), {'fields': ('price', 'state_id','country_id','category_id','status','images','image_tag')}),
        (_('Creator'), {
            'fields': ('creator', 'user'),
        }),
    )
    readonly_fields = ('image_tag',)

    def get_country_name(self, obj):
        return obj.country_id.country_name if obj.country_id else None
    
    get_country_name.short_description = 'Country Name'

    def get_state_name(self, obj):
        return obj.state_id.state_name if obj.state_id else None
    
    get_state_name.short_description = 'State Name'

    def get_category_name(self, obj):
        return obj.category_id.category_name if obj.category_id else None
    
    get_category_name.short_description = 'Category Name'

    def get_status(self,obj):
        return obj.status

    get_status.short_description = 'Status'

    def image_tag(self, obj):
        images = obj.images.all()
        image_tags = ''
        for image in images:
            print(image.image.url)
            image_tags += '<img src="{}" style="max-width:200px; max-height:200px; margin-right: 10px;"/>'.format(image.image.url)
        return format_html(image_tags)



@admin.register(SustainableMarketplaceCategory)
class SustainableMarketplaceCategoryAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'
    list_display = ['image_tag']

admin.site.register(SustainableMarketplaceListing,SustainableMarketplaceListingAdmin)
admin.site.register(SustainableMarketplaceListingImage, ImageAdmin)

