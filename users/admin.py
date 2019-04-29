from django.contrib import admin
from .models import Act

# Register your models here.
@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    """
    アカウント情報管理用
    """
    pass