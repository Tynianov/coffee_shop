from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import *


class WeekDayInline(admin.TabularInline):
    model = RestaurantBranch.working_days.through
    verbose_name = _("Weekday")
    verbose_name_plural = _("Weekdays")
    extra = 0
    max_num = 7


@admin.register(RestaurantBranch)
class BranchInline(admin.ModelAdmin):
    list_display = ['branch_name', 'is_active']
    inlines = [WeekDayInline]


@admin.register(RestaurantConfig)
class RestaurantConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(WorkHours)
class WorkHoursAdmin(admin.ModelAdmin):
    list_display = ['begin', 'end']
