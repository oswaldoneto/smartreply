from django.contrib import admin

from crm.models import Campanha, Cliente, Cobranca


@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    pass


class CobrancaInline(admin.TabularInline):
    model = Cobranca


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fone', 'email',)
    inlines = [CobrancaInline]
