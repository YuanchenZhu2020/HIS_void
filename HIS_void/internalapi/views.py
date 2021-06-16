import json
from time import sleep
import uuid

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone, dateparse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from his.models import Department, DeptAreaBed, Staff
from inpatient.models import HospitalRegistration, NursingRecord
from outpatient.models import RemainingRegistration, RegistrationInfo, Prescription, PrescriptionDetail
from patient.models import PatientUser
from rbac.decorators import patient_login_required
from pharmacy.models import MedicineInfo
from laboratory.models import PatientTestItem
from internalapi.models import PaymentRecord
from externalapi.external_api import AlipayClient
from django.core.paginator import Paginator

from patient.validators import PhoneNumberValidator


def get_current_reg_time():
    # 获取本地日期时间
    now_datetime = timezone.localtime()
    TARGET_REG_TIME = dateparse.parse_time("08:00:00")
    if now_datetime.time() > dateparse.parse_time("12:00:00"):
        TARGET_REG_TIME = dateparse.parse_time("13:00:00")
    return TARGET_REG_TIME

# def null_string_to_none(string):
#     return None if string.strip() == '' else string.strip()


class OutpatientAPI(View):
    """
    门诊医生工作台数据查询API
    """
    MEDICINE_INFO_CACHE = None
    UPDATE_DATE = None

    # region OutpatientAPI GET
    def get(self, request):
        query_key_to_func = {
            # 病历首页信息查询
            "history_sheet": self.query_history_sheet,
            # 待诊患者信息查询
            "waiting_diagnosis": self.query_waiting_diagnosis_patients,
            # 诊中患者信息查询
            "in_diagnosis": self.query_in_diagnosis_patients,
            # 检查结果信息查询
            "test_results": self.query_inspect_result,
            # 处方开具，药品检索
            "medicine_info": self.query_medicine_info,
            # 患者基础信息查询
            "patient_base_info": self.query_patient_base_info,
            # 确诊结果查询
            "diagnosis_results": self.query_diagnosis_results,
            # 医嘱查询
            "medical_advice": self.query_medical_advice,
            # 入院申请
            "application_inhospital": self.application_inhospital,
            # 诊疗结束
            'diagnosis_over': self.diagnosis_over,
        }
        # 获取需要查询的信息类型
        query_information = request.GET.get('get_param')
        data = query_key_to_func.get(query_information)(request)
        print('====== OutpatientAPI GET ======')
        print('【request.GET】', request.GET)
        print('【regis_id】', request.GET.get('regis_id'))
        print('====== OutpatientAPI GET ======')
        return JsonResponse(data, safe=False)

    def query_history_sheet(self, request):
        """ 病历首页查询 """
        regis_id = request.GET.get('regis_id')
        regis_info = RegistrationInfo.objects.get(id = regis_id)
        data = {
            'chief_complaint': regis_info.chief_complaint,
            'allegic_history': regis_info.patient.allegic_history,
            'past_illness': regis_info.patient.past_illness,
            'illness_date': regis_info.illness_date
        }
        return data

    def query_waiting_diagnosis_patients(self, request):
        """ 待诊患者查询 """
        staff_id = request.session["username"]
        TARGET_REG_TIME = get_current_reg_time()
        # 查询指定医生在当前就诊时段的所有还没有开始诊疗的患者
        # 即：匹配医生ID、日期、时间，并且患者主诉为空
        # 查询挂号数据
        regis_info = RegistrationInfo.objects.filter(
            diagnosis_status = 0,  # 判断诊断结果为待诊
            medical_staff__user__username = staff_id,  # 指定门诊医生
            registration_date__time = TARGET_REG_TIME,  # 判断上下午
            registration_date__date = timezone.localdate(),  # 当天
        ).values_list(
            "id", "patient__name", "patient__gender"
        )
        data = []
        gender_convert = dict(PatientUser.SEX_ITEMS)
        for regis in regis_info:
            patient_details = dict(zip(
                ['id', 'name', 'gender'],
                [regis[0], regis[1], gender_convert[regis[2]]]
            ))
            data.append(patient_details)
        # print("医生编号", staff_id)
        return data

    def query_patient_base_info(self, request):
        """ 患者基础信息查询 """
        regis_id = request.GET.get('regis_id')
        regis_info = RegistrationInfo.objects.get(id = regis_id)
        data = {
            'no': regis_info.patient.patient_id,
            'name': regis_info.patient.name,
            'gender': regis_info.patient.get_gender_display(),
            'age': timezone.now().year - regis_info.patient.birthday.year,
        }
        return data

    def query_in_diagnosis_patients(self, request):
        """ 诊中患者查询 """
        staff_id = request.session["username"]
        data = []
        # 诊中患者，筛选条件为 diagnosis_status 为 1，同时指定挂号医生
        regis_info = RegistrationInfo.objects.filter(
            medical_staff__user__username = staff_id,  # 指定挂号医生
            diagnosis_status = 1  # 诊断状态为诊中
        )
        for regis in regis_info:
            # 找到该挂号下所有的检验信息
            all_test_info = PatientTestItem.objects.filter(
                registration_info_id=regis.id,  # 该挂号的所有检验
            )
            # 初始化总检验项目及已完成检验项目
            all_test_num = finished_test_num = 0
            for test_info in all_test_info:
                all_test_num += 1
                if test_info.test_results is not None:
                    finished_test_num += 1
            data.append({
                "regis_id": regis.id,
                "name": regis.patient.name,
                "progress": (finished_test_num / all_test_num) * 100
            })
        return data

    def query_inspect_result(self, request):
        """ 检查结果查询 """
        regis_id = request.GET.get('regis_id')
        tests_info = PatientTestItem.objects.filter(
            registration_info_id = regis_id
        ).values_list(
            'test_item__inspect_type__inspect_type_name',
            'test_item__inspect_name',
            'test_item__inspect_price',
            'test_results'
        )
        data = []
        for test in tests_info:
            data.append(dict(zip(
                ["inspect_type_name", "inspect_name", "inspect_price", "test_results"],
                test
            )))
        # print(data)
        return data

    def query_diagnosis_results(self, request):
        """ 确诊结果查询 """
        regis_id = request.GET.get('regis_id')
        regis_info = RegistrationInfo.objects.get(id = regis_id)
        data = {"diagnosis_results": regis_info.diagnosis_results}
        return data

    def query_medicine_info(self, request):
        """ 药品查询 """
        if OutpatientAPI.UPDATE_DATE is None or OutpatientAPI.UPDATE_DATE < timezone.localdate():
            all_medicines = MedicineInfo.objects.all().values_list(
                "medicine_id", "medicine_name", "retail_price"
            )
            data = []
            for medicine in all_medicines:
                data.append(dict(zip(
                    ["medicine_info_id", "medicine_name", "retail_price"],
                    medicine
                )))
            OutpatientAPI.MEDICINE_INFO_CACHE = data
        return OutpatientAPI.MEDICINE_INFO_CACHE

    def query_medical_advice(self, request):
        regis_id = request.GET.get('regis_id')
        data = {'medical_advice': None, 'medicine': []}
        prescription = Prescription.objects.filter(registration_info_id = regis_id)
        if prescription.exists():
            medicine_info = PrescriptionDetail.objects.filter(
                prescription_info_id = prescription.id
            ).values_list(
                'medicine_info_id', 'medicine_quantity',
                'medicine_info__medicine_name', 'medicine_info__retail_price'
            )
            medicine = []
            for val in medicine_info:
                medicine.append(dict(zip(
                    ['medicine_info_id', 'medicine_quantity', 'medicine_name', 'retail_price'],
                    val
                )))
            data = {
                "medical_advice": prescription.medical_advice,
                "medicine": medicine
            }
        return data

    def application_inhospital(self, request):
        """ 创建入院申请记录，更新挂号信息中的就诊状态 """
        regis_id = request.GET.get('regis_id')
        dept_id = request.GET.get('dept_id')
        # 病人在住院时需要有门诊的确诊结果作为预诊结果
        regis_info = RegistrationInfo.objects.get(id = regis_id)
        if not regis_info.diagnosis_results:
            return {'status': -1, 'message': '请先提交预诊结果再进行转院操作！'}

        with transaction.atomic():
            HospitalRegistration.objects.create(
                dept_id = dept_id,
                registration_info_id = regis_id
            )
            RegistrationInfo.objects.filter(
                id = regis_id
            ).update(diagnosis_status = 2)
        return {'status': 0, 'message': '已移交至住院部！'}

    def diagnosis_over(self, request):
        regis_id = request.GET.get('regis_id')
        regis_info = RegistrationInfo.objects.get(id = regis_id)
        # 先判断是否存在患者主诉
        if not regis_info.chief_complaint:
            return {'status': -1, 'message': '尚不存在患者主诉！'}
        elif not regis_info.diagnosis_results:
            return {'status': -1, 'message': '尚不存在确诊结果！'}
        else:
            with transaction.atomic():
                RegistrationInfo.objects.filter(
                    id = regis_id
                ).update(diagnosis_status = 2)
            return {'status': 0, 'message': '诊疗完毕！'}

    # endregion

    # region OutpatientAPI POST
    def post(self, request):
        post_key_to_func = {
            # 检查项目提交
            "inspection": self.post_inspection,
            # 病历首页提交
            "history_sheet": self.post_history_sheet,
            # 药品及医嘱提交
            "medicine": self.post_medicine,
            # 诊断结果提交
            "diagnosis_results": self.post_diagnosis_results,
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
        data = post_key_to_func[post_param](request)
        return JsonResponse(data, safe=False)

    def post_history_sheet(self, request):
        """
        提交病历首页
        """
        callback = {'status': -1, 'message': '未知原因提交失败！'} # 默认的提交失败提示可以修改
        regis_id = request.POST.get('regis_id')
        chief_complaint = request.POST.get('chief_complaint')
        illness_date = dateparse.parse_date(request.POST.get('illness_date'))
        allegic_history = request.POST.get('allegic_history')
        past_illness = request.POST.get('past_illness')
        # 判断是否存在患者主诉
        if not chief_complaint:
            callback['message'] = '未填写患者主诉！'
            return callback
        # 判断是否存在发病时间
        elif not illness_date:
            callback['message'] = '未填写发病时间！'
            return callback
        with transaction.atomic():
            RegistrationInfo.objects.filter(
                id = regis_id
            ).update(
                chief_complaint = chief_complaint or None,  # 将空字符串转换为None，不用再定义专门的函数 null_string_to_none
                illness_date = illness_date or None  # 将空字符串转换为None，不用再定义专门的函数 null_string_to_none
            )
            PatientUser.objects.filter(
                registrations__id = regis_id
            ).update(
                allegic_history = allegic_history or None,
                past_illness = past_illness or None
            )
            callback['status'] = 1
            callback['message'] = '病历首页提交成功！'
            return callback

    def post_inspection(self, request):
        """
        提交检查检验
        """
        regis_id = request.POST.get('regis_id')
        data = dict(request.POST)
        callback = {'status': -1, 'message': '请至少选择一个检验项目！'}
        with transaction.atomic():
            test_id = PatientTestItem.objects.filter(registration_info_id = regis_id).count()
            for param in data:
                if param not in ('post_param', 'regis_id'):
                    for test_item in data[param]:
                        callback['status'] = 0
                        callback['message'] = '检验项目已更新'
                        test_id += 1
                        PatientTestItem.objects.create(
                            test_id = test_id,
                            registration_info_id = regis_id,
                            test_item_id = test_item,
                            payment_status = 0,
                            inspect_status = 0
                        )
            # 之前的逻辑有问题，虽然提示了未选择检验项目，但仍将就诊状态修改为1，即没有检验却变成检中患者
            if callback['status'] == -1:
                return callback
            else:
                RegistrationInfo.objects.filter(
                    id=regis_id
                ).update(diagnosis_status=1)
                return callback

    def post_diagnosis_results(self, request):
        """
        提交确诊结果
        """
        callback = {'status': -1, 'message': '未填写确诊信息！'}
        regis_id = request.POST.get('regis_id')
        diagnosis_results = request.POST.get('diagnosis_results')
        if not diagnosis_results:
            return callback
        with transaction.atomic():
            RegistrationInfo.objects.filter(
                id = regis_id
            ).update(
                diagnosis_results = diagnosis_results or None  # 由于上述的判断，确诊结果应该不会是空字符了，不知是否还需要 or None
            )
            callback['status'] = 0
            callback['message'] = '确诊结果提交成功！'
            return callback

    def post_medicine(self, request):
        """
        提交药品信息、医嘱建议
        """
        regis_id = request.POST.get('regis_id')
        data = dict(request.POST)
        if 'medicine_info_id[]' not in data:
            return {'status': -1, 'message': '请至少选择一种药品！'}
        medicine_num = len(data['medicine_info_id[]'])
        result = Prescription.objects.filter(registration_info_id = regis_id)
        with transaction.atomic():
            if result:
                PrescriptionDetail.objects.filter(prescription_info_id = result[0].id).delete()
                result.delete()
            prescription = Prescription.objects.create(
                registration_info_id = regis_id,
                medical_advice = data['medical_advice'][0] or None, # 使用 or None 代替 null_string_to_none
                medicine_num = medicine_num,
                payment_status = 0
            )
            for i in range(medicine_num):
                PrescriptionDetail.objects.create(
                    detail_id = i + 1,
                    medicine_quantity = data['medicine_quantity[]'][i],
                    medicine_info_id = data['medicine_info_id[]'][i],
                    prescription_info_id = prescription.id
                )
            return {'status': 0, 'message': '药品及医嘱提交成功！'}

    # endregion



class NurseAPI(View):
    """
    护士工作站数据查询API
    """

    def get(self, request):
        print('====== START NurseAPI GET ======')
        for param in request.GET:
            print(f'【{param}】{request.GET.get(param)}')
        print('======  END NurseAPI GET ======')
        query_key_to_func = {
            # 医嘱处理信息查询
            "MEDICAL_ADVICE_QUERY": self.query_medical_advice_process,
            # 住院患者信息查询
            "INPATIENTS_QUERY": self.query_inpatients,
            # 患者入院登记基础信息查询
            "PATIENT_INFO_QUERY": self.query_patient_info,
            # 待收患者信息查询
            "WAITING_QUERY": self.query_waiting_patients,
            # 空床位查询
            "BED_QUERY": self.query_empty_beds
        }

        # 获取需要查询的信息类型
        query_information = request.GET.get('get_param')
        data = query_key_to_func.get(query_information)(request)
        return JsonResponse(data, safe=False)

    def query_medical_advice_process(self, request):
        regis_id = request.GET.get('regis_id')
        medical_advice_info = Prescription.objects.filter(
            registration_info_id=regis_id
        ).values_list('medical_advice')
        medicine_info = PrescriptionDetail.objects.filter(
            prescription_info__registration_info_id=regis_id
        ).values_list(
            'medicine_quantity', 'medicine_info__medicine_name')
        inspect_info = PatientTestItem.objects.filter(
            registration_info_id=regis_id,
            issue_time__date=timezone.localdate()
        ).values_list('test_item__inspect_name')

        medical_advice_info = [info[0] for info in medical_advice_info]
        medicine_info = list(medicine_info)
        inspect_info = [info[0] for info in inspect_info]
        print(medical_advice_info, medicine_info, inspect_info)
        data = {
            'medicine_info': medicine_info,
            'medical_advice_info': medical_advice_info,
            'inspect_info': inspect_info
            }
        return data

    def query_inpatients(self, request):
        dept_id = request.session.get('dept_id')
        regis_info = HospitalRegistration.objects.filter(
            reg_date__isnull=False,
            dept_id=dept_id
        ).values_list(
            'registration_info_id',
            'registration_info__patient__name',
            'care_level'
        )
        data = [dict(zip(
            ['regis_id', 'name', 'care_level'],
            regis
        )) for regis in regis_info]
        # 传入医生主键，这样可以有选择的返回病人信息
        return data

    def query_patient_info(self, request):
        regis_id = request.GET.get('regis_id')
        hospital_regis_info = HospitalRegistration.objects.get(registration_info_id=regis_id)
        gender_convert = ['男', '女']
        data = {
            'regis_id': hospital_regis_info.registration_info.id,
            'name': hospital_regis_info.registration_info.patient.name,
            'gender': gender_convert[hospital_regis_info.registration_info.patient.gender],
            'age': timezone.localdate().year - hospital_regis_info.registration_info.patient.birthday.year,
        }
        return data

    #  查询待收患者
    def query_waiting_patients(self, request):
        dept_id = request.session.get('dept_id')
        regis_info = HospitalRegistration.objects.filter(
            reg_date__isnull=True,
            dept_id=dept_id
        ).values_list(
            'registration_info_id',
            'registration_info__patient__name',
            'registration_info__patient__gender'
        )
        gender_convert = ['男', '女']
        data = [dict(zip(
            ['regis_id', 'name', 'gender'],
            (regis[0], regis[1], gender_convert[regis[2]])
        )) for regis in regis_info]
        print(data)
        return data

    def query_empty_beds(self, request):
        """
        空床位查询

        数据示例：{"AREA": "A","BED": [1, 3, 4, 5, 6]}
        """
        dept_id = request.session["dept_id"]
        inpatient_area_info = []
        nurse_dept = Department.objects.get_by_dept_id(dept_id)
        # 所有病区与床位
        area_beds = DeptAreaBed.objects.filter(
            dept = nurse_dept
        ).values_list("area", "bed_id")
        # 已用病区与床位
        # 筛选条件为：入院登记表中，属于本科室，同时未出院的患者所在的病区与床位
        used_beds = HospitalRegistration.objects.filter(
            dept = nurse_dept,
            discharge_status = 0
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
        print(inpatient_area_info)
        return inpatient_area_info

    def post(self, request):
        print("========= START NurseAPI POST =========")
        for param in request.POST:
            print(f'【{param}】{request.POST.get(param)}')
        print("=========  END NurseAPI POST ==========")
        post_key_to_func = {
            "hospital_registration": self.post_hospital_registration,
            'nursing_record': self.post_nursing_record
        }
        callback = post_key_to_func[request.POST.get('post_param')](request)
        return JsonResponse(callback, safe=False)

    # 提交护理记录
    def post_nursing_record(self, request):
        regis_id = request.POST.get("regis_id")
        today = timezone.localdate()
        nurse_id = request.session.get('username')
        systolic = request.POST.get("systolic")
        diastolic = request.POST.get("diastolic")
        temperature = request.POST.get("temperature")
        note = request.POST.get("note")
        with transaction.atomic():
            NursingRecord.objects.update_or_create(
                registration_info_id = regis_id,
                nursing_date = today,
                defaults = {
                    "registration_info_id": regis_id,
                    "medical_staff_id": nurse_id,
                    "systolic": systolic,
                    "diastolic": diastolic,
                    "temperature": temperature,
                    "note": note,
                }
            )
            # nursing_info = NursingRecord.objects.filter(
            #     registration_info_id = regis_id,
            #     nursing_date = timezone.localdate()
            # )
            # if nursing_info.exists():
            #     nursing_info.update(
            #         registration_info_id = regis_id,
            #         medical_staff_id = nurse_id,
            #         systolic = request.POST.get('systolic'),
            #         diastolic = request.POST.get('diastolic'),
            #         temperature = request.POST.get('temperature'),
            #         note = request.POST.get('note')
            #     )
            # else:
            #     NursingRecord.objects.create(
            #         registration_info_id = regis_id,
            #         medical_staff_id = nurse_id,
            #         systolic = request.POST.get('systolic'),
            #         diastolic = request.POST.get('diastolic'),
            #         temperature = request.POST.get('temperature'),
            #         note = request.POST.get('note')
            #     )
        return {'status': 0, 'message': '护理记录已更新'}

    # 提交入院登记
    def post_hospital_registration(self, request):
        regis_id = request.POST.get("regis_id")
        reg_date = request.POST.get("reg_date")
        reg_level = int(request.POST.get("care_level"))
        area_id = request.POST.get('area_bed')[0]
        bed_id = request.POST.get('area_bed')[1]
        kin_phone = request.POST.get('kin_phone')
        try:
            PhoneNumberValidator()(kin_phone)
        except Exception as e:
            return {'status': 1, 'message': e.message}
        with transaction.atomic():
            HospitalRegistration.objects.filter(registration_info_id = regis_id).update(
                reg_date = reg_date,
                care_level = reg_level,
                area_id = area_id,
                bed_id = bed_id,
                kin_phone = kin_phone
            )
            return {'status': 0, 'message': "入院登记已记录"}


# 住院医生工作台数据
class InpatientAPI(View):
    # region get函数
    def get(self, request):
        print('====== InpatientAPI GET ======')
        for get_param in request.GET:
            print(f'【{get_param}】{request.GET.get(get_param)}')
        print('====== InpatientAPI GET ======')
        # 获取需要查询的信息类型
        get_param = request.GET.get('get_param')
        query_key_to_func = {
            "inpatient": self.query_inpatient,
            'recently_discharged': self.query_recently_discharged,
            'medical_advice': self.query_medical_advice,
            'history_sheet': self.query_history_sheet,
            'patient_info': self.query_patient_info,
            'search_medicines': self.query_search_medicines,
            'medicine_details': self.query_medicine_details
        }

        data = query_key_to_func[get_param](request)
        return JsonResponse(data, safe=False)

    # 查询药品信息，设置了分页功能
    def query_search_medicines(self, request):
        # select2要求的数据格式：{total_count: 108, items: list(30), incomplete_results: boolean}
        # 获取需要查询的页数
        page = int(request.GET.get('page'))
        # 设置每页的数据量，
        pageSize = 10
        medicine_text = request.GET.get('medicine_text')
        # 查询所有符合条件的药品
        medicine_info = MedicineInfo.objects.filter(medicine_name__contains=medicine_text)
        # 设置分页
        ptr = Paginator(medicine_info, pageSize)
        # 获取分页对象
        medicine_page_info = ptr.page(page).object_list
        # 获取分页对象值
        medicines = medicine_page_info.values_list(
            'medicine_id', 'medicine_name'
        )
        data = {
            'items': [],
            'total_count': medicine_info.count(),
            'incomplete_results': ptr.num_pages == page
        }
        # 返回的数据中一定需要以id为键的值，用以select2区分数据
        for info in medicines:
            data['items'].append(dict(zip(
                ['id', 'medicine_name'],
                info
            )))
        return data

    # 查询药品价格
    def query_medicine_details(self, request):
        medicine_id = request.GET.get('medicine_id')
        medicine = MedicineInfo.objects.get(medicine_id=medicine_id)
        return {'retail_price': medicine.retail_price}

    # 查询病人基础信息
    def query_patient_info(self, request):
        regis_id = request.GET.get('regis_id')
        patient = RegistrationInfo.objects.get(id=regis_id).patient
        # data = {
        #     'regis_id': regis_id,
        #     'name': patient.name,
        #     'gender': patient.gender,
        #     'age': timezone.now().year - patient.birthday.year
        # }
        data = [regis_id, patient.name, patient.gender, timezone.now().year - patient.birthday.year]
        return data

    # 查询住院患者
    def query_inpatient(self, request):
        data = []
        inhospital_info = HospitalRegistration.objects.filter(
            area_id=request.GET.get('area_id'),
            dept_id=request.GET.get('dept_id'),
            discharge_status=0
        ).values_list('registration_info__patient__name', 'care_level', 'bed_id', 'registration_info_id')
        for info in inhospital_info:
            data.append(dict(zip(
                ['patient_name', 'care_level', 'bed_id', 'regis_id'],
                [info[0], info[1], info[2], info[3]]
            )))
        return data

    # 查询即将出院的患者
    def query_recently_discharged(self, request):
        area_id = request.GET.get('area_id')
        dept_id = request.GET.get('dept_id')
        discharged_info = HospitalRegistration.objects.filter(
            area_id=area_id, dept_id=dept_id, discharge_status=1
        ).values_list(
            'registration_info_id',
            'registration_info__patient__name',
            'bed_id',
            'care_level'
        )
        data = []
        for info in discharged_info:
            data.append(dict(zip(
                ['regis_id', 'patient_name', 'bed_id', 'care_level'],
                info
            )))
        return data

    # 病人详情
    def query_history_sheet(self, request):
        regis_id = request.GET.get('regis_id')
        patient_info = RegistrationInfo.objects.filter(id=regis_id).values_list(
            'chief_complaint', 'patient__allegic_history', 'illness_date', 'patient__past_illness', 'diagnosis_results'
        )
        patient_info_dict = dict(zip(
            ('chief_complaint', 'allegic_history', 'illness_date', 'past_illness', 'diagnosis_results'),
            patient_info[0]
        ))
        print(patient_info_dict)
        return patient_info_dict

    # 查询药品及医嘱
    def query_medical_advice(self, request):
        medical_advice = []
        regis_id = request.GET.get('regis_id')
        prescription_info = Prescription.objects.filter(
            registration_info_id=regis_id,
        ).values_list('id', 'medical_advice', 'prescription_date')
        for prescription in prescription_info:
            prescription_details_info = PrescriptionDetail.objects.filter(
                prescription_info_id=prescription[0]).values_list(
                'medicine_info__medicine_name', 'medicine_quantity'
            )
            print('prescription_details_infomations')
            print(prescription_details_info)
            medical_advice.append({
                'medical_advice': prescription[1],
                'medicine_info': list(prescription_details_info),
                'issue_time': prescription[2]
            })
        print(medical_advice)
        return medical_advice

    # endregion

    def post(self, request):
        post_key_to_func = {
            # 保存医生医嘱
            "medical_advice": self.save_medical_advice,
            "inspection": self.post_inspection,

        }
        # 输出提示信息
        print("==========START outpatientAPI POST==========")
        for post_param in request.POST:
            print(f'【{post_param}】{request.POST.get(post_param)}')
        for post_param in dict(request.POST):
            print(f"【{post_param}】{dict(request.POST)[post_param]}")
        print("==========END outpatientAPI POST==========")
        ''' 
        param对照表:
        medicine -> 处方开具选择的药品
        inspection -> 检验信息
        history_sheet -> 病历首页
        '''
        # 根据参数直接映射对应的函数，并执行
        data = post_key_to_func[request.POST.get('post_param')](request)
        return JsonResponse(data, safe=False)

    def save_medical_advice(self, request):
        with transaction.atomic():
            medicine_info = []
            for i in range(len(dict(request.POST)['medicine_id[]'])):
                medicine_info.append([
                    dict(request.POST)['medicine_id[]'][i],
                    dict(request.POST)['medicine_quantity[]'][i],
                ])
            prescription = Prescription.objects.create(
                registration_info_id=request.POST.get('regis_id'),
                medicine_num=len(medicine_info),
                medical_advice=request.POST.get('medical_advice') or None,
                payment_status=0,
            )
            for i in range(len(medicine_info)):
                PrescriptionDetail.objects.create(
                    detail_id=i,
                    medicine_quantity=medicine_info[i][1],
                    medicine_info_id=medicine_info[i][0],
                    prescription_info_id=prescription.id
                )
            return {'status': 0, 'message': '医嘱已添加'}

    def post_inspection(self, request):
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
            regis_id = request.POST.get('regis_id')
            data = dict(request.POST)
            RegistrationInfo.objects.filter(id=regis_id).update(diagnosis_status=1)
            test_id = len(PatientTestItem.objects.filter(registration_info_id=regis_id))
            status = -1
            message = '请至少选择一个检验项目！'
            for param in data:
                print('param:', param)
                if param not in ('post_param', 'regis_id'):
                    for test_item in data[param]:
                        status = 0
                        message = '检验项目已更新'
                        print('test_item: ', test_item)
                        test_id += 1
                        print(test_id)
                        PatientTestItem.objects.create(
                            test_id=test_id,
                            registration_info_id=regis_id,
                            test_item_id=test_item,
                            payment_status=0,
                            inspect_status=0
                        )
        print(status, message)
        return {'status': status, 'message': message}

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
    RE_REG_REDIRECT_URL_NAME = "patient"
    patient_next_url_name = "patient-details"

    def query_registration_info(self, request):
        """
        查询
        """
        # 数据格式示例：[{
        #     "doctor_id": "999",
        #     "doctor_name": "lisa",
        #     "AM": 3,
        #     "PM": 4,
        #     "price": 25,
        # },...]
        reg_date = request.GET.get('date')
        # 构造挂号时段
        reg_datetime = {
            "AM": dateparse.parse_datetime(reg_date + " 08:00:00").astimezone(timezone.utc),
            "PM": dateparse.parse_datetime(reg_date + " 13:00:00").astimezone(timezone.utc)
        }
        dept_id = int(request.GET.get('KS_id'))
        # 获取指定科室、指定时段的剩余挂号信息
        reginfo_detail = RemainingRegistration.objects.filter(
            medical_staff__dept__usergroup__ug_id=dept_id,
            register_date__in=reg_datetime.values()
        ).values_list(
            "medical_staff__user__username",
            "medical_staff__name",
            "medical_staff__title__titleregisternumber__registration_price",
            "register_date",
            "remain_quantity",
        )
        doctor_info = reginfo_detail.values_list(
            "medical_staff__user__username",
            "medical_staff__name",
            "medical_staff__title__titleregisternumber__registration_price",
        ).distinct()
        reginfo = []
        for regdetail in doctor_info:
            doc_reg = {
                "doctor_id": regdetail[0],
                "doctor_name": regdetail[1],
                "price": regdetail[2],
                "AM": reginfo_detail.filter(
                    medical_staff__user__username=regdetail[0],
                    register_date=reg_datetime["AM"]
                ).values_list("remain_quantity", flat=True)[0],
                "PM": reginfo_detail.filter(
                    medical_staff__user__username=regdetail[0],
                    register_date=reg_datetime["PM"]
                ).values_list("remain_quantity", flat=True)[0],
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
            # "query_source": request.session["patient_id"],
            "query_data": query_data,
            "token": token,
            "submit_url": reverse(PatientRegisterAPI.SUBMIT_URL_NAME)
        }
        return JsonResponse(data, safe = False)

    def post(self, request):
        # 获取请求中的信息
        reg_info = json.loads(request.body.decode())
        reg_info["reg_datetime"] = timezone.make_aware(
            dateparse.parse_datetime(reg_info["reg_datetime"])
        ).astimezone(timezone.utc)
        reg_info["is_emergency"] = Staff.objects.get_by_user(
            reg_info["doctor_id"]
        ).dept == Department.objects.get_by_dept_name("急诊科")
        # 获取病人与医生对象
        patient_id = request.session["patient_id"]
        patient = PatientUser.objects.get_by_patient_id(patient_id)
        doctor = Staff.objects.get_by_user(reg_info["doctor_id"])
        # 检查是否存在重复的挂号记录
        if RegistrationInfo.objects.filter(
            patient = patient,
            medical_staff = doctor,
            registration_date = reg_info["reg_datetime"],
        ).count() > 0:
            return JsonResponse(
                {
                    "status": False,
                    "msg": "您已重复挂号！",
                    "redirect_url": reverse(PatientRegisterAPI.RE_REG_REDIRECT_URL_NAME)
                },
                safe = False
            )
        with transaction.atomic():
            # 更新剩余挂号数
            remain_reg_record = RemainingRegistration.objects.get(
                medical_staff__user__username=reg_info["doctor_id"],
                register_date=reg_info["reg_datetime"]
            )
            remain_reg_record.remain_quantity = remain_reg_record.remain_quantity - 1
            remain_reg_record.save()
            # 写入挂号信息
            reg_id = patient.registration_set.count() + 1
            reg_record = RegistrationInfo.objects.create(
                patient=patient,
                reg_id=reg_id,
                medical_staff=doctor,
                registration_date=reg_info["reg_datetime"],
                reg_class=1 if reg_info["is_emergency"] else 0
            )
        return JsonResponse(
            {
                "status": True,
                "msg": "即将跳转至您的个人界面",
                "redirect_url": reverse(PatientRegisterAPI.patient_next_url_name)
            },
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
                "price": reginfo_detail.values_list(
                    "medical_staff__title__titleregisternumber__registration_price",
                    flat = True,
                )[0],
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


class PatientUserAPI(View):
    """
    病人基础信息API，用于医生获取病人基础数据
    """
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


@method_decorator(patient_login_required(login_url = "/login-patient/"), name = "post")
class PaymentAPI(View):
    """
    支付API

    （暂时只支持支付宝Alipay）
    """
    NOTIFY_URL_NAME = settings.ALIPAY_APP_NOTIFY_URL_NAME
    # 支付项目类型名称(str, name) -> 支付项目类型存储值(int)
    # e.g. 挂号 -> 0
    ITEM_TYPE_DICT = {item[1]:item[0] for item in PaymentRecord.ITEM_TYPE_ITEMS}
    # 支付项目类型存储值(int) -> 支付项目类型名称(str, name)
    # e.g. 0 -> 挂号
    ITEM_TYPE_DICT_REV = dict(PaymentRecord.ITEM_TYPE_ITEMS)
    # 支付项目类型代码(str, code) -> 支付项目类型名称(str, name)
    # e.g. registration -> 挂号
    ITEM_TYPE_STR_MAP = dict(zip(
        ["registration", "test", "operation", "prescription", "discharge"],
        ITEM_TYPE_DICT.keys()
    ))

    def post(self, request):
        pay_type_to_func = {
            # 支付宝支付
            "alipay": self.pay_alipay,
            # 微信支付
            # "wechatpay": self.pay_wechatpay,
        }
        # 获取支付类型（支付平台代号）
        pay_type = request.POST.get("type")
        # 获取协议与域名，用于构造 return/notify url
        schema = request.scheme
        host = request.get_host()
        url_pattern = "{}://{}/{}/".format(schema, host, '{}')
        # 构造支付信息字典，并加入支付成功的回调URL
        pay_data = {
            "item": request.POST.get("item"),
            "price": request.POST.get("price"),
            "pk": request.POST.get("pk"),
            "subject": request.POST.get("subject"),
            "return_url": url_pattern.format(request.POST.get("return_url").strip('/')),
            "notify_url": '',
            "out_trade_no": '',
        }
        pay_data["notify_url"] = url_pattern.format(reverse(PaymentAPI.NOTIFY_URL_NAME).strip('/'))
        # 这里使用 uuid1 算法保证唯一性，但可能泄露主机 MAC，需要更换
        pay_data["out_trade_no"] = pay_data["item"] + uuid.uuid1().hex
        # 记录订单信息
        self.create_payment_record(pay_data)
        # 获取支付信息，包括：
        # @res: 标志
        # @msg: 提示信息
        # @url: 支付URL
        pay_info = pay_type_to_func[pay_type](pay_data)
        return JsonResponse(pay_info, safe = False)

    def create_payment_record(self, pay_data):
        # return
        item_type = PaymentAPI.ITEM_TYPE_DICT[
            PaymentAPI.ITEM_TYPE_STR_MAP[pay_data["item"]]
        ]
        with transaction.atomic():
            PaymentRecord.objects.create(
                trade_no = pay_data["out_trade_no"],
                total_amount = pay_data["price"],
                item_type = item_type,
                item_name = pay_data["subject"],
                item_pk = pay_data["pk"]
            )

    def pay_alipay(self, pay_data):
        pay_info = AlipayClient().get_page_pay_url(pay_data)
        return pay_info


class PaymentCheck(View):
    """
    检查支付是否成功。成功则跳转回主页，失败则显示失败页面，然后跳转回目标页面
    """
    PAYMENT_ERROR_PAGE = "payment-error.html"
    PAYMENT_SUCCESS_NAME = "index"

    def get(self, request):
        success = AlipayClient().verify(request)

        # ##### 测试各表 payment 字段的更新 #####
        # out_trade_no = request.GET.get("out_trade_no")
        # # 2. 根据订单号将数据库中的数据进行更新（修改订单状态）
        # pr = PaymentRecord.objects.get(trade_no = out_trade_no)
        # # 2.1 根据订单记录中的 item_type 找到要更新的表，更新对应的缴费字段
        # status = self.update_payment_field(pr.item_type, pr.item_pk)
        # # 2.2 更新缴费记录中的缴费字段
        # self.update_payment_status(out_trade_no)
        # ##### END #####

        if success:
            return redirect(reverse(PaymentCheck.PAYMENT_SUCCESS_NAME))
        return render(request, PaymentCheck.PAYMENT_ERROR_PAGE)

    def update_payment_field(self, item_type, item_pk):
        value_to_func = {
            0: self.update_registration_info, # 挂号
            1: self.update_patient_test_item, # 患者检验项目
            2: self.update_operation_info, # 手术
            3: self.update_prescription, # 处方
            4: self.update_hospital_registration, # 住院记录
        }
        item_pk_list = item_pk.split('-')
        status = value_to_func.get(item_type)(item_pk_list)
        return status

    def update_payment_status(self, pk):
        """
        更新缴费记录表中对应订单的缴费状态字段
        """
        with transaction.atomic():
            pr = PaymentRecord.objects.get(trade_no = pk)
            pr.is_pay = 1
            pr.save()

    def update_registration_info(self, pk_list):
        """
        根据主键列表找到对应挂号信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id = pk_list[0:2]
        patient = PatientUser.objects.get_by_patient_id(patient_id)
        with transaction.atomic():
            ri = RegistrationInfo.objects.get(patient = patient, reg_id = reg_id)
            ri.payment_status = True
            ri.save()
        return True

    def update_patient_test_item(self, pk_list):
        """
        根据主键列表找到对应患者检验项目中的记录，更新缴费状态字段。
        """
        patient_id, reg_id, test_id = pk_list[0:3]
        with transaction.atomic():
            pti = PatientTestItem.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id,
                test_id = test_id
            )
            pti.payment_status = True
            pti.save()
        return True

    def update_operation_info(self, pk_list):
        """
        根据主键列表找到对应手术信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id, operation_id = pk_list[0:3]
        with transaction.atomic():
            oi = OperationInfo.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id,
                operation_id = operation_id
            )
            oi.payment_status = True
            oi.save()
        return True

    def update_prescription(self, pk_list):
        """
        根据主键列表找到对应入院信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id, prescription_date = pk_list[0:3]
        prescription_date = prescription_date.split('_')
        pres_date = '-'.join(prescription_date[0:3]) + " " + ':'.join(prescription_date[3:6])
        pres_date = dateparse.parse_datetime(pres_date).astimezone(timezone.utc)
        with transaction.atomic():
            pp = Prescription.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id,
                prescription_date = pres_date
            )
            pp.payment_status = True
            pp.save()
        return True

    def update_hospital_registration(self, pk_list):
        """
        根据主键列表找到对应挂号信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id = pk_list[0:2]
        with transaction.atomic():
            hr = HospitalRegistration.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id
            )
            hr.payment_status = True
            hr.save()
        return True


@method_decorator(csrf_exempt, name = "dispatch")
class PaymentNotifyAPI(View):
    """
    支付回调视图函数，用于在支付成功后，接收支付宝发送的 POST 请求，然后修改订单状态。

    公网下才能够执行
    ---------------
    """
    # @csrf_exempt
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        from urllib.parse import parse_qs

        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        client = AlipayClient().CLIENT
        sign = post_dict.pop('sign', None)
        status = client.verify(post_dict, sign)
        if status:
            # 1. 获取订单号
            out_trade_no = post_data.get("out_trade_no")[0]
            # 2. 根据订单号将数据库中的数据进行更新（修改订单状态）
            pr = PaymentRecord.objects.get(trade_no = out_trade_no)
            # 2.1 根据订单记录中的 item_type 找到要更新的表，更新对应的缴费字段
            status = self.update_payment_field(pr.item_type, pr.item_pk)
            # 2.2 更新缴费记录中的缴费字段
            self.update_payment_status(out_trade_no)
            return HttpResponse('success')
        # 3. 最终需要返回 "success" 字符给支付宝，否则支付宝将一直请求该地址并发送回调结果（具体看官方文档）
        return HttpResponse('success')

    def update_payment_field(self, item_type, item_pk):
        value_to_func = {
            0: self.update_registration_info, # 挂号
            1: self.update_patient_test_item, # 患者检验项目
            2: self.update_operation_info, # 手术
            3: self.update_prescription, # 处方
            4: self.update_hospital_registration, # 住院记录
        }
        item_pk_list = item_pk.split('-')
        status = value_to_func.get(item_type)(item_pk_list)
        return status

    def update_payment_status(self, pk):
        """
        更新缴费记录表中对应订单的缴费状态字段
        """
        with transaction.atomic():
            pr = PaymentRecord.objects.get(trade_no = pk)
            pr.is_pay = 1
            pr.save()

    def update_registration_info(self, pk_list):
        """
        根据主键列表找到对应挂号信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id = pk_list[0:2]
        patient = PatientUser.objects.get_by_patient_id(patient_id)
        with transaction.atomic():
            ri = RegistrationInfo.objects.get(patient = patient, reg_id = reg_id)
            ri.payment_status = True
            ri.save()
        return True

    def update_patient_test_item(self, pk_list):
        """
        根据主键列表找到对应患者检验项目中的记录，更新缴费状态字段。
        """
        patient_id, reg_id, test_id = pk_list[0:3]
        with transaction.atomic():
            pti = PatientTestItem.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id,
                test_id = test_id
            )
            pti.payment_status = True
            pti.save()
        return True

    def update_operation_info(self, pk_list):
        """
        根据主键列表找到对应手术信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id, operation_id = pk_list[0:3]
        with transaction.atomic():
            oi = OperationInfo.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id,
                operation_id = operation_id
            )
            oi.payment_status = True
            oi.save()
        return True

    def update_prescription(self, pk_list):
        """
        根据主键列表找到对应入院信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id, prescription_date = pk_list[0:3]
        prescription_date = prescription_date.split('_')
        pres_date = '-'.join(prescription_date[0:3]) + " " + ':'.join(prescription_date[3:6])
        pres_date = dateparse.parse_datetime(pres_date).astimezone(timezone.utc)
        with transaction.atomic():
            pp = Prescription.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id,
                prescription_date = pres_date
            )
            pp.payment_status = True
            pp.save()
        return True

    def update_hospital_registration(self, pk_list):
        """
        根据主键列表找到对应挂号信息中的记录，更新缴费状态字段。
        """
        patient_id, reg_id = pk_list[0:2]
        with transaction.atomic():
            hr = HospitalRegistration.objects.get(
                registration_info__patient__patient_id = patient_id,
                registration_info__reg_id = reg_id
            )
            hr.payment_status = True
            hr.save()
        return True


class PaymentError(View):
    """
    缴费失败页面
    """
    payment_error_template = "payment-error.html"

    def get(self, request):
        return render(request, PaymentError.payment_error_template)
