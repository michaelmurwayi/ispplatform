from django.urls import path, include
from .views import HomeView, SignupView, ProfileView
from django.views.generic import TemplateView

urlpatterns = [
    path('', HomeView.as_view(), name="home" ),
    path('signup/', SignupView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('login/', TemplateView.as_view(template_name='registration/login.html'), name='google_login')
]

