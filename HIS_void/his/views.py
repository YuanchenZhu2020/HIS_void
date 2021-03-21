from django.shortcuts import render
from django.views import View

from rbac import models as rbac_models


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, IndexView.template_name)


class LoginView(View):
    template_name = "page-login.html"

    def get(self, request):
        return render(request, LoginView.template_name, context={"user_type": "staff"})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = rbac_models.UserInfo.objects.filter(username=username, password=password).first()
        if user:
            request.session["user_name"] = user.name
            request.session["dep_id"] = user.dep_id
            return render(request, "")
        else:
            return render(request, LoginView.template_name)
