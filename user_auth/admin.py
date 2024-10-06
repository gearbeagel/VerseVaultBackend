from django.contrib import admin

from user_auth.models import Profile, ReaderStats, WriterStats

# Register your models here.
admin.site.register(Profile)
admin.site.register(ReaderStats)
admin.site.register(WriterStats)