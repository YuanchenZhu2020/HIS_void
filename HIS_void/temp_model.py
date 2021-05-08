from __future__ import unicode_literals
from django.db import models

# Create your models here.
class equipment_information(models.Model):    #设备信息
    eid = models.AutoField(primary_key=True)
    emodel = models.CharField(max_length=20)
    estart = models.DateField()
    elifetime = models.PositiveIntegerField()
    equantity = models.PositiveIntegerField(default=1)
    
class equipment_purchase(models.Model):    #设备采购记录
    eid = models.OneToOneField(equipment_information, on_delete=models.CASCADE, primary_key=True, related_name='equ_eid') #这个不应该是一对一关系嘛？
    epdate = models.DateField()    #感觉没必要是主码就没设置
    epquantity = models.PositiveIntegerField(default=1)


class title_register_map(models.Model):    #职称-挂号数对应表（我觉得这里的联系有点儿问题）
    TITLE_CHOICES = (
        (1, '住院医师'),
        (2, '主治医师'),
        (3, '副主任医师'),
        (4, '主任医师'),
    )
    titleid = models.IntegerField(primary_key=True, choices=TITLE_CHOICES)
    register_limit = models.IntegerField() #感觉没有必要是主码就没写

class medical_staff(models.Model):    #医护人员信息
    SEX_CHOICE = (
        (0, '男'),
        (1, '女'),
    )
    JOB_CHOICES = (    #虽然写了两个但是按道理只有一个医生就够了？加了一个设备号
        (1, '门诊医生'),
        (2, '住院医生'),
        (3, '护士'),
        (4, '药房医生'),
        (5, '检验医生'),
        (6, '财务'),
        (7, '检验设备')
    )
    msid = models.CharField(primary_key=True, max_length=6)
    deptid = models.ForeignKey(departments, on_delete=models.CASCADE, related_name = 'meds_deptid')
    msname = models.CharField(max_length=10)  #应该不是bit叭……
    mssex = models.IntegerField(choices=SEX_CHOICE)   #bit我改了
    msidnumber = models.CharField(max_length=18)
    titleid = models.ForeignKey(title_register_map, on_delete=models.CASCADE, related_name='meds_titleid')   #多设置了个外键职称对应的挂号限额？
    job_type = models.IntegerField(choices=JOB_CHOICES)
    mpassword = models.CharField(max_length=20, blank=True)

class remaining_quantity(models.Model):    #医生剩余挂号数
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name = 'rem_msid')
    register_date = models.DateField()
    remain_quantity = models.PositiveIntegerField(blank=True)
    class Meta:
        db_table = 'remaining_quantity'
        unique_together = ['msid', 'register_date']

class duty_schedule(models.Model):    #医生排班表
    WEEKDAY_CHOICES = (
        (1, '星期一'),
        (2, '星期二'),
        (3, '星期三'),
        (4, '星期四'),
        (5, '星期五'),
        (6, '星期六'),
        (7, '星期日'),
    )
    DUTY_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name = 'dut_msid')
    weekday = models.PositiveIntegerField(choices=WEEKDAY_CHOICES)
    duty_region = models.CharField(blank=True, choices=DUTY_CHOICES, max_length=1)
    class Meta:
        db_table = 'duty_schedule'
        unique_together = ['msid', 'weekday']

class nursing_records(models.Model):    #护理记录
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name = 'nur_msid')
    pid = models.ForeignKey(patient_information, on_delete=models.CASCADE, related_name = 'nur_pid')
    nursing_date = models.DateField()
    systolic = models.PositiveIntegerField(blank=True)
    diastolic = models.PositiveIntegerField(blank=True)
    temperature = models.FloatField(blank=True)
    note = models.TextField(max_length=100, blank = True)
    class Meta:
        db_table = 'nursing_records'
        unique_together = ['msid', 'pid', 'nursing_date']

