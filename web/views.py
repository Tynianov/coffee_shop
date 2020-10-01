from django.shortcuts import render

from config.models import AppMetadataConfig
from django.utils.translation import ugettext_lazy as _


def index(request):
    config = AppMetadataConfig.get_solo()
    return render(request, "web/index.html", context={"config": config})


def terms_and_conditions(request):
    config = AppMetadataConfig.get_solo()
    return render(request, "web/terms_policy.html",
                  context={"text": config.terms_and_conditions, "title": _("Terms and Conditions")})


def privacy_policy(request):
    config = AppMetadataConfig.get_solo()
    return render(request, "web/terms_policy.html",
                  context={"text": config.privacy_policy, "title": _("Privacy Policy")})
