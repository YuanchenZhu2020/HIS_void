from django.shortcuts import render
from django.utils import timezone
from django.views import View

from his.models import Department, Staff, DutyRoster
from laboratory.models import TestItemType


class NurseView(View):
    template_name = 'nurse-workspace.html'

    def get(self, request):
        return render(request, NurseView.template_name)


class InpatientWorkspaceView(View):
    template_name = 'inpatient-workspace.html'

    TEST_ITEMS_CACHE = None
    CACHE_DATE = None

    def get(self, request):
        # 检查是否需要更新缓存
        today = timezone.localdate()
        if InpatientWorkspaceView.CACHE_DATE is None or InpatientWorkspaceView.CACHE_DATE < today:
            test_items = []
            for tit in TestItemType.objects.all():
                # 存放指定检验类型下的所有检验项目
                content = list(tit.testitem_set.all().values())
                test_items.append({
                    'inspect_type_id': tit.inspect_type_id,
                    "inspect_type_name": tit.inspect_type_name,
                    "content": content
                })
            InpatientWorkspaceView.TEST_ITEMS_CACHE = test_items
            InpatientWorkspaceView.CACHE_DATE = today

        username = request.session.get('username')
        nurse_info = Staff.objects.filter(user_id=username).values_list(
            'dept__usergroup__ug_id',
            'dept__usergroup__name')
        area = DutyRoster.objects.filter(working_day=timezone.now().weekday(), medical_staff_id=username)
        area = 'B'
        context = {
                "TestItems": InpatientWorkspaceView.TEST_ITEMS_CACHE,
                "area": area,
                'dept_id': nurse_info[0][0],
                'dept_name': nurse_info[0][1]
            }

        return render(request, InpatientWorkspaceView.template_name, context=context)
