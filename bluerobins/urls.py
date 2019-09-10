"""bluerobins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from analyticsmaven.views import *
from django.conf.urls import url, include
from django.conf.urls.static import static

from social_django.models import Association, Nonce, UserSocialAuth

admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^djrichtextfield/', include('djrichtextfield.urls')),
    url(r'^', include(('analyticsmaven.urls', 'analyticsmaven'), namespace='analyticsmaven')),
    url(r'^admin/password_reset/$', PasswordResetView.as_view(),{'template_name': 'admin/password_reset_form.html'}, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', PasswordResetDoneView.as_view(),{'template_name': 'admin/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^admin-forgotpassword/$',ForgotPassword.as_view(), name='forgotpasswordpage'),
    url(r'^forgot-password/(?P<uidb64>[0-9A-Za-z_\-]+)/$',ResetPassword.as_view(), name='forgot-password'),
    url(r'^oauth/', include('social_django.urls', namespace='social'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
