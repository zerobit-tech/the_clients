from django.contrib import admin

from .models import Client, ClientMeta
# Register your models here.

class ClientMetaInline(admin.TabularInline):
    model = ClientMeta
 
    verbose_name = 'Meta data'
    verbose_name_plural = 'Meta data'
    extra = 2

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = ClientMetaInline,

    list_display = ("user", "active")
