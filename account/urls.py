from django.conf.urls import url

from .views import (SignUp, Confirm, ConfirmStatus, SignIn, SignOut, Reset,
                    ResetStatus, Update, UpdateStatus)


urlpatterns = [
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^confirm/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<confirmation>[\w]+)/$',
        Confirm.as_view(), name='confirm_link'),
    url(r'^confirm/success/$', ConfirmStatus.as_view(), name='confirm_success'),
    url(r'^confirm/fail/$', ConfirmStatus.as_view(), name='confirm_fail'),

    url(r'^signin/$', SignIn.as_view(), name='signin'),
    url(r'^signout/$', SignOut.as_view(), name='signout'),
    url(r'^reset/$', Reset.as_view(), name='reset'),
    url(r'^reset/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<confirmation>[\w]+)/$',
        Reset.as_view(), name='reset_link'),
    url(r'^reset/success/$', ResetStatus.as_view(), name='reset_success'),
    url(r'^reset/fail/$', ResetStatus.as_view(), name='reset_fail'),

    url(r'^update/$', Update.as_view(), name='update'),
    url(r'^update/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<confirmation>[\w]+)/$',
        Update.as_view(), name='update_link'),
    url(r'^update/success/$', UpdateStatus.as_view(), name='update_success'),
    url(r'^update/fail/$', UpdateStatus.as_view(), name='update_fail'),
    url(r'^update/password/$', UpdateStatus.as_view(), name='update_password'),
]
