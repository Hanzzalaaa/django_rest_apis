from django.urls import path, include
from .views import *
from django_rest_passwordreset.views import ResetPasswordConfirm,ResetPasswordRequestToken
urlpatterns = [
    path('signup/', UserRegisterView.as_view(),name='signup'),
    path('signin/', UserLoginView.as_view(),name='signin'),
    path('confirm/', ResetPasswordConfirm.as_view(),name='reset-password-confirm'),
    path('password_reset/request/', ResetPasswordRequestToken.as_view(), name='reset-password-request'),

    # path('password_reset/', include(password_reset_urls), name = 'django_rest_passwordreset'),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



]