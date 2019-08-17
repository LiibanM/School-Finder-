from django.contrib import admin
from school.models import mapData, schoolPerformance, UserProfile
# Register your models here.

admin.site.register([mapData, schoolPerformance, UserProfile])
