from django.shortcuts import render
from django.views.generic.base import TemplateView
from useraccess.models import SelectedPackages
# Create your views here.


class AdminDashboard(TemplateView):
    template_name = "admindash.html"

    def get(self, request):
        Packages = SelectedPackages.objects.count()
        import ipdb
        ipdb.set_trace()
        Packages = {}
        return render(request, "admindash.html", {"Packages": Packages})
