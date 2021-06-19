-- 患者 URL 访问权限
insert into patient_patienturlpermission 
(url_perm_id) values ("logout"), ("patient-details"), ("PatientFastRegisterAPI"), ("PatientTreatmentDetailAPI"),("PaymentAPI"),("payment-check");
-- role
insert into rbac_role
(id, name, description, create_time) values 
    (1,"职工","职工角色，所有医院职工共有的角色。URL访问权限为：workhub, news 和 logout。","2021-06-14 02:05:42"),
    (2,"门诊医生","门诊医生角色，URL访问权限为：OutpatientAPI 和 outpatient-workspace。","2021-06-14 02:05:43"),
    (3,"住院医生","住院部工作的医生角色，URL访问权限为：InpatientAPI 和 inpatient-workspace。","2021-06-14 02:05:44"),
    (4,"住院护士","住院部工作的护士角色，URL访问权限为：NurseAPI 和 nurse-workspace。","2021-06-14 02:05:45"),
    (5,"医学检验师","检验科医学检验师角色，URL访问权限为：InspectionAPI 和 inspection-workspace。","2021-06-14 02:05:46"),
    -- 无实际应用
    (6,"支付包支付接口开发","开发支付宝支付功能，URL访问权限为：PaymentAPI, PaymentNotifyAPI, payment-check, payment-error 和 patient-details。","2021-06-14 02:05:47"),
    (7,"内部数据API测试","测试全部内部数据API，URL访问权限为：*API。","2021-06-14 02:05:48"),
    (8,"患者快速挂号API压力测试","对患者快速挂号API进行压力测试，URL访问权限为：PatientFastRegisterAPI","2021-06-14 02:05:49");


-- role url perms
insert into rbac_role_url_permissions
(id, role_id, urlpermission_id) values 
    (1,1,"workhub"),(2,1,"logout"),(3,1,"news"),
    (4,2,"outpatient-workspace"),(5,2,"OutpatientAPI"),
    (6,3,"inpatient-workspace"),(7,3,"InpatientAPI"),
    (8,4,"nurse-workspace"),(9,4,"NurseAPI"),
    (10,5,"inspection-workspace"),(11,5,"InspectionAPI"),
    -- 无实际应用
    (12,6,"PaymentAPI"),(13,6,"payment-notify"),(14,6,"payment-check"),(15,6,"payment-error"),(16,6,"patient-details"),
    (17,7,"PatientRegisterAPI"),(18,7,"PatientFastRegisterAPI"),(19,7,"PatientTreatmentDetailAPI"),(20,7,"OutpatientAPI"),(21,7,"InspectionAPI"),(22,7,"NurseAPI"),(23,7,"InpatientAPI"),
    (24,8,"PatientFastRegisterAPI");

-- usergroup roles
insert into rbac_usergroup_roles
(id, usergroup_id, role_id) values 
    (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),
    (12,12,1),(13,13,1);

--
