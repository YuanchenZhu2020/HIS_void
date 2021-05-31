import datetime
import json
from time import sleep

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone, dateparse
from django.utils.decorators import method_decorator
from django.views import View

from his.models import Department, DeptAreaBed, Staff
from inpatient.models import HospitalRegistration
from outpatient.models import RemainingRegistration, RegistrationInfo
from patient.models import PatientUser
from rbac.decorators import patient_login_required
from pharmacy.models import MedicineInfo
from laboratory.models import PatientTestItem


def get_current_reg_time():
    # 获取本地日期时间
    now_datetime = timezone.localtime()
    TARGET_REG_TIME = dateparse.parse_time("08:00:00")
    if now_datetime.time() > dateparse.parse_time("12:00:00"):
        TARGET_REG_TIME = dateparse.parse_time("13:00:00")
    return TARGET_REG_TIME

class OutpatientAPI(View):
    """
    门诊医生工作台数据查询API
    """

    # region OutpatientAPI get部分
    def get(self, request):
        query_key_to_func = {
            # 病历首页信息查询
            "BLSY": self.query_medical_record,
            # 待诊患者信息查询
            "waiting_diagnosis": self.query_waiting_diagnosis_patients,
            # 诊中患者信息查询
            "in_diagnosis": self.query_in_diagnosis_patients,
            # 检查结果信息查询
            "test_results": self.query_inspect_result,
            # 处方开具，药品检索
            "CFKJ": self.query_medicine,
            # 待诊患者基础信息
            "waiting_diagnosis_patient_info": self.query_waiting_diagnosis_patient_info,
            # 诊中患者基础信息
            "in_diagnosis_patient_info": self.query_in_diagnosis_patient_info
        }
        # 获取需要查询的信息类型
        query_information = request.GET.get('get_param')
        data = query_key_to_func.get(query_information)(request)
        return JsonResponse(data, safe=False)

    # 病历首页查询
    def query_medical_record(self, request):
        regis_id = request.GET.get('regis_id')
        regis_info = RegistrationInfo.objects.get(id=regis_id)
        data = {
            'chief_complaint': regis_info.chief_complaint,
            'allegic_history': regis_info.patient.allegic_history,
            'past_illness': regis_info.patient.past_illness,
            'illness_date': regis_info.illness_date}
        return data

    # 待诊患者基础信息查询
    def query_waiting_diagnosis_patient_info(self, request):
        regis_id = request.GET.get('regis_id')
        regis_info = RegistrationInfo.objects.get(id=regis_id)
        print("=======START outpatientAPI GET========")
        print(regis_info.__dict__)
        print(regis_info.patient.__dict__)
        print("========END outpatientAPI GET========")
        gender_convert = ["男", "女"]
        data = {
            'no': regis_info.patient.patient_id,
            'name': regis_info.patient.name,
            'gender': gender_convert[regis_info.patient.gender],
            'age': (timezone.now().date() - regis_info.patient.birthday).days // 365,
        }
        return data
        pass
    def query_in_diagnosis_patient_info(self, request):
        data = {
            '心肺听诊': '水肿,粪便可见嗜酸性WBC',
            '脑CT': '镜下镰形细胞,粘液变性',
            '粪便常规': '粪便可见RBC'
        }
        return data

    # 待诊患者查询
    def query_waiting_diagnosis_patients(self, request):
        """
        查询待诊患者。

        数据格式示例：[{
            "regis_id": "1",
            "name": "李国铭",
            "gender": "男",
        },...]
        """
        staff_id = request.session["username"]
        TARGET_REG_TIME = get_current_reg_time()
        # 查询指定医生在当前就诊时段的所有还没有开始诊疗的患者
        # 即：匹配医生ID、日期、时间，并且患者主诉为空
        regis_info = RegistrationInfo.objects.filter(
            medical_staff__user__username = staff_id,
            registration_date__time = TARGET_REG_TIME,
            registration_date__date = timezone.localdate(),
            chief_complaint__isnull = True,
        ).values_list(
            "id", "patient__name", "patient__gender"
        )
        data = []
        gender_convert = dict(PatientUser.SEX_ITEMS)
        for regis in regis_info:
            # 医生工作4个小时
            patient_details = dict(zip(
                ['id', 'name', 'gender'],
                [regis[0], regis[1], gender_convert[regis[2]]]
            ))
            data.append(patient_details)
            # print(patient_details)
        print("医生编号", staff_id)
        return data

    # 诊中患者查询
    def query_in_diagnosis_patients(self, request):
        staff_id = request.session["username"]
        TARGET_REG_TIME = get_current_reg_time()
        # 查询指定医生在当前就诊时段的所有开始诊疗但还没确诊的患者
        # 即：匹配医生ID、日期、时间，并且患者已经进行了主诉，但确诊结果为空
        regis_info = RegistrationInfo.objects.filter(
            medical_staff__user__username = staff_id,
            chief_complaint__isnull = False,
            diagnosis_results__isnull = True,
        ).values_list(
            "id", "patient__name", "patient__gender"
        )
        data = []
        gender_convert = dict(PatientUser.SEX_ITEMS)
        for regis in regis_info:
            patient_details = dict(zip(
                ['regis_id', 'name', 'gender'],
                [regis[0], regis[1], gender_convert[regis[2]]]
            ))
            data.append(patient_details)
            # print(patient_details)
        print("医生编号", staff_id)
        return data

    # 检查结果查询
    def query_inspect_result(self, request):
        data = {
            '心肺听诊': '水肿,粪便可见嗜酸性WBC',
            '脑CT': '镜下镰形细胞,粘液变性',
            '粪便常规': '粪便可见RBC'
        }
        return data

    # 药品查询（已完成）
    def query_medicine(self, request):
        with transaction.atomic():
            # 在with代码块中写事务操作
            all_medicines = MedicineInfo.objects.all().values_list(
                "medicine_id", "medicine_name", "retail_price"
            )
            data = []
            for medicine in all_medicines:
                data.append(dict(zip(
                    ["no", "name", "price"],
                    medicine
                )))
        return data

    # endregion

    # region OutpatientAPI post部分
    def post(self, request):
        query_key_to_func = {
            # 检查项目提交
            "inspection": self.post_inspection,
            # 病历首页提交
            "history_sheet": self.post_history_sheet,
            # 药品及医嘱提交
            "medicine": self.post_medicine,
            "diagnosis_results": self.post_diagnosis_results
        }
        data = request.POST
        post_param = data['post_param']
        # 输出提示信息
        print("==========START outpatientAPI POST==========")
        print('【request.POST】', data)
        print('【post_param】', data['post_param'])
        print("==========END outpatientAPI POST==========")
        ''' 
        param对照表:
        medicine -> 处方开具选择的药品
        inspection -> 检验信息
        history_sheet -> 病历首页
        '''
        # 根据参数直接映射对应的函数，并执行
        query_key_to_func[post_param](data)

        # 这条语句并不会使页面刷新
        return redirect(reverse("outpatient-workspace"))

    # 提交病历首页部分
    def post_history_sheet(self, data):
        """ 【request.POST】内容
        <QueryDict: {
            'regis_id': ['19'],
            'post_param': ['history_sheet'],
            'chief_complaint': ['患者主诉文本'],
            'past_illness': ['既往病史文本'],
            'allegic_history': ['过敏病史文本'],
            'illness_date': ['2021-05-25']
        }>
        """
        with transaction.atomic():  # 事务原子性保证
            pass  # 病历首页数据库操作
            ''' 我的之前的存储代码，后端人员可以重新编写
            RegistrationInfo.objects.filter(
                id=data['regis_id']
            ).update(
                chief_complaint=data['chief_complaint'],
                illness_date=data['illness_date']
            )
            PatientUser.objects.filter(
                registrations__id=data['regis_id']
            ).update(
                allegic_history=data['allegic_history'],
                past_illness=data['past_illness']
            )
            print("========= 挂号信息 ==========")
            print(RegistrationInfo.objects.filter(
                id=data['regis_id']
            ))
            '''

    # 检查检验部分
    def post_inspection(self, data):
        """【request.POST】内容
         <QueryDict: {
            'regis_id': ['19'],
            'post_param': ['inspection'],
            '1': ['1', '4', '6'],
            '2': ['16'],
            '3': ['63'],
            '5': ['40', '49']
        }>
        """
        with transaction.atomic():  # 事务原子性保证
            pass  # 检查检验据库操作

    # 确诊结果
    def post_diagnosis_results(self, data):
        """【request.POST】
        <QueryDict: {
            'regis_id': ['19'],
            'post_param': ['diagnosis_results'],
            'diagnosis_results': ['门诊确诊文本']
        }>
        """
        with transaction.atomic():  # 事务原子性保证
            pass  # 检查检验据库操作

    # 药品信息、医嘱建议
    def post_medicine(self, data):
        """【request.POST】
        <QueryDict: {
            'medicine_data[0][medicine_id]': ['A00255'],
            'medicine_data[0][medicine_num]': ['2'],
            'medicine_data[1][medicine_id]': ['A00596'],
            'medicine_data[1][medicine_num]': ['1'],
            'post_param': ['medicine'],
            'medical_advice': ['用药建议、医嘱建议文本'],
            'regis_id': ['19']
        }>
        """
        with transaction.atomic():  # 事务原子性保证
            pass  # 检查检验据库操作

    # endregion


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
        return JsonResponse(data, safe=False)

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
            dept=nurse_dept
        ).values_list("area", "bed_id")
        used_beds = HospitalRegistration.objects.filter(
            dept=nurse_dept
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


@method_decorator(patient_login_required(login_url = "/login-patient/"), name = "post")
class PatientRegisterAPI(View):
    """
    患者挂号查询与提交API
    """
    SUBMIT_URL_NAME = "PatientRegisterAPI"
    patient_next_url_name = "patient-details"

    def query_registration_info(self, request):
        # 数据格式示例：[{
        #     "doctor_id": "999",
        #     "doctor_name": "lisa",
        #     "AM": 3,
        #     "PM": 4,
        # },...]
        reg_date = request.GET.get('date')
        reg_datetime = {
            "AM": dateparse.parse_datetime(reg_date + " 08:00:00").astimezone(timezone.utc), 
            "PM": dateparse.parse_datetime(reg_date + " 13:00:00").astimezone(timezone.utc)
        }
        dept_id = int(request.GET.get('KS_id'))
        reginfo_detail = RemainingRegistration.objects.filter(
            medical_staff__dept__usergroup__ug_id = dept_id,
            register_date__in = reg_datetime.values()
        ).values_list(
            "medical_staff__user__username",
            "medical_staff__name",
            "register_date",
            "remain_quantity",
        )
        doctor_info = reginfo_detail.values_list(
            "medical_staff__user__username",
            "medical_staff__name"
        ).distinct()
        reginfo = []
        for regdetail in doctor_info:
            doc_reg = {
                "doctor_id": regdetail[0],
                "doctor_name": regdetail[1],
                "AM": reginfo_detail.filter(
                        medical_staff__user__username = regdetail[0],
                        register_date = reg_datetime["AM"]
                    ).values_list("remain_quantity", flat = True)[0],
                "PM": reginfo_detail.filter(
                        medical_staff__user__username = regdetail[0],
                        register_date = reg_datetime["PM"]
                    ).values_list("remain_quantity", flat = True)[0],
            }
            reginfo.append(doc_reg)
        return reginfo

    def get(self, request):
        # 挂号信息查询
        query_data = self.query_registration_info(request)
        # 动态获取 crsf_token
        from django.middleware.csrf import get_token
        token = get_token(request)
        data = {
            "query_data": query_data, 
            "token": token, 
            "submit_url": reverse(PatientRegisterAPI.SUBMIT_URL_NAME)
        }
        return JsonResponse(data, safe = False)

    def post(self, request):
        reg_info = json.loads(request.body.decode())
        reg_info["reg_datetime"] = timezone.make_aware(
            dateparse.parse_datetime(reg_info["reg_datetime"])
        ).astimezone(timezone.utc)
        reg_info["is_emergency"] = Staff.objects.get_by_user(
            reg_info["doctor_id"]
        ).dept == Department.objects.get_by_dept_name("急诊科")
        with transaction.atomic():
            # 更新剩余挂号数
            remain_reg_record = RemainingRegistration.objects.get(
                medical_staff__user__username = reg_info["doctor_id"],
                register_date = reg_info["reg_datetime"]
            )
            remain_reg_record.remain_quantity = remain_reg_record.remain_quantity - 1
            remain_reg_record.save()
            # 写入挂号信息
            patient_id = request.session["patient_id"]
            patient = PatientUser.objects.get_by_patient_id(patient_id)
            doctor = Staff.objects.get_by_user(reg_info["doctor_id"])
            reg_id = patient.registration_set.count() + 1
            reg_record = RegistrationInfo.objects.create(
                patient = patient,
                reg_id = reg_id,
                medical_staff = doctor,
                registration_date = reg_info["reg_datetime"],
                reg_class = 1 if reg_info["is_emergency"] else 0
            )
        return JsonResponse(
            {"status": True, "redirect_url": reverse(PatientRegisterAPI.patient_next_url_name)}, 
            safe = False
        )


@method_decorator(patient_login_required(login_url = "/login-patient/"), name = "post")
class PatientFastRegisterAPI(PatientRegisterAPI):
    """
    患者详情页面API，主要用于查询指定医生挂号信息，以便患者快速挂号
    """
    SUBMIT_URL_NAME = "PatientFastRegisterAPI"
    patient_next_url_name = "patient-details"

    def query_registration_info(self, request):
        doctor_id = request.GET.get("doctor_id")
        reg_date = request.GET.get("reg_date")
        reg_datetime = {
            "AM": dateparse.parse_datetime(reg_date + " 08:00:00").astimezone(timezone.utc), 
            "PM": dateparse.parse_datetime(reg_date + " 13:00:00").astimezone(timezone.utc)
        }
        reginfo_detail = RemainingRegistration.objects.filter(
            medical_staff__user__username = doctor_id,
            register_date__in = reg_datetime.values(),
        )
        doc_reg = None
        if len(reginfo_detail) > 0:
            doc_reg = {
                "dept_name": reginfo_detail.values_list(
                        "medical_staff__dept__usergroup__name",
                        flat = True,
                    ).distinct()[0],
                "AM": reginfo_detail.filter(
                        register_date = reg_datetime["AM"]
                    ).values_list("remain_quantity", flat = True)[0],
                "PM": reginfo_detail.filter(
                        register_date = reg_datetime["PM"]
                    ).values_list("remain_quantity", flat = True)[0],
            }
        return doc_reg


@method_decorator(patient_login_required(login_url = "/login-patient/"), name = "get")
class PatientTreatmentDetails(View):
    """
    患者治疗详情查询API，包括挂号详情、检查详情
    """

    def query_dianosis_detail(self, request):
        patient_id = int(request.session["patient_id"])
        patient = PatientUser.objects.get_by_patient_id(patient_id)
        reg_id = request.GET.get("reg_id")
        reg_info = RegistrationInfo.objects.filter(patient = patient, reg_id = reg_id).values_list(
            "medical_staff__name",
            "appointment_date",
            "registration_date",
            "reg_class",
            "illness_date",
            "chief_complaint",
            "diagnosis_results",
        )[0]
        reg_info = dict(zip(
            [
                "reg_id", "doctor_name", "ap_date", "reg_date", "reg_class", 
                "ill_date", "chief_complaint", "diag_result"
            ],
            (reg_id,) + reg_info
        ))
        reg_info["reg_class"] = "普通门诊" if reg_info["reg_class"] == 0 else "急诊"
        # print(timezone.make_naive(reg_info["ap_date"]))
        ap_date = timezone.make_naive(reg_info["ap_date"])
        reg_info["ap_date"] = "{0.year}年{0.month:>02d}月{0.day:>02d}日".format(ap_date) + " " + ap_date.strftime("%H:%M:%S")
        return reg_info

    def query_check_detail(self, request):
        patient_id = int(request.session["patient_id"])
        patient = PatientUser.objects.get_by_patient_id(patient_id)
        reg_id = request.GET.get("reg_id")
        test_id = request.GET.get("test_id")
        test_info = PatientTestItem.objects.filter(
            registration_info__patient = patient, 
            registration_info__reg_id = reg_id, 
            test_id = test_id
        ).values_list(
            "test_item__inspect_name", 
            "handle_staff__name",
            "issue_time", 
            "test_results",
        )[0]
        test_info = dict(zip(
            ["reg_id", "test_id", "test_name", "doctor_name", "issue_date", "result"],
            (reg_id, test_id) + test_info
        ))
        if test_info["result"] is None:
            test_info["result"] = "（等待结果中）"
        issue_date = timezone.make_naive(test_info["issue_date"])
        test_info["issue_date"] = "{0.year}年{0.month:>02d}月{0.day:>02d}日".format(issue_date)
        return test_info

    def get(self, request):
        query_key_to_func = {
            # 挂号详情查询
            "REG": self.query_dianosis_detail,
            # 检查详情查询
            "CHE": self.query_check_detail,
        }
        query_key = request.GET.get("type")

        data = query_key_to_func[query_key](request)
        return JsonResponse(data, safe = False)


# 病人基础信息API，用于医生获取病人基础数据
class PatientUserAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')
        data = {}
        # 确诊详情信息查询
        if query_information == "QZXQ":
            quezhen_no = request.GET.get('p_no')
            print("--------------------")
            print(quezhen_no)
            print("--------------------")
            # 给出能给的尽量多的信息就行，以下只是示例
            data = {
                "no": 114514,
                "name": "CCC",
                "gender": "男",
                "age": 18,
                "HZZS": "患者主诉文本",
                "TGJC": "体格检查文本",
                "FBSJ": "发病事件文本",
                "QZ": "确诊文本",
            }

        # 检查详情查询
        elif query_information == "JCXQ":
            pass

        elif query_information == "XXXX":
            pass

        return JsonResponse(data, safe=False)


# 住院医生工作台数据
class InpatientAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('get_param')

        #
        if query_information == "ZZHZ":
            p_no = request.GET.get('p_no')
            print(p_no)
            # 数据库查询语句
            data = [{
                "p_no": 114514,
                "name": "发多冲",
                "bed": 123,
            }, {
                "p_no": 11343,
                "name": "肖大赛",
                "bed": 543,
            }, {
                "p_no": 114424,
                "name": "阿凡达",
                "bed": 64,
            }]
        return JsonResponse(data, safe=False)
