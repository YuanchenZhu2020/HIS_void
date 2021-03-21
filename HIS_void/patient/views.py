from django.shortcuts import render
from django.views import View


class PatientLoginView(View):
    template_name = "page-login.html"

    def get(self, request):
        return render(request, PatientLoginView.template_name, context = {"user_type": "patient"})
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 测试用
        print(username, password)
        if username == "test" and password == "123456":
            return render(request, "index.html")
        else:
            return render(request, PatientLoginView.template_name, context = {"user_type": "patient"})
