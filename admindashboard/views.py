from django.shortcuts import render
from django.views.generic.edit import FormView
from useraccess.models import SelectedPackages
import collections
from useraccess.models import Packages
from .forms import MessageForm
# Create your views here.


class AdminDashboardView(FormView):
    template_name = "admindash.html"
    form_class = MessageForm
    success_url = '/admindash/'

    def get(self, request):
        form = self.form_class()
        bundle_id = SelectedPackages.objects.values("bundle_id")
        bundle_id_dict_list = [items for items in bundle_id]
        bundle_id_list = [items["bundle_id"] for items in bundle_id_dict_list]

        bundle_id_and_freq = dict(collections.Counter(bundle_id_list))
        package_freq_list = []

        for keys, values in bundle_id_and_freq.items():
            package = [
                items for items in Packages.objects.filter(
                    id=keys).values("bundle", "bundle_length", "bundle_price")
            ]
            count = values
            bundle_freqs = {"packages": package, "count": count}
            package_freq_list.append(bundle_freqs)

        return render(request, "admindash.html", {
            "bundle_freqs": package_freq_list,
            "form": form
        })
