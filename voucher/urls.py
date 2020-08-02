from django.urls import re_path

from .views import *

urlpatterns = [
    re_path('scan-qr-code/(?P<pk>\d+)/$', ScanVoucherQRCode.as_view(), name='scan-voucher-code')
]
