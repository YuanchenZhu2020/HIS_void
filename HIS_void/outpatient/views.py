from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from laboratory.models import TestItemType


class OutpatientView(View):
    template_name = 'outpatient-workspace.html'

    def get(self, request):
        # 检验信息数据
        # 数据格式示例：
        # [{
        #     'name': "临床检查",
        #     'content': ['临床检查1', '临床检查2', ]
        # }, ...]
        test_items = []
        for tit in TestItemType.objects.all():
            test_items.append(
                {
                    "name": tit.inspect_type_name,
                    "content": [
                        tituple[0]
                        for tituple in tit.testitem_set.all().values_list("inspect_name")
                    ]
                }
            )
        context = {"TestItems": test_items}
        return render(request, OutpatientView.template_name, context = context)
