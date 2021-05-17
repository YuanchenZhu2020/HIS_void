from django.shortcuts import render
from django.views import View


class NurseView(View):
    template_name = 'nurse-workspace.html'

    def get(self, request):
        return render(request, NurseView.template_name)


class InpatientWorkspaceView(View):
    template_name = 'inpatient-workspace.html'

    def get(self, request):
        return render(request, InpatientWorkspaceView.template_name)