class patient_register(models.Model):    #挂号信息
    RCLASS_CHOICE = (
        ('门诊', '门诊'),
        ('急诊', '急诊'),
    )
    pid = models.ForeignKey(patient_information, on_delete=models.CASCADE, related_name = 'pat_pid')
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name = 'pat_msid')
    rid = models.PositiveIntegerField()
    reservedate = models.DateField()
    rdate = models.DateTimeField()   #点击“挂号”的时间
    rclass = models.CharField(max_length=4, choices=RCLASS_CHOICE)
    rdepartment = models.CharField(max_length=20)    #原科室名称，感觉删了也行……
    pstartdate = models.DateField(blank=True)
    pstate = models.TextField(max_length=512, blank=True)
    pconfirm = models.TextField(max_length=512, blank=True)
    class Meta:
        db_table = 'patient_register'
        unique_together = ['pid', 'rid']

class register_information(models.Model):    #入院登记信息文件
    REGION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    CARE_CHOICES = (
        (1, '一级护理'),     #一级护理用粉红色标记，表示重点护理，但不派专人守护。对绝大多数重危病人来说，这就算是高等级的护理。
        (2, '二级护理'),     #二级护理用蓝色标记，表示病情无危险性，适于病情稳定的重症恢复期病人，或年老体弱、生活不能完全自理、不宜多活动的病人。
        (3, '三级护理'),     #三级护理是普通护理，不作标记。对这个护理级别的轻病人，护士每3～4小时巡视1次。
        (4, '四级护理'),     #特别护理(特护)用大红色标记，凡病情危重或重大手术后的病人，随时可能发生意外，需要严密观察和加强照顾。特护的都是重危病人，但重危病人不一定都要特护。
    )
    pid = models.OneToOneField(patient_register, on_delete=models.CASCADE, related_name = 'reg_pid')    #外码从病人信息拿也可以吧
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name='reg_msid')  #我感觉没有必要存在了？而且就是要有的话也得是外键8，不然重复了
    rid = models.OneToOneField(patient_register, on_delete=models.CASCADE, related_name = 'reg_rid')
    region = models.CharField(max_length=1, choices=REGION_CHOICES)
    bed = models.PositiveIntegerField()
    rdate = models.DateField()
    care_level = models.PositiveIntegerField(choices=CARE_CHOICES)
    rduration = models.PositiveIntegerField(default=1)
    kinphone = models.CharField(max_length=11)
    discharge = models.BooleanField(default=False)    #修改了bit
    class Meta:
        db_table = 'register_information'
        unique_together = ['pid', 'rid']

class test_item_dic(models.Model):    #检验项目字典
    TYPE_CHOICES = (
        ('临床', '临床'), 
        ('生物化学', '生物化学'),
        ('微生物', '微生物'),
        ('寄生虫', '寄生虫'),
        ('免疫', '免疫'),
    )
    iid = models.CharField(max_length = 6, primary_key=True)
    itype = models.CharField(max_length = 10, choices = TYPE_CHOICES)
    iname = models.CharField(max_length = 30)
    iprice = models.FloatField()

class test_items(models.Model):    #病人检验项目
    pid = models.ForeignKey(patient_register, on_delete=models.CASCADE, related_name='tes_pid')
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name='tes_msid')   #同理？
    rid = models.ForeignKey(patient_register, on_delete=models.CASCADE, related_name = 'tes_rid')
    tid = models.PositiveIntegerField()
    iid = models.ForeignKey(test_item_dic, on_delete=models.CASCADE, related_name = 'tes_iid')
    issuetime = models.DateTimeField()
    test_results = models.TextField(max_length=400, blank=True)
    t_paystate = models.BooleanField(default=False)
    class Meta:
        db_table = 'test_items'
        unique_together = ['pid', 'rid', 'tid']

class operation_information(models.Model):    #手术信息文件
    LEVEL_CHOICES = (
        (1, '一级手术'),    #手术过程简单、技术难度较低、风险度较小的各种手术。
        (2, '二级手术'),    #手术过程不复杂、技术难度一般、风险度中等的各种手术。
        (3, '三级手术'),    #手术过程较复杂、技术难度较大、风险度较大的各种手术。
        (4, '四级手术'),    #手术过程复杂、技术难度大、风险度大的各种手术。
    )
    pid = models.ForeignKey(patient_register, on_delete=models.CASCADE, related_name='ope_pid')
    msid = models.ForeignKey(patient_register, on_delete=models.CASCADE, related_name='ope_msid')    #同理？
    rid = models.ForeignKey(patient_register, on_delete=models.CASCADE, related_name = 'ope_rid')
    oid = models.PositiveIntegerField()
    olevel = models.PositiveIntegerField(choices=LEVEL_CHOICES)
    odate = models.DateField()
    oname = models.CharField(max_length=40)
    oresult = models.CharField(max_length=20, blank=True)
    oduration = models.TimeField(blank=True)
    orecover = models.CharField(blank=True, max_length=10)
    o_paystate = models.BooleanField(default=False)
    class Meta:
        db_table = 'operation_information'
        unique_together = ['pid', 'rid', 'oid']

