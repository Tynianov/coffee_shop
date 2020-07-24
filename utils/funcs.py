from django.contrib.sites.models import Site
from django.conf import settings


def get_backend_url():
    site = Site.objects.get(pk=settings.SITE_ID)
    return "{protocol}://{domain}".format(
        protocol=settings.PROTOCOL, domain=site.domain
    )


def get_absolute_url(path):
    return f'{get_backend_url()}{path}'
