from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel

from utils.models import StatusModel, StatusQuerySet


class WorkHours(models.Model):
    begin = models.TimeField(_("Start"))
    end = models.TimeField(_('End'))

    class Meta:
        verbose_name = _("Work Hours")

    def __str__(self):
        return self.begin.strftime("%H:%M") + "-" + self.end.strftime("%H:%M")


class WeekDay(models.Model):
    WEEKDAYS = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    ]
    name = models.PositiveSmallIntegerField(choices=WEEKDAYS, unique=True)
    duration = models.ManyToManyField(
        "WorkHours", verbose_name="Duration", help_text="Working hours"
    )

    def __str__(self):
        return f"{self.get_name_display()}, {self.working_hours}"

    class Meta:
        verbose_name = _("Week day")
        verbose_name_plural = _("Week days")

    @property
    def working_hours(self):
        result = ",".join(str(work_hours) for work_hours in self.duration.all())
        return result


class RestaurantConfig(SingletonModel):

    name = models.CharField(
        _("Name"),
        max_length=512,
        help_text=_("Enter restaurant name")
    )
    email = models.EmailField(
        _("Email"),
        null=True,
        blank=True,
        help_text=_("Enter restaurant email address")
    )
    website = models.URLField(
        _("Website"),
        blank=True,
        null=True,
        help_text=_("Enter restaurant website")
    )
    phone = models.CharField(
        _("Phone number"),
        blank=True,
        null=True,
        max_length=16,
        help_text=_("Enter restaurant phone number")
    )
    instagram_link = models.CharField(
        _("Instagram link"),
        max_length=256,
        blank=True,
        null=True,
        help_text=_("Enter Instagram link")
    )
    facebook = models.CharField(
        _("Facebook link"),
        max_length=256,
        blank=True,
        null=True,
        help_text=_("Enter Facebook link")
    )
    logo = models.ImageField(
        _("Restaurant logo"),
        blank=True,
        null=True,
        upload_to='restaurant',
        help_text=_("Add restaurant logo to display it in the app")
    )


class RestaurantBranch(StatusModel):
    branch_name = models.CharField(
        _("Branch name"),
        max_length=512,
        help_text=_("Enter branch name")
    )
    branch_phone = models.CharField(
        _("Phone number"),
        blank=True,
        null=True,
        max_length=16,
        help_text=_("Enter restaurant phone number")
    )
    working_days = models.ManyToManyField(
        WeekDay,
        verbose_name=_('Working hours during week'),
        blank=True,
        help_text=_("Specify days in which branch will work")
    )
    address = models.CharField(
        _("Branch address"),
        max_length=512,
        help_text=_("Enter Branch address")
    )
    google_maps_iframe = models.TextField(
        _('Google Maps embedded code'),
        help_text=_("Click 'Share or embed map', then click 'Embed map' and copy-paste code there"),
        blank=True
    )
    image = models.ImageField(
        _("Branch image"),
        blank=True,
        null=True,
        upload_to='branch_images',
        help_text=_("Add branch image to display it in the app")
    )
    short_description = models.CharField(
        _("Short description"),
        blank=True,
        null=True,
        max_length=512,
        help_text=_("Enter short description of branch")
    )

    objects = StatusQuerySet.as_manager()

    class Meta:
        verbose_name = _("Restaurant branch")
        verbose_name_plural = _("Restaurant branches")
