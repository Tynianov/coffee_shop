from django.urls import include, re_path

urlpatterns = [
    re_path(r'^user/', include('user.urls')),
    re_path(r'restaurant/', include('config.urls')),
    re_path(r'posts/', include('post.urls')),
    re_path(r'vouchers/', include('voucher.urls')),
    re_path(r'menu/', include('menu.urls'))

]
