from django.contrib import admin

# Register your models here.
from mail.models import Message, Property, Payload


class PropertyInline(admin.TabularInline):
    model = Property


class PayloadInline(admin.TabularInline):
    model = Payload


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'uuid', 'state',)
    inlines = [PropertyInline, PayloadInline]
