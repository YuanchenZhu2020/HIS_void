from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View


class OutpatientView(View):
    template_name = 'outpatient-workspace.html'

    def get(self, request):
        # 检验信息数据
        JYXX = [
            {
                'name': "临床检查",
                'content': ['临床检查1', '临床检查2', ]
            },
            {
                'name': "生物化学",
                'content': ['生物化学1', '生物化学2', ]
            },
        ]
        return render(request, OutpatientView.template_name, context={"JYXX": JYXX})


class OutpatientAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')

        # 病历首页信息查询
        if query_information == "BLSY":
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

        # 待诊患者信息查询
        elif query_information == "DZHZ":
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

        # 诊中患者信息查询
        elif query_information == "ZZHZ":
            data = [
                {
                    "p_no": "183771**",
                    "name": "李国铭",
                    "status": "检验完成",
                },
                {
                    "p_no": "183771--",
                    "name": "肖云冲",
                    "status": "待检验",
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

        # 检查结果信息查询
        elif query_information == "JCJY":
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
        # 处方开具
        elif query_information == "CFKJ":
            data = [
                {'name': "多塞平", 'price': 41, 'no': 1, },
                {'name': "多塞平1", 'price': 41, 'no': 2, },
                {'name': "多塞平2", 'price': 41, 'no': 3, },
                {'name': "艾司西酞普兰", 'price': 42, 'no': 4, },
                {'name': "帕罗西汀", 'price': 43, 'no': 5, },
                {'name': "氟西汀", 'price': 44, 'no': 6, },
                {'name': "度洛西汀", 'price': 45, 'no': 7, },
                {'name': "氟伏沙明", 'price': 46, 'no': 8, },
            ]

        return JsonResponse(data, safe=False)

    def post(self, request):
        print("================================")
        print(request.POST)
        print("================================")
        sleep(1)
        return redirect(reverse("outpatient-workspace"))
