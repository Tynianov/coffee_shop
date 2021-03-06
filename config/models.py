from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel

from utils.models import StatusModel, StatusQuerySet


class WorkHours(models.Model):
    begin = models.TimeField(_("Start"))
    end = models.TimeField(_('End'))

    class Meta:
        verbose_name = _("Work Hour")

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

    class Meta:
        verbose_name = _("Restaurant config")


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
    weekday_working_hours = models.ForeignKey(
        WorkHours,
        on_delete=models.SET_NULL,
        null=True,
        related_name='weekday_working_hours',
        help_text=_("Set working hours during weekdays")
    )

    weekend_working_hours = models.ForeignKey(
        WorkHours,
        on_delete=models.SET_NULL,
        null=True,
        related_name='weekend_working_hours',
        help_text=_("Set working hours during weekends")
    )
    lat = models.DecimalField(
        _("Latitude"),
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text=_("Enter latitude of branch")
    )
    lon = models.DecimalField(
        _("Longitude"),
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text=_("Enter longitude of branch")
    )

    objects = StatusQuerySet.as_manager()

    class Meta:
        verbose_name = _("Restaurant branch")
        verbose_name_plural = _("Restaurant branches")


class AppMetadataConfig(SingletonModel):
    terms_and_conditions = models.TextField(
        _("Terms and Conditions"),
        help_text=_("Enter app terms and Conditions")
    )
    android_download_link = models.URLField(
        _("Android app download link")
    )
    ios_download_link = models.URLField(
        _("IOS app download link")
    )
    privacy_policy = models.TextField(
        _("Privacy Policy"),
        help_text=_("Enter app Privacy Policy")
    )

    class Meta:
        verbose_name = _("App metadata config")

    def __str__(self):
        return "App config"
