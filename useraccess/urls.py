from django.urls import path, include
from .views import HomeView, SignupView, ProfileView, PaymentView
from django.views.generic import TemplateView

urlpatterns = [
    path('', HomeView.as_view(), name="home" ),
    path('signup/', SignupView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('login/', TemplateView.as_view(template_name='registration/login.html'), name='login'),
    path('payment/', TemplateView.as_view(template_name='payment.html'), name='payment'),
    path('packages/', TemplateView.as_view(template_name='packages.html'), name='packages')
]

