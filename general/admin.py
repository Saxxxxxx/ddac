from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Country, State

class CountryFilter(admin.SimpleListFilter):
    title = _('Country')
    parameter_name = 'country_id'

    def lookups(self, request, model_admin):
        countries = Country.objects.all()
        return [(country.pk, country.country_name) for country in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country_id=self.value())
        return queryset

class StateInline(admin.TabularInline):
    model = State
    extra = 0  # Allow editing existing instances

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    '''DEFINE ADMIN MODEL FOR Country MODEL'''
    
    list_display = ('country_name', 'creator')
    search_fields = ('country_name',)
    ordering = ('country_name', 'creator')
    inlines = [StateInline]

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    '''DEFINE ADMIN MODEL FOR State MODEL'''

    list_display = ('state_name', 'get_country_name', 'creator')
    search_fields = ('state_name', 'country_id__country_name')
    ordering = ('state_name', 'creator')
    list_filter = (CountryFilter,)

    def get_country_name(self, obj):
        return obj.country_id.country_name if obj.country_id else None

    get_country_name.short_description = 'Country Name'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['state_name'].initial = obj.state_name
        return form
