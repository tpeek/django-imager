from django.contrib import admin

from .models import ImagerProfile


# class ImagerProfileAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['user']}),
#         ('Date information', {'fields': ['camera'], 'classes': ['collapse']}),
#     ]
#     list_display = ('user.username', 'camera', 'website_url')
#     # list_filter = ['pub_date']

admin.site.register(ImagerProfile)
