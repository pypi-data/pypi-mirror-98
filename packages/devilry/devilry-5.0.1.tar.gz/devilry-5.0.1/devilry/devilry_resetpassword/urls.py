from django.conf.urls import url
from cradmin_legacy.apps.cradmin_resetpassword.views.begin import BeginPasswordResetView
from cradmin_legacy.apps.cradmin_resetpassword.views.email_sent import EmailSentView
from cradmin_legacy.apps.cradmin_resetpassword.views.reset import ResetPasswordView


urlpatterns = [
    url(r'^begin',
        BeginPasswordResetView.as_view(),
        name="cradmin-resetpassword-begin"),
    url(r'^email-sent',
        EmailSentView.as_view(),
        name="cradmin-resetpassword-email-sent"),
    url(r'^reset/(?P<token>.+)',
        ResetPasswordView.as_view(),
        name="cradmin-resetpassword-reset"),
]
