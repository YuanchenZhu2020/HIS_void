from django.shortcuts import render
from django.views import View

from laboratory.models import TestItemType


class OutpatientView(View):
    template_name = 'outpatient-workspace.html'

    def get(self, request):
        # 检验信息数据
        # 数据格式示例：
        # [{
        #     'name': "临床检查",
        #     'content': [
        #         ['临床检查1', 价格1],
        #         ['临床检查2', 价格2]
        #        ]
        # }, ...]
        test_items = []
        for tit in TestItemType.objects.all():
            content = []  # 存放指定检验类型的所有检验项目
            for i in range(len(tit.testitem_set.all().values_list('inspect_price'))):
                content.append({
                    'inspect_name': tit.testitem_set.all().values_list('inspect_name')[i][0],
                    'inspect_price': tit.testitem_set.all().values_list('inspect_price')[i][0],
                    'inspect_id': tit.testitem_set.all().values_list('inspect_id')[i][0]
                })
            test_items.append(
                {
                    'inspect_type_id': tit.inspect_type_id,
                    "inspect_type_name": tit.inspect_type_name,
                    "content": content
                }
            )
        context = {"TestItems": test_items}
        return render(request, OutpatientView.template_name, context=context)
