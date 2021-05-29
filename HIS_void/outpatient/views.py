from django.shortcuts import render
from django.utils import timezone
from django.views import View

from laboratory.models import TestItemType


class OutpatientView(View):
    template_name = 'outpatient-workspace.html'

    TEST_ITEMS_CACHE = None
    CACHE_DATE = None

    def get(self, request):
        # 检查是否需要更新缓存
        today = timezone.localdate()
        if OutpatientView.CACHE_DATE is None or OutpatientView.CACHE_DATE < today:
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
                # 存放指定检验类型下的所有检验项目
                content = list(tit.testitem_set.all().values())
                test_items.append({
                    'inspect_type_id': tit.inspect_type_id,
                    "inspect_type_name": tit.inspect_type_name,
                    "content": content
                })
            OutpatientView.TEST_ITEMS_CACHE = test_items
            OutpatientView.CACHE_DATE = today

        context = {"TestItems": OutpatientView.TEST_ITEMS_CACHE}
        return render(request, OutpatientView.template_name, context = context)
