from django.contrib import admin

from crm.models import Campanha


@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    pass