from django.contrib import admin

from classification.models import Classification, Property


class PropertyInlineAdmin(admin.TabularInline):
    model = Property


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [PropertyInlineAdmin]




