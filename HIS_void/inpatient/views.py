from django.shortcuts import render, redirect
from django.views import View


class NurseView(View):
    template_name = 'nurse-workspace.html'

    def get(self, request):
        return render(request, NurseView.template_name)
