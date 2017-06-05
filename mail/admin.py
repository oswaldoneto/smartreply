from django.contrib import admin

# Register your models here.
from mail.models import Message, Property, Payload, MessageClassification, MessageCampaign


class PropertyInline(admin.TabularInline):
    model = Property


class PayloadInline(admin.TabularInline):
    model = Payload


class MessageClassificationInline(admin.TabularInline):
    model = MessageClassification


class MessageCampaignInline(admin.TabularInline):
    model = MessageCampaign


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'uuid', 'state',)
    inlines = [PropertyInline, PayloadInline, MessageCampaignInline, MessageClassificationInline]
