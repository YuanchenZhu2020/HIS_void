# -*- coding: utf-8 -*-
"""
Created on Sat May 15 18:35:15 2021

@author: 14306
"""

#  患者信息插入代码
from patient.models import PatientUser
import xlrd

data = xlrd.open_workbook(r'./db_data_insert/患者信息.xls')
sheet = data.sheet_by_index(0)
patient_lis = []

for i in range(1,sheet.nrows):
     patient_lis.append(PatientUser(id_type=sheet.cell_value(i,1), id_number=sheet.cell_value(i,2), 
                                    name=sheet.cell_value(i,3), gender=sheet.cell_value(i,4),
                                    birthday=sheet.cell_value(i,5), phone=sheet.cell_value(i,6), 
                                    past_illness=sheet.cell_value(i,7), allegic_history=sheet.cell_value(i,8)))

PatientUser.objects.bulk_create(patient_lis)

for item in sheet.col_values(2,1):
    pu = PatientUser.objects.get(id_number = item)
    pu.set_password('123456')
    pu.save()



#  职工信息插入代码
from rbac.models import UserInfo
import xlrd

data = xlrd.open_workbook(r'./db_data_insert/职工信息.xlsx')
sheet = data.sheet_by_index(0)
sid = sheet.col_values(0,1)
staff_lis = []

for item in sid:
   ui =  UserInfo.objects.create(username = item)
   ui.set_password('123456')
   

