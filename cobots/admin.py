from django.contrib import admin
from .models import Cobots


@admin.register(Cobots)
class CobotsAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'is_approved')