class prescription(models.Model):    #患者处方文件
    predate = models.DateTimeField()
    pid = models.OneToOneField(patient_register, on_delete=models.CASCADE, related_name = 'pre_pid')
    rid = models.OneToOneField(patient_register, on_delete=models.CASCADE, related_name = 'pre_rid')
    quantity = models.PositiveIntegerField(blank=True)
    order = models.TextField(max_length=400)
    p_paystate = models.BooleanField(default=False)
    class Meta:
        db_table = 'prescription'
        unique_together = ['predate', 'pid', 'rid']

class medicine_information(models.Model):    #药品信息
    SPECIAL_CHOICES = (
        (1, '麻醉药品'),
        (2, '精神药品'),
        (3, '毒性药品'),
        (4, '放射性药品'),
        (0, '普通药品'),
    )
    batch_num = models.PositiveIntegerField()
    mid = models.CharField(max_length=6)
    mname = models.CharField(max_length=20)
    specification = models.CharField(max_length=30)
    cost = models.FloatField()
    price = models.FloatField()
    stock_num = models.PositiveIntegerField()
    overdue_date = models.DateField()
    special = models.IntegerField(default=0, choices=SPECIAL_CHOICES)
    OTC = models.BooleanField(default=False)
    class Meta:
        db_table = 'medicine_information'
        unique_together = ['batch_num', 'mid']

class order_detail(models.Model):    #患者处方细节
    predate = models.ForeignKey(prescription, on_delete = models.CASCADE, related_name='ord_predate')
    pid = models.ForeignKey(prescription, on_delete=models.CASCADE, related_name = 'ord_pid')
    rid = models.ForeignKey(prescription, on_delete=models.CASCADE, related_name='ord_rid')
    batch_num = models.ForeignKey(medicine_information, on_delete=models.CASCADE, related_name = 'ord_batch_num')
    mid = models.ForeignKey(medicine_information, on_delete=models.CASCADE, related_name='ord_mid')
    did = models.PositiveIntegerField()
    oquantity = models.PositiveIntegerField()
    class Meta:
        db_table = 'order_detail'
        unique_together = ['predate', 'pid', 'rid', 'did']

class medicine_purchase(models.Model):    #药品采购记录
    batch_num = models.ForeignKey(medicine_information, on_delete=models.CASCADE, related_name = 'med_batch_num')
    mid = models.ForeignKey(medicine_information, on_delete=models.CASCADE, related_name = 'med_mid')
    mpdate = models.DateField()
    mpquantity = models.PositiveIntegerField()
    class Meta:
        db_table = 'medicine_purchase'
        unique_together = ['batch_num', 'mid']

class narcotic_information(models.Model):    #麻醉信息反馈
    msid = models.ForeignKey(medical_staff, on_delete=models.CASCADE, related_name = 'nar_msid')
    batch_num = models.ForeignKey(medicine_information, on_delete=models.CASCADE, related_name='nar_batch_num')
    mid = models.ForeignKey(medicine_information, on_delete=models.CASCADE, related_name = 'nar_mid')
    pid = models.OneToOneField(operation_information, on_delete=models.CASCADE, related_name = 'nar_pid')
    rid = models.OneToOneField(operation_information, on_delete=models.CASCADE, related_name = 'nar_rid')
    oid = models.OneToOneField(operation_information, on_delete=models.CASCADE, related_name = 'nar_oid')
    class Meta:
        db_table = 'narcotic_information'
        unique_together = ['pid', 'rid', 'oid']
