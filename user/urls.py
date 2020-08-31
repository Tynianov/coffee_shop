from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('profile', UserView.as_view(), name='profile_view'),
    re_path('scan-qr-code/(?P<pk>\d+)/$', ScanUserQRCodeView.as_view(), name='scan-user-code'),
    re_path(r'^user-voucher-details', UserVoucherDetailsView.as_view(), name='user-voucher-details'),
    re_path(r'scan-qr-code/(?P<pk>\d+)/$', ScanUserQRCodeView.as_view(), name='scan-user-code'),
    re_path(r'^request-reset-password-code', RequestPasswordRestCodeView.as_view(), name='request-reset-password-code'),
    re_path(r'validate-sms-code', ValidatePasswordResetPasswordCodeView.as_view()),
    re_path(r'^change-password', ChangePasswordView.as_view({'post': 'create'}))
]
