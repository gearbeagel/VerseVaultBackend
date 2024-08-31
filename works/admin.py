# Register your models here.

from django.contrib import admin
from works.models import *

admin.site.register(Work)
admin.site.register(Tag)
admin.site.register(Chapter)