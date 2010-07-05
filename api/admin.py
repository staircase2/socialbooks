from django.contrib import admin

from socialbooks.api import models

class APIKeyAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.APIKey, APIKeyAdmin)
