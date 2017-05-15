from django.contrib import admin
from exchange.models import EmailServer, MailBox


class MailBoxInline(admin.TabularInline):
    model = MailBox


@admin.register(EmailServer)
class EmailServerAdmin(admin.ModelAdmin):
    list_display = ('host', 'user', 'active',)
    inlines = [MailBoxInline]

