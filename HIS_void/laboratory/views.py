from django.urls import reverse
from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class InspectionView(View):
    template_name = 'inspection-workspace.html'

    def get(self, request):
        return render(request, InspectionView.template_name)
