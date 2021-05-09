from django.db import models
from django.utils.translation import gettext_lazy as _


class TestItem(models.Model):
    """
    检验项目
    """
    TEST_TYPE_ITEMS = (
        (1, '临床'), 
        (2, '生物化学'),
        (3, '微生物'),
        (4, '寄生虫'),
        (5, '免疫'),
    )
    iid = models.CharField(max_length = 6, primary_key=True)
    itype = models.CharField(max_length = 10, choices = TEST_TYPE_ITEMS)
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
