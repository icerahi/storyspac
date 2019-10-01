import allauth
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect

from django.urls import path, include, reverse, reverse_lazy

from accounts.forms import PasswordChangeForm
from accounts.views import PeopleListView, UserRegisterView
from fame.views import index, ResetPasswordRequestView, PasswordResetConfirmView, activate, signup
from .views import SearchView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',index,name='index'),
    #authentication
    path('', include('django.contrib.auth.urls'),name='login'),
    path('signup/',signup,name='signup'),

    path('admin/', admin.site.urls),
    # profile
    path('profile/', include(('accounts.urls', 'accounts'), namespace='profile')),

    #people ,photo,stickypic,article
    path('people/',PeopleListView.as_view(),name='people'),
    path('photo/',include(('photos.urls','photos'),namespace='photo')),
    path('stickypic/', include(('stickypics.urls', 'stickypics'), namespace='stickypic')),
    path('article/', include(('articles.urls', 'articles'), namespace='article')),

    #api
    path('^api-auth/', include('rest_framework.urls')),
    #search
    path('search/',SearchView.as_view(),name='search'),


# all auth
    path('accounts/',include('allauth.urls')),
    #password _set
    # path('/accounts/password/change/',allauth.account.views.PasswordChangeView.as_view(),name="account_change_password"),

    path('change_password/',auth_views.PasswordChangeView.as_view(form_class=PasswordChangeForm,template_name='registration/password_change.html'),name='change_password'),
    path('change_password/done/',auth_views.PasswordChangeDoneView.as_view( template_name='registration/password_change_done.html'),name='change_password_done'),
    # password_reset
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('reset_password_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
    path('reset_password/',ResetPasswordRequestView.as_view(),name='reset_password'),


    #All api url
    path('api/articles/',include(('articles.api.urls','articles.api'),namespace='articles-api')), #articles api
]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)