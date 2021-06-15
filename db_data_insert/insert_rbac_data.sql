-- 患者 URL 访问权限
insert into patient_patienturlpermission 
(url_perm_id) values ("logout"), ("patient-details"), ("PatientFastRegisterAPI"), ("PatientTreatmentDetailAPI");
-- role
insert into rbac_role
(id, name, description, create_time) values 
    (1,"职工","职工角色，所有医院职工共有的角色。URL访问权限为：workhub 和 logout。", "2021-06-14 02:05:42"),
    (1,"门诊医生","门诊医生角色，URL访问权限为：OutpatientAPI 和 outpatient-workspace。", "2021-06-14 02:05:43"),
    (1,"职工","门诊医生角色，URL访问权限为：OutpatientAPI 和 outpatient-workspace。", "2021-06-14 02:05:43"),


-- role url perms
insert into rbac_role_url_permissions
(id, role_id, urlpermission_id) values 
    (1,1,"workhub"),(2,1,"logout"),
    (3,2,"outpatient-workspace"),(4,2,"OutpatientAPI"),

-- usergroup roles
insert into rbac_usergroup_roles
(id, usergroup_id, role_id) values 
    (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),
    (12,12,1),(13,13,1);
