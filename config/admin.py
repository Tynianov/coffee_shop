from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import *


@admin.register(RestaurantBranch)
class BranchInline(admin.ModelAdmin):
    list_display = ['branch_name', 'is_active']


@admin.register(RestaurantConfig)
class RestaurantConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(WorkHours)
class WorkHoursAdmin(admin.ModelAdmin):
    list_display = ['begin', 'end']
