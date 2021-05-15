from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from his.models import Department, DeptAreaBed
from inpatient.models import HospitalRegistration


class OutpatientAPI(View):
    """
    门诊医生工作台数据查询API
    """
    def get(self, request):
        query_key_to_func = {
            # 病历首页信息查询
            "BLSY": self.query_medical_record,
            # 待诊患者信息查询
            "DZHZ": self.query_waiting_diagnosis_patients,
            # 诊中患者信息查询
            "ZZHZ": self.query_in_diagnosis_patients,
            # 检查结果信息查询
            "JCJY": self.query_inspect_result,
            # 处方开具，药品检索
            "CFKJ": self.query_medicine,
        }
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')
        data = query_key_to_func.get(query_information)(request)
        return JsonResponse(data, safe=False)

    def query_medical_record(self, request):
        patient_id = request.GET.get('patient_id')
        print(patient_id)
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
        return data

    def query_waiting_diagnosis_patients(self, request):
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
        return data

    def query_in_diagnosis_patients(self, request):
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
        return data

    def query_inspect_result(self, request):
        data = []
        return data

    def query_medicine(self, request):
        data = [
            {'name': "多塞平", 'price': 41, 'number': 100, },
            {'name': "艾司西酞普兰", 'price': 42, 'number': 100, },
            {'name': "帕罗西汀", 'price': 43, 'number': 100, },
            {'name': "氟西汀", 'price': 44, 'number': 100, },
            {'name': "度洛西汀", 'price': 45, 'number': 100, },
            {'name': "氟伏沙明", 'price': 46, 'number': 100, },
        ]
        return data

    def post(self, request):
        print("================================")
        print(request.POST)
        print("================================")
        sleep(1)
        return redirect(reverse("outpatient-workspace"))


class NurseAPI(View):
    """
    护士工作站数据查询API
    """
    def get(self, request):
        query_key_to_func = {
            # 医嘱处理信息查询
            "MEDICAL_ADVICE_QUERY": self.query_medical_advice_process,
            # 住院患者信息查询
            "INPATIENTS_QUERY": self.query_inpatients,
            # 患者入院登记基础信息查询
            "REGISTER_QUERY": self.query_register_patient_info,
            # 待收患者信息查询
            "WAITING_QUERY": self.query_waiting_patients,
            # 空床位查询
            "BED_QUERY": self.query_empty_beds
        }
        
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')
        data = query_key_to_func.get(query_information)(request)
        return JsonResponse(data, safe = False)

    def query_medical_advice_process(self, request):
        patient_id = request.GET.get('patient_id')
        print(patient_id)
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
        return data

    def query_inpatients(self, request):
        data = [
            {
                "pid": "183771**",
                "name": "李国铭",
                "status": "危机",
            },
            {
                "pid": "183771--",
                "name": "肖云冲",
                "status": "普通",
            },
            {
                "pid": "183771++",
                "name": "朱元琛",
                "status": "安全",
            },
        ]
        # 传入医生主键，这样可以有选择的返回病人信息
        d_no = request.GET.get('d_no')
        print(d_no)
        return data

    def query_register_patient_info(self, request):
        data = {
            "no": 114514,
            "name": "代收患者姓名",
            "gender": "男",
            "age": 18
        }
        return data

    def query_waiting_patients(self, request):
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
        return data

    def query_empty_beds(self, request):
        # 数据示例：{"AREA": "A","BED": [1, 3, 4, 5, 6]}
        inpatient_area_info = []
        nurse_dept = Department.objects.get_by_dept_id(request.session["dept_id"])
        area_beds = DeptAreaBed.objects.filter(
            dept = nurse_dept
        ).values_list("area", "bed_id")
        used_beds = HospitalRegistration.objects.filter(
            dept = nurse_dept
        ).values_list("area", "bed_id")
        empty_beds = set(area_beds) - set(used_beds)
        areas = sorted(list(dict(empty_beds).keys()))
        for area in areas:
            inpatient_area_info.append(
                {
                    "AREA": area,
                    "BED": sorted([ab[1] for ab in filter(lambda ab: ab[0] == area, empty_beds)])
                }
            )
        return inpatient_area_info

    def post(self, request):
        print("================================")
        print(request.POST.get('SZY'))
        print("================================")

        print("================================")
        print(request.POST.get('RYRQ'))
        print("================================")
        sleep(1)
        return redirect(reverse("nurse-workspace"))


class InspectionAPI(View):
    """
    检中患者数据查询API
    """
    def get(self, request):
        query_key_to_func = {
            "InspectingInformation": self.query_inspecting_info,
            "InspectingPatient": self.query_inspecting_patient
        }
        query_information = request.GET.get('information')
        data = query_key_to_func.get(query_information)(request)
        return JsonResponse(data, safe=False)

    def query_inspecting_info(self, request):
        p_no = request.GET.get('p_no')
        data = {
            "no": 114514,
            "name": "肖云冲",
            "gender": "男",
            "age": 18,
            "JYMC": "血常规",
            "KJSJ": "2021.05.1 20：00",
            "KJYS": "王医生"
        }
        return data

    def query_inspecting_patient(self, request):
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
        return data

    def post(self, request):
        print("================================")
        print(request.POST.get('PDXX'))
        print("================================")
        sleep(1)
        return redirect(reverse("inspection-workspace"))
