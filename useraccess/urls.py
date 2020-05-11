from django.urls import path, include
from .views import HomeView, SignupView, ProfileView, PaymentView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name="home" ),
    path('signup/', SignupView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('payment/', TemplateView.as_view(template_name='payment.html'), name='payment'),
    path('packages/', TemplateView.as_view(template_name='packages.html'), name='packages')
]

