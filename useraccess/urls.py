from django.urls import path, include
from .views import HomeView, SignupView, ProfileView, PackageView, get_bundle
# from mpesa_api.views import packages
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name="home" ),
    path('signup/', SignupView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('packages/', PackageView.as_view(), name='packages'),
    path('get_bundle/', get_bundle, name='get_bundle')
]

