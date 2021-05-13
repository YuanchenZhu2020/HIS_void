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


# 检中患者数据查询
class InspectionAPI(View):
    def get(self, request):
        query_information = request.GET.get('information')

        # 数据库查询操作
        if query_information == "InspectingInformation":
            p_no = request.GET.get('p_no')
            print(p_no)
            data = {
                "no": 114514,
                "name": "肖云冲",
                "gender": "男",
                "age": 18,
                "JYMC": "血常规",
                "KJSJ": "2021.05.1 20：00",
                "KJYS": "王医生"
            }
        elif query_information == "InspectingPatient":
            data = [
                {
                    "p_no": "183771**",
                    "name": "李国铭",
                    "status": "危机",
                },
                {
                    "p_no": "183771--",
                    "name": "肖云冲",
                    "status": "普通",
                },
                {
                    "p_no": "183771++",
                    "name": "朱元琛",
                    "status": "安全",
                },
            ]
            # 传入医生主键，这样可以有选择的返回病人信息
            d_no = request.GET.get('d_no')
            print(d_no)

        return JsonResponse(data, safe=False)

    def post(self, request):
        print("================================")
        print(request.POST.get('PDXX'))
        print("================================")
        sleep(1)
        return redirect(reverse("inspection-workspace"))
