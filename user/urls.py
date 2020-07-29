from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('profile', UserView.as_view(), name='profile_view'),
    re_path('scan-qr-code/(?P<pk>\d+)/$', ScanUserQRCodeView.as_view(), name='scan-user-code')
]
