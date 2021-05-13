from django.urls import reverse
from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class NurseView(View):
    template_name = 'nurse-workspace.html'

    def get(self, request):
        data = [
            {"BQ": "A",
             "CW": [1, 3, 4, 5, 6, 7, 8]},
            {"BQ": "B",
             "CW": [2, 3, 4, 5, 6, 7, 8]},
        ]
        return render(request, NurseView.template_name, context={'data': data})


class NurseAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')

        # 医嘱处理信息查询
        if query_information == "YZCL":
            p_no = request.GET.get('p_no')
            print(p_no)
            data = {
                "no": 114514,
                "name": "肖云冲",
                "gender": "男",
                "age": 18,
                "HZZS": "患者主诉文本",
                "ZLQK": "治疗情况文本",
                "JWBS": "既往病史文本",
                "GMBS": "过敏病史文本",
                "TGJC": "体格检查文本",
                "FBSJ": "发病事件文本",
            }

        # 住院患者信息查询
        elif query_information == "ZYHZ":
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

        elif query_information == "RYDJ":
            data = {
                "no": 114514,
                "name": "代收患者姓名",
                "gender": "男",
                "age": 18,
                "HZZS": "患者主诉文本",
                "ZLQK": "治疗情况文本",
                "JWBS": "既往病史文本",
                "GMBS": "过敏病史文本",
                "TGJC": "体格检查文本",
                "FBSJ": "发病事件文本",
            }

        # 待收患者信息查询
        elif query_information == "DSHZ":
            data = [
                {
                    "p_no": "183771**",
                    "name": "李国铭（待收患者）",
                    "status": "危机",
                },
                {
                    "p_no": "183771--",
                    "name": "肖云冲（待收患者）",
                    "status": "普通",
                },
                {
                    "p_no": "183771++",
                    "name": "朱元琛（待收患者）",
                    "status": "安全",
                },
            ]
            # 传入医生主键，这样可以有选择的返回病人信息
            d_no = request.GET.get('d_no')
            print(d_no)

        elif query_information == "CWXX":
            data = [
                {"BQ": "A",
                 "CW": [1, 3, 4, 5, 6, 7, 8]},
                {"BQ": "B",
                 "CW": [5, 6, 7, 8, 9, 10]},
            ]

        return JsonResponse(data, safe=False)

    def post(self, request):
        print("================================")
        print(request.POST.get('SZY'))
        print("================================")

        print("================================")
        print(request.POST.get('RYRQ'))
        print("================================")
        sleep(1)
        return redirect(reverse("nurse-workspace"))
