-- 挂号信息
-- 预约时间,记录编号,挂号编号,挂号时间,就诊类别,患病时间,患者主诉,确诊,医生工号,就诊号
-- ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}),([0-9]*),([0-9]*),([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}),([01]),([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}),(.*),([0-9]{6}),([0-9]*)
-- ("$1",$2,$3,"$4",$5,"$6",$7,"$8",$9),
insert into outpatient_registrationinfo values 
    ("2021-05-15 05:46:02",1,1,"2021-05-16 13:00:00",0,"2021-05-12 14:44:42","疼痛症状:肩及上肢痛,疼痛指征:局部痛; 伴随症状:呼吸困难、喷嚏","副肿瘤综合征,雷诺病","000023",1),
    ("2021-05-17 06:12:24",2,1,"2021-05-21 08:00:00",0,"2021-05-11 06:01:30","血压特征:低血压,血压特征持续时间:当天; 疼痛症状:肩及上肢痛,疼痛指征:急性痛; 伴随症状:昏迷、呕吐、咳嗽","脑梗塞,胰腺肿瘤","000030",2),
    ("2021-05-14 12:52:30",3,1,"2021-05-18 13:00:00",1,"2021-04-28 13:19:45","伴随症状:四肢乏力、易怒、关节肿痛","巩膜炎","000033",3),
    ("2021-05-18 04:55:43",4,1,"2021-05-19 13:00:00",0,"2021-05-13 08:22:01","体温特征:不规则发热,体温特征持续时间:一个月以上; 血压特征:高血压,血压特征持续时间:三天内; 疼痛症状:腹痛,疼痛指征:反复痛; 伴随症状:血尿","湿毒疮,外耳道炎,荨麻疹","000083",4),
    ("2021-05-13 22:34:22",5,1,"2021-05-17 13:00:00",0,"2021-05-02 06:14:12","体温特征:高热惊厥,体温特征持续时间:一个月以上; 疼痛症状:盆部痛,疼痛指征:急性痛; 伴随症状:易怒","远视,职业性皮肤癌","000099",5),
    ("2021-05-17 16:57:14",6,1,"2021-05-20 13:00:00",0,"2021-04-28 11:10:42","伴随症状:水肿","创伤性气胸,脾破裂,风湿性心脏病","000023",6),
    ("2021-05-19 01:10:27",7,1,"2021-05-22 13:00:00",0,"2021-05-16 12:51:04","体温特征:超高热,体温特征持续时间:一个月; 伴随症状:淋巴结肿大、伴有水疱","胆囊结石,胰腺炎,胰腺肿瘤","000030",7),
    ("2021-05-15 02:43:51",8,1,"2021-05-16 13:00:00",0,"2021-05-10 03:38:21","血压特征:高血压,血压特征持续时间:一周; 疼痛症状:腹痛,疼痛指征:放射痛; 伴随症状:伴有水疱、溃疡、黄疸","骨关节炎","000033",8),
    ("2021-05-16 15:44:30",9,1,"2021-05-19 08:00:00",0,"2021-05-10 02:53:39","体温特征:高热无汗,体温特征持续时间:一个月; 疼痛症状:颈部痛,疼痛指征:放射痛; 伴随症状:关节肿痛、溃疡","脑膜炎,红眼病","000083",9),
    ("2021-05-18 15:05:27",10,1,"2021-05-20 08:00:00",0,"2021-05-17 23:26:31","血压特征:高血压,血压特征持续时间:一周; 伴随症状:关节僵硬","慢性咽炎,干眼","000099",10),
    ("2021-05-17 06:20:00",11,1,"2021-05-20 08:00:00",0,"2021-05-14 19:45:10","伴随症状:呕吐、食欲减退","瘢痕挛缩,脑膜炎,过敏性鼻炎","000023",11),
    ("2021-05-20 03:12:15",12,1,"2021-05-21 08:00:00",1,"2021-05-18 13:50:04","血压特征:低血压,血压特征持续时间:一周; 疼痛症状:胸痛,疼痛指征:反复痛; 伴随症状:关节僵硬、喷嚏、昏迷","鼻窦炎,颅内真菌感染,肺结核","000030",12),
    ("2021-05-14 05:27:29",13,1,"2021-05-17 08:00:00",0,"2021-04-26 02:22:53","体温特征:连续低烧不退,体温特征持续时间:当天; 血压特征:高血压,血压特征持续时间:一个月; 伴随症状:呼吸困难、咳嗽","咽喉炎,胰腺肿瘤","000033",13),
    ("2021-05-14 15:40:01",14,1,"2021-05-18 13:00:00",1,"2021-05-03 19:15:47","体温特征:高热，大量出汗,体温特征持续时间:三天内; 血压特征:高血压,血压特征持续时间:三天内; 疼痛症状:头痛,疼痛指征:慢性痛; 伴随症状:咳嗽、恶心","接触性皮炎","000083",14),
    ("2021-05-15 20:15:01",15,1,"2021-05-19 13:00:00",0,"2021-05-04 23:51:22","体温特征:高热，大量出汗,体温特征持续时间:三天内; 血压特征:高血压,血压特征持续时间:一个月; 疼痛症状:头痛,疼痛指征:进展性痛; 伴随症状:咳嗽、呼吸困难、头晕","荨麻疹","000099",15),
    ("2021-05-17 20:41:29",16,1,"2021-05-18 13:00:00",1,"2021-05-03 18:05:26","体温特征:高热无汗,体温特征持续时间:一周; 血压特征:低血压,血压特征持续时间:当天; 伴随症状:咳嗽伴有哮鸣音","狼疮性肾炎,帕金森病","000023",16),
    ("2021-05-12 11:59:32",17,1,"2021-05-16 08:00:00",0,"2021-05-07 19:28:14","血压特征:高血压,血压特征持续时间:三天内; 伴随症状:食欲减退、咳嗽","鼻窦炎,小儿慢性粒细胞","000030",17),
    ("2021-05-19 00:32:48",18,1,"2021-05-20 08:00:00",1,"2021-05-04 23:03:14","血压特征:高血压,血压特征持续时间:一周; 伴随症状:活动障碍、昏迷","枯草热","000033",18),
    ("2021-05-16 07:48:47",19,1,"2021-05-21 13:00:00",0,"2021-05-04 10:47:18","体温特征:连续低烧，午后加重,体温特征持续时间:一个月; 伴随症状:溃疡、咳嗽伴有哮鸣音","鼻出血,湿毒疮,脑出血","000083",19),
    ("2021-05-18 11:26:01",20,1,"2021-05-19 08:00:00",0,"2021-05-15 09:26:48","体温特征:高热无汗,体温特征持续时间:当天; 血压特征:低血压,血压特征持续时间:三天内; 疼痛症状:盆部痛,疼痛指征:反复痛; 伴随症状:溃疡","青光眼,鼻咽癌","000099",20),
    ("2021-05-13 14:33:22",21,1,"2021-05-17 13:00:00",0,"2021-04-29 06:09:57","体温特征:间歇高热,体温特征持续时间:三天内; 血压特征:高血压,血压特征持续时间:当天; 伴随症状:易怒、昏迷、头晕","肝破裂,肺气肿,多发性颅内血肿","000103",21),
    ("2021-05-17 17:53:10",22,1,"2021-05-22 13:00:00",0,"2021-05-12 08:51:34","疼痛症状:颈部痛,疼痛指征:胀痛; 伴随症状:寒战、活动障碍","枯草热,分泌性中耳炎","000042",22),
    ("2021-05-11 07:10:53",23,1,"2021-05-16 08:00:00",0,"2021-05-02 17:18:51","血压特征:高血压,血压特征持续时间:一个月; 伴随症状:易困、咯血、呼吸困难","脊髓灰质炎,骨折,脂溢性皮炎","000051",23),
    ("2021-05-17 12:32:44",24,1,"2021-05-19 13:00:00",0,"2021-04-30 16:48:28","体温特征:间歇低热,体温特征持续时间:一周; 血压特征:低血压,血压特征持续时间:一个月以上; 疼痛症状:下肢痛,疼痛指征:局部痛; 伴随症状:淋巴结肿大、易困","细菌性角膜炎,支气管哮喘","000031",24),
    ("2021-05-14 02:36:09",25,1,"2021-05-19 13:00:00",0,"2021-04-25 16:06:54","体温特征:高热，大量出汗,体温特征持续时间:当天; 血压特征:高血压,血压特征持续时间:一个月以上; 伴随症状:出血症状","鼻出血,小儿支气管哮喘,化脓性阑尾炎","000049",25),
    ("2021-05-19 14:29:41",26,1,"2021-05-21 13:00:00",0,"2021-05-17 10:42:00","伴随症状:淋巴结肿大","肾破裂,胃炎,细菌性角膜炎","000053",26),
    ("2021-05-14 02:23:35",27,1,"2021-05-17 08:00:00",1,"2021-05-08 10:22:45","疼痛症状:胸痛,疼痛指征:胀痛; 伴随症状:食欲减退","更年期综合征,葡萄胎","000048",27),
    ("2021-05-12 08:03:19",28,1,"2021-05-17 13:00:00",0,"2021-04-28 14:44:10","体温特征:超高热,体温特征持续时间:当天; 疼痛症状:下肢痛,疼痛指征:放射痛; 伴随症状:单纯疱疹、活动障碍","脊髓灰质炎","000089",28),
    ("2021-05-16 17:30:10",29,1,"2021-05-17 13:00:00",0,"2021-05-15 09:45:09","体温特征:连续低烧，午后加重,体温特征持续时间:一周; 伴随症状:淋巴结肿大","骨折","000033",29),
    ("2021-05-13 08:54:06",30,1,"2021-05-17 13:00:00",0,"2021-05-05 16:05:58","体温特征:高热，大量出汗,体温特征持续时间:一个月; 疼痛症状:颌面部痛,疼痛指征:局部痛; 伴随症状:食欲减退、伴有水疱、呕吐","巩膜炎,颧骨骨折","000057",30),
    ("2021-05-19 17:21:37",31,1,"2021-05-22 08:00:00",1,"2021-05-06 20:24:25","体温特征:间歇高热,体温特征持续时间:一周; 血压特征:低血压,血压特征持续时间:一周; 疼痛症状:下肢痛,疼痛指征:慢性痛; 伴随症状:易困","法乐四联症","000041",31),
    ("2021-05-16 17:40:54",32,1,"2021-05-21 08:00:00",0,"2021-05-11 19:13:55","体温特征:连续低烧不退,体温特征持续时间:一个月以上; 疼痛症状:盆部痛,疼痛指征:慢性痛; 伴随症状:意识障碍","轻度烧伤,红眼病","000048",32),
    ("2021-05-17 08:04:06",33,1,"2021-05-19 13:00:00",1,"2021-04-27 03:36:29","体温特征:高热无汗,体温特征持续时间:一个月; 伴随症状:出血症状","职业性哮喘,枯草热,进行性肌营养不良","000055",33),
    ("2021-05-18 19:37:01",34,1,"2021-05-20 13:00:00",0,"2021-05-10 17:25:40","体温特征:间歇高热,体温特征持续时间:一周; 伴随症状:单纯疱疹、四肢乏力、咳嗽伴有哮鸣音","鼻中隔弯曲","000103",34),
    ("2021-05-12 17:11:52",35,1,"2021-05-16 13:00:00",1,"2021-05-05 21:56:28","伴随症状:咳嗽伴有哮鸣音、淋巴结肿大","红眼病,荨麻疹,胆囊结石","000105",35),
    ("2021-05-19 02:39:08",36,1,"2021-05-20 08:00:00",1,"2021-04-29 02:43:06","体温特征:超高热,体温特征持续时间:一个月; 血压特征:高血压,血压特征持续时间:三天内; 伴随症状:易怒、咳嗽伴有哮鸣音、关节肿痛","骨折,细菌性角膜炎","000043",36),
    ("2021-05-20 04:51:29",37,1,"2021-05-22 08:00:00",0,"2021-05-13 00:03:36","疼痛症状:腰及骶部痛,疼痛指征:放射痛; 伴随症状:出血症状、意识障碍、水肿","冻伤","000083",37),
    ("2021-05-13 17:32:19",38,1,"2021-05-18 08:00:00",1,"2021-05-04 21:53:46","伴随症状:咳嗽伴有哮鸣音","手足口病,远视","000099",38),
    ("2021-05-18 20:43:04",39,1,"2021-05-19 13:00:00",0,"2021-05-06 14:55:20","疼痛症状:颌面部痛,疼痛指征:局部痛; 伴随症状:出血症状、咯血、易困","高血压","000042",39),
    ("2021-05-20 09:23:09",40,1,"2021-05-22 08:00:00",0,"2021-05-12 08:53:22","体温特征:连续低烧，午后加重,体温特征持续时间:三天内; 血压特征:高血压,血压特征持续时间:一个月以上; 疼痛症状:腰及骶部痛,疼痛指征:慢性痛; 伴随症状:头晕、水肿、活动障碍","阿尔兹海默症,血液循环障碍","000037",40),
    ("2021-05-13 13:19:28",41,1,"2021-05-16 08:00:00",0,"2021-04-28 19:21:58","疼痛症状:颌面部痛,疼痛指征:按压痛; 伴随症状:淋巴结肿大、呼吸困难","毛囊炎,小儿支气管哮喘,虫咬性皮炎","000053",41),
    ("2021-05-18 10:13:30",42,1,"2021-05-22 08:00:00",1,"2021-04-30 05:11:16","体温特征:驰长高热,体温特征持续时间:三天内; 伴随症状:咳嗽伴有哮鸣音","狼疮性肾炎","000093",42),
    ("2021-05-20 18:13:13",43,1,"2021-05-22 08:00:00",0,"2021-05-12 10:31:25","疼痛症状:腰及骶部痛,疼痛指征:局部痛; 伴随症状:关节僵硬","小儿惊厥","000093",43),
    ("2021-05-16 08:09:15",44,1,"2021-05-20 13:00:00",0,"2021-05-05 19:44:04","伴随症状:结膜充血","帕金森病,尿路结石,弱视","000033",44),
    ("2021-05-16 01:26:29",45,1,"2021-05-17 08:00:00",0,"2021-04-30 14:49:19","疼痛症状:颌面部痛,疼痛指征:绞痛; 伴随症状:心慌","新生儿发热,骨关节炎,小儿慢性粒细胞","000030",45),
    ("2021-05-17 15:24:57",46,1,"2021-05-19 08:00:00",0,"2021-05-05 04:39:45","体温特征:高热惊厥,体温特征持续时间:一个月以上; 血压特征:低血压,血压特征持续时间:一个月; 疼痛症状:胸痛,疼痛指征:胀痛; 伴随症状:关节肿痛","鼻息肉","000083",46),
    ("2021-05-16 03:58:03",47,1,"2021-05-20 08:00:00",0,"2021-05-01 18:05:35","血压特征:低血压,血压特征持续时间:一个月; 疼痛症状:颌面部痛,疼痛指征:放射痛; 伴随症状:活动障碍","重症肌无力,颅脑破裂,子宫内膜异位症","000045",47),
    ("2021-05-16 11:16:34",48,1,"2021-05-17 08:00:00",0,"2021-05-06 09:02:59","伴随症状:易困、结膜充血","颅脑破裂,小儿支气管哮喘,鼻中隔弯曲","000095",48),
    ("2021-05-12 00:25:56",49,1,"2021-05-17 13:00:00",0,"2021-04-23 16:24:48","体温特征:间歇高热,体温特征持续时间:当天; 血压特征:高血压,血压特征持续时间:三天内; 伴随症状:关节僵硬","宫外孕,狼疮性肾炎,小儿流行性肺炎","000035",49),
    ("2021-05-12 08:46:42",50,1,"2021-05-16 08:00:00",0,"2021-05-08 08:58:40","体温特征:间歇低热,体温特征持续时间:一周; 血压特征:低血压,血压特征持续时间:一个月以上; 疼痛症状:腹痛,疼痛指征:按压痛; 伴随症状:出血症状、头晕","湿毒疮,干燥性角结膜炎,肺结核","000037",50),
    ("2021-05-17 12:39:31",51,1,"2021-05-18 13:00:00",0,"2021-04-30 12:33:21","体温特征:高热无汗,体温特征持续时间:三天内; 伴随症状:心慌、伴有水疱","外耳道炎","000047",51),
    ("2021-05-15 15:19:10",52,1,"2021-05-16 13:00:00",1,"2021-05-13 04:53:52","体温特征:高热惊厥,体温特征持续时间:三天内; 伴随症状:喷嚏、呕吐、咯血","心肌炎,粪类圆线虫病","000051",52),
    ("2021-05-20 04:59:53",53,1,"2021-05-22 13:00:00",1,"2021-05-14 02:47:56","体温特征:不规则发热,体温特征持续时间:一个月以上; 伴随症状:关节肿痛、食欲减退","粪类圆线虫病","000039",53),
    ("2021-05-17 07:24:23",54,1,"2021-05-22 13:00:00",0,"2021-05-12 00:03:27","伴随症状:昏迷、易怒","鼻出血","000109",54),
    ("2021-05-18 13:55:46",55,1,"2021-05-21 08:00:00",0,"2021-05-17 09:17:54","体温特征:高热无汗,体温特征持续时间:三天内; 血压特征:低血压,血压特征持续时间:三天内; 疼痛症状:头痛,疼痛指征:放射痛; 伴随症状:头晕、寒战、四肢乏力","外周神经疾病,脑膜炎","000099",55),
    ("2021-05-21 17:02:45",56,1,"2021-05-22 08:00:00",0,"2021-05-15 07:03:25","体温特征:超高热,体温特征持续时间:当天; 伴随症状:血尿、咯血","脾破裂,类风湿性关节炎","000053",56),
    ("2021-05-14 20:17:56",57,1,"2021-05-19 08:00:00",0,"2021-04-30 17:31:12","疼痛症状:胸痛,疼痛指征:按压痛; 伴随症状:心慌","脂溢性皮炎,红斑性肢痛症,视网膜脱落","000063",57),
    ("2021-05-16 06:33:39",58,1,"2021-05-17 13:00:00",1,"2021-04-27 21:15:03","疼痛症状:腰及骶部痛,疼痛指征:反复痛; 伴随症状:溃疡","青光眼","000091",58),
    ("2021-05-17 12:24:51",59,1,"2021-05-18 13:00:00",0,"2021-05-06 01:37:51","体温特征:驰长高热,体温特征持续时间:一周; 血压特征:高血压,血压特征持续时间:一周; 伴随症状:单纯疱疹、意识障碍、伴有水疱","脑卒中","000051",59),
    ("2021-05-20 20:30:36",60,1,"2021-05-22 13:00:00",0,"2021-05-18 08:26:06","血压特征:高血压,血压特征持续时间:三天内; 伴随症状:头晕、易困、关节肿痛","远视,肺错构瘤","000087",60),
    ("2021-05-20 21:34:23",61,1,"2021-05-22 13:00:00",0,"2021-05-08 03:06:30","体温特征:驰长高热,体温特征持续时间:当天; 血压特征:低血压,血压特征持续时间:半个月; 疼痛症状:颈部痛,疼痛指征:反复痛; 伴随症状:溃疡","手足口病","000061",61),
    ("2021-05-17 16:39:32",62,1,"2021-05-22 08:00:00",1,"2021-05-10 11:11:43","体温特征:连续低烧不退,体温特征持续时间:一个月以上; 伴随症状:意识障碍、血尿","牛皮癣,子宫肌瘤,巩膜炎","000095",62),
    ("2021-05-16 11:49:24",63,1,"2021-05-19 08:00:00",0,"2021-04-28 14:45:49","体温特征:不规则发热,体温特征持续时间:三天内; 血压特征:高血压,血压特征持续时间:一周; 疼痛症状:颌面部痛,疼痛指征:胀痛; 伴随症状:关节僵硬","小儿流行性肺炎","000049",63),
    ("2021-05-18 03:36:43",64,1,"2021-05-22 08:00:00",0,"2021-05-07 11:25:54","伴随症状:咳嗽伴有哮鸣音、水肿","鼻炎","000054",64),
    ("2021-05-13 17:34:26",65,1,"2021-05-16 08:00:00",0,"2021-04-28 21:49:55","体温特征:连续低烧不退,体温特征持续时间:当天; 疼痛症状:颈部痛,疼痛指征:急性痛; 伴随症状:呼吸困难、溃疡","小儿流行性肺炎","000087",65),
    ("2021-05-12 04:11:04",66,1,"2021-05-17 08:00:00",1,"2021-05-02 20:53:06","伴随症状:关节僵硬","先天性唇腭裂,盆腔炎","000089",66),
    ("2021-05-15 07:24:30",67,1,"2021-05-18 08:00:00",0,"2021-05-03 07:55:46","血压特征:高血压,血压特征持续时间:一个月以上; 疼痛症状:颌面部痛,疼痛指征:进展性痛; 伴随症状:喷嚏","牙周病","000097",67),
    ("2021-05-17 04:56:46",68,1,"2021-05-20 08:00:00",1,"2021-05-16 04:09:34","体温特征:不规则发热,体温特征持续时间:当天; 血压特征:高血压,血压特征持续时间:三天内; 伴随症状:水肿","职业性皮肤癌,肾破裂","000066",68),
    ("2021-05-14 08:44:11",69,1,"2021-05-16 13:00:00",1,"2021-05-02 17:00:00","疼痛症状:颌面部痛,疼痛指征:局部痛; 伴随症状:昏迷、咳嗽","中度烧伤,干眼","000031",69),
    ("2021-05-17 10:03:15",70,1,"2021-05-21 08:00:00",0,"2021-05-07 11:46:35","血压特征:低血压,血压特征持续时间:三天内; 伴随症状:咳嗽伴有哮鸣音、意识障碍、单纯疱疹","静脉曲张","000036",70),
    ("2021-05-16 11:25:30",71,2,"2021-05-20 08:00:00",0,"2021-05-02 21:03:34","体温特征:超高热,体温特征持续时间:三天内; 血压特征:高血压,血压特征持续时间:三天内; 疼痛症状:头痛,疼痛指征:进展性痛; 伴随症状:昏迷、易困、黄疸","复发性阿弗他性","000035",1),
    ("2021-05-12 16:43:41",72,2,"2021-05-17 08:00:00",0,"2021-05-01 18:19:56","体温特征:间歇低热,体温特征持续时间:三天内; 血压特征:低血压,血压特征持续时间:一周; 伴随症状:头晕、伴有水疱","尿路结石,法乐四联症","000065",2),
    ("2021-05-14 15:15:17",73,2,"2021-05-19 13:00:00",0,"2021-04-24 05:32:22","体温特征:驰长低热,体温特征持续时间:当天; 血压特征:高血压,血压特征持续时间:三天内; 伴随症状:恶心、活动障碍、淋巴结肿大","狼疮性肾炎","000041",3),
    ("2021-05-18 23:33:15",74,2,"2021-05-22 13:00:00",1,"2021-05-05 17:30:55","伴随症状:呼吸困难","脾破裂,肺炎","000059",4),
    ("2021-05-19 23:54:05",75,2,"2021-05-21 08:00:00",0,"2021-05-05 17:42:22","血压特征:高血压,血压特征持续时间:一个月; 疼痛症状:盆部痛,疼痛指征:按压痛; 伴随症状:易怒、食欲减退","鼻窦炎,重症肌无力","000061",5),
    ("2021-05-15 12:31:09",76,2,"2021-05-20 13:00:00",0,"2021-05-05 14:40:37","血压特征:高血压,血压特征持续时间:一个月以上; 疼痛症状:腰及骶部痛,疼痛指征:按压痛; 伴随症状:伴有红斑、黄疸","蛛网膜下腔出血,远视","000055",6),
    ("2021-05-15 08:23:22",77,2,"2021-05-17 08:00:00",1,"2021-05-09 11:13:05","疼痛症状:肩及上肢痛,疼痛指征:反复痛; 伴随症状:关节肿痛","支气管哮喘,糖尿病,脑卒中","000059",7),
    ("2021-05-15 04:04:07",78,2,"2021-05-19 13:00:00",0,"2021-05-13 17:34:16","体温特征:高热，大量出汗,体温特征持续时间:一个月; 血压特征:高血压,血压特征持续时间:一个月以上; 疼痛症状:肩及上肢痛,疼痛指征:绞痛; 伴随症状:单纯疱疹、意识障碍","冠心病","000049",8),
    ("2021-05-16 15:50:54",79,2,"2021-05-17 08:00:00",0,"2021-04-30 08:20:16","体温特征:高热，大量出汗,体温特征持续时间:半个月; 伴随症状:头晕、关节肿痛","白喉,荨麻疹,慢性咽炎","000107",9),
    ("2021-05-16 03:19:35",80,2,"2021-05-19 13:00:00",1,"2021-05-09 21:13:16","血压特征:高血压,血压特征持续时间:当天; 疼痛症状:颈部痛,疼痛指征:急性痛; 伴随症状:喷嚏","小儿支气管哮喘,干燥性角结膜炎,创伤性气胸","000047",10),
    ("2021-05-16 01:33:41",81,2,"2021-05-20 13:00:00",1,"2021-04-27 22:55:27","体温特征:高热惊厥,体温特征持续时间:一周; 疼痛症状:下肢痛,疼痛指征:按压痛; 伴随症状:关节僵硬、活动障碍","干燥性角结膜炎","000060",11),
    ("2021-05-15 22:52:25",82,2,"2021-05-16 13:00:00",0,"2021-05-01 09:44:21","体温特征:不规则发热,体温特征持续时间:一个月以上; 血压特征:高血压,血压特征持续时间:一个月以上; 疼痛症状:颈部痛,疼痛指征:急性痛; 伴随症状:单纯疱疹","重症肌无力","000101",12),
    ("2021-05-15 11:49:25",83,2,"2021-05-19 08:00:00",0,"2021-04-30 09:33:46","体温特征:高热惊厥,体温特征持续时间:当天; 疼痛症状:肩及上肢痛,疼痛指征:急性痛; 伴随症状:咯血","毛囊炎,沙眼","000051",13),
    ("2021-05-18 18:48:10",84,2,"2021-05-19 08:00:00",1,"2021-05-02 12:16:29","体温特征:间歇低热,体温特征持续时间:一个月以上; 血压特征:高血压,血压特征持续时间:一个月以上; 疼痛症状:头痛,疼痛指征:反复痛; 伴随症状:呼吸困难、结膜充血","牛皮癣,小儿支气管哮喘,粪类圆线虫病","000049",14),
    ("2021-05-17 03:23:21",85,2,"2021-05-22 08:00:00",0,"2021-05-14 06:32:21","血压特征:低血压,血压特征持续时间:一周; 疼痛症状:颈部痛,疼痛指征:急性痛; 伴随症状:食欲减退","高血压性心脏病,牛皮癣,小儿支气管哮喘","000039",15),
    ("2021-05-13 16:14:24",86,2,"2021-05-16 08:00:00",0,"2021-04-24 20:18:06","体温特征:连续低烧不退,体温特征持续时间:半个月; 伴随症状:食欲减退","先天性心脏病","000057",16),
    ("2021-05-20 23:42:15",87,2,"2021-05-22 08:00:00",0,"2021-05-08 17:24:25","体温特征:连续低烧不退,体温特征持续时间:一周; 血压特征:高血压,血压特征持续时间:三天内; 伴随症状:单纯疱疹、黄疸、溃疡","鼻咽癌,肺炎","000053",17),
    ("2021-05-15 16:02:08",88,2,"2021-05-17 08:00:00",0,"2021-05-14 14:56:35","体温特征:间歇低热,体温特征持续时间:一个月以上; 伴随症状:活动障碍","胰腺炎","000091",18),
    ("2021-05-15 01:17:59",89,2,"2021-05-19 13:00:00",0,"2021-04-28 05:02:11","体温特征:高热惊厥,体温特征持续时间:三天内; 伴随症状:喷嚏","胰腺炎","000105",19),
    ("2021-05-11 20:46:33",90,2,"2021-05-16 08:00:00",0,"2021-04-28 06:28:43","血压特征:低血压,血压特征持续时间:半个月; 疼痛症状:胸痛,疼痛指征:进展性痛; 伴随症状:恶心","肺气肿","000043",20),
    ("2021-05-14 12:54:04",91,2,"2021-05-16 13:00:00",1,"2021-04-25 10:38:25","血压特征:低血压,血压特征持续时间:当天; 伴随症状:关节僵硬","子宫肌瘤","000036",21),
    ("2021-05-13 11:00:27",92,2,"2021-05-16 13:00:00",1,"2021-05-02 04:26:15","体温特征:高热，大量出汗,体温特征持续时间:半个月; 伴随症状:单纯疱疹","红眼病,类风湿性关节炎","000085",22),
    ("2021-05-18 05:12:25",93,2,"2021-05-20 08:00:00",1,"2021-04-30 16:22:11","体温特征:超高热,体温特征持续时间:一个月以上; 血压特征:低血压,血压特征持续时间:一个月; 伴随症状:血尿、咳嗽伴有哮鸣音、咯血","小儿血友病,多发性颅内血肿,进行性肌营养不良","000101",23),
    ("2021-05-16 10:40:24",94,2,"2021-05-17 13:00:00",0,"2021-04-26 18:44:33","体温特征:连续低烧，午后加重,体温特征持续时间:半个月; 疼痛症状:下肢痛,疼痛指征:慢性痛; 伴随症状:关节僵硬、伴有水疱、呼吸困难","小儿黄水疮","000085",24),
    ("2021-05-13 04:17:48",95,2,"2021-05-16 08:00:00",0,"2021-04-26 19:48:51","体温特征:超高热,体温特征持续时间:一个月; 血压特征:低血压,血压特征持续时间:当天; 伴随症状:淋巴结肿大、单纯疱疹","小儿黄水疮,高血压","000097",25),
    ("2021-05-13 00:30:06",96,2,"2021-05-16 13:00:00",0,"2021-05-02 19:14:40","伴随症状:血尿","胃癌,冻伤,脾破裂","000045",26),
    ("2021-05-21 22:15:59",97,2,"2021-05-22 08:00:00",0,"2021-05-09 23:57:11","体温特征:高热，大量出汗,体温特征持续时间:一个月; 血压特征:低血压,血压特征持续时间:当天; 疼痛症状:盆部痛,疼痛指征:按压痛; 伴随症状:咳嗽伴有哮鸣音","智齿冠周炎,盆腔炎,慢性咽炎","000107",27),
    ("2021-05-11 21:49:09",98,2,"2021-05-16 08:00:00",0,"2021-05-08 18:21:40","体温特征:间歇高热,体温特征持续时间:一周; 血压特征:低血压,血压特征持续时间:一周; 疼痛症状:腹痛,疼痛指征:反复痛; 伴随症状:伴有红斑、咯血、易困","胰腺炎","000030",28),
    ("2021-05-11 12:19:04",99,2,"2021-05-16 13:00:00",1,"2021-04-23 16:31:24","体温特征:驰长高热,体温特征持续时间:三天内; 血压特征:低血压,血压特征持续时间:三天内; 伴随症状:淋巴结肿大、寒战","先天性心脏病,十二指肠溃疡,脂溢性皮炎","000109",29),
    ("2021-05-13 13:25:58",100,2,"2021-05-17 13:00:00",0,"2021-04-27 04:26:28","血压特征:低血压,血压特征持续时间:一周; 疼痛症状:盆部痛,疼痛指征:慢性痛; 伴随症状:单纯疱疹、心慌","脑出血","000054",30),
    ("2021-05-13 21:50:02",101,2,"2021-05-16 08:00:00",0,"2021-04-30 02:23:36","体温特征:间歇高热,体温特征持续时间:一个月以上; 疼痛症状:腹痛,疼痛指征:胀痛; 伴随症状:关节肿痛、伴有红斑、溃疡","中度烧伤","000060",31);

-- 入院信息登记
-- 入院日期,挂号信息记录编号,床位号,护理级别,住院天数,家属电话,即将出院状态,所属病区,所属科室
-- ([0-9]{4}-[0-9]{2}-[0-9]{2}),((?:[0-9]*,*){4}),([0-9]{11}),([0-9]),([A-Z]),([0-9])
--     ('$1',$2,'$3',$4,'$5',$6),
insert into inpatient_hospitalregistration values 
    ('2021-05-17',1,1,3,5,'13083380335',0,'A',2),
    ('2021-05-22',2,2,3,5,'18959571846',0,'A',2),
    ('2021-05-19',3,3,4,30,'13879910473',0,'A',2),
    ('2021-05-20',4,4,1,15,'13426618282',0,'A',2),
    ('2021-05-18',5,5,3,5,'13905342276',1,'A',2),
    ('2021-05-21',6,6,2,10,'15333951885',0,'A',2),
    ('2021-05-23',7,1,2,10,'15083487936',0,'B',2),
    ('2021-05-17',8,2,3,5,'15629478048',1,'B',2),
    ('2021-05-20',9,3,3,5,'13975090051',0,'B',2),
    ('2021-05-21',10,4,1,15,'13691988218',0,'B',2),
    ('2021-05-21',11,5,3,7,'13399883338',0,'B',2),
    ('2021-05-22',12,6,4,30,'13330683692',0,'B',2),
    ('2021-05-18',13,7,3,7,'13985010011',0,'B',2),
    ('2021-05-19',14,1,3,5,'17746578171',0,'C',2),
    ('2021-05-20',15,2,3,5,'15209439664',1,'C',2),
    ('2021-05-19',16,3,2,10,'18794319128',0,'C',2),
    ('2021-05-17',17,4,1,15,'18409022101',0,'C',2),
    ('2021-05-21',18,5,2,10,'15600780781',0,'C',2),
    ('2021-05-22',19,6,3,5,'16619733417',1,'C',2),
    ('2021-05-20',20,7,1,15,'13370033072',0,'C',2);
-- 手术信息
-- 手术日期,手术信息记录编号,手术编号,手术等级,手术名称,手术结果,手术持续时间,预后结果,缴费状态,挂号信息记录编号
insert into inpatient_operationinfo values 
    ('2021-05-25',1,1,1,'跟腱断裂修补术','经过顺利，目的完成',180,'预后良好',1,26),
    ('2021-05-19',2,1,1,'脊髓动静脉畸形切除术','经过顺利，成功切除',180,'预后良好',1,58),
    ('2021-05-19',3,1,2,'Omaya管置入术','经过顺利，目的完成',120,'预后不良',1,66),
    ('2021-05-26',4,1,3,'颅骨钻孔探查术','经过顺利，探查情况明晰',180,'预后良好',1,25),
    ('2021-05-20',5,1,3,'颅内多发血肿清除术','清除血肿70%',180 ,'预后良好',1,9),
    ('2021-05-26',6,1,3,'第四脑室肿瘤切除术','肿瘤未切除',240,'预后不良',1,10),
    ('2021-05-25',7,1,2,'脑脊膜膨出修补术','经过顺利，目的完成',180,'预后良好',1,43),
    ('2021-05-23',8,1,2,'颅缝骨化症整形术','经过顺利，目的完成',200,'预后良好',1,51),
    ('2021-05-22',9,1,1,'骨纤维异常增殖切除整形术','成功切除全部增殖组织',120,'预后良好',1,33),
    ('2021-05-26',10,1,1,'三叉神经撕脱术','经过顺利，目的完成',180,'预后较差',1,40),
    ('2021-05-22',11,1,2,'面神经简单修复术','修复达50%',180 ,'预后良好',1,4),
    ('2021-05-21',12,1,3,'迷路后前庭切断术','未完成完全切断',200,'预后良好',1,49),
    ('2021-05-23',13,1,4,'颅内动脉瘤包裹术','经过顺利，肿瘤未切除',180,'预后良好',1,16),
    ('2021-05-21',14,1,3,'指关节成形术','经过顺利，目的完成',120,'预后不良',1,27),
    ('2021-05-21',15,1,2,'带蒂复合组织瓣成形术','经过顺利，目的完成',180,'预后良好',1,38),
    ('2021-05-24',16,1,1,'手部关节松解术','经过顺利，目的完成',120,'预后较差',1,57),
    ('2021-05-18',17,1,2,'腕关节韧带修补术','经过顺利，目的完成',180,'预后良好',1,17),
    ('2021-05-23',18,1,4,'手外伤腹部埋藏皮瓣术','经过顺利，目的完成',150,'预后良好',1,39);

-- 护理记录
-- 护理时间,护理记录编号,收缩压,舒张压,体温,备注,责任护士工号,就诊号
-- ([0-9]{4}-[0-9]{2}-[0-9]{2}),([0-9]*),((?:[0-9]{2,3},){2})([0-9]{2}.[0-9]) ,(.*),([0-9]{6}),([0-9]*)
--     ('$1',$2,$3$4,'$5','$6',$7),
insert into inpatient_nursingrecord values 
    ('2021-05-18',1,120,80,36.8,'','000002',1),
    ('2021-05-23',2,155,110,36.5,'','000020',2),
    ('2021-05-20',3,115,79,36.8,'心率不齐','000034',3),
    ('2021-05-21',4,123,75,37.4,'','000038',4),
    ('2021-05-19',5,127,82,37.2,'轻度浮肿','000056',5),
    ('2021-05-22',6,117,81,37.4,'','000074',6),
    ('2021-05-24',7,120,75,37.3,'','000084',7),
    ('2021-05-18',8,121,89,36.6,'体检提醒，晚22:00禁食水','000088',8),
    ('2021-05-21',9,140,93,36.7,'','000092',9),
    ('2021-05-22',10,135,99,37.3,'','000002',10),
    ('2021-05-22',11,145,101,37.0,'','000020',11),
    ('2021-05-23',12,110,70,36.6,'','000034',12),
    ('2021-05-19',13,103,65,37.2,'次日5:00化验','000038',13),
    ('2021-05-20',14,100,70,36.9,'','000056',14),
    ('2021-05-21',15,120,81,37.0,'','000074',15),
    ('2021-05-20',16,125,78,36.9,'食欲不振','000084',16),
    ('2021-05-18',17,132,89,37.1,'','000088',17),
    ('2021-05-22',18,120,78,37.1,'','000092',18),
    ('2021-05-23',19,136,90,37.4,'平卧困难','000020',19),
    ('2021-05-21',20,144,93,37.2,'','000092',20);

-- 麻醉信息反馈
-- 手术信息记录编号,麻醉师工号,麻醉药品编号
insert into inpatient_narcoticinfo values 
    (1,3,'A00603'),
    (2,9,'A00604'),
    (3,15,'A00605'),
    (4,21,'A00606'),
    (5,3,'A00607'),
    (6,9,'A00608'),
    (7,15,'A00609'),
    (8,21,'A00610'),
    (9,3,'A00611'),
    (10,9,'A00612'),
    (11,15,'A00613'),
    (12,21,'A00614'),
    (13,3,'A00603'),
    (14,9,'A00604'),
    (15,15,'A00605'),
    (16,21,'A00606'),
    (17,3,'A00607'),
    (18,9,'A00608');

-- 处方文件
-- 开具时间,处方记录编号,药品种类数,医嘱,缴费状态,挂号记录编号
-- (^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}),([0-9]*),([0-9]* ),([^,]*),([01]),([0-9]*)
--     ('$1',$2,$3,'$4',$5,$6),
insert into outpatient_prescription values 
    ('2021-05-16 13:15:11',1,1 ,'用药:两日一次; 日常生活中应适度运动',0,1),
    ('2021-05-21 08:15:18',2,1 ,'用药:两日一次; 日常生活中应低蛋白饮食',0,2),
    ('2021-05-18 13:15:31',3,1 ,'用药:两日一次; 日常生活中应忌心情波动',0,3),
    ('2021-05-19 13:15:17',4,1 ,'用药:一日一次; 日常生活中应低蛋白饮食',0,4),
    ('2021-05-17 13:15:13',5,1 ,'用药:两日一次; 日常生活中应忌剧烈运动',0,5),
    ('2021-05-20 13:15:33',6,1 ,'用药:一日两次; 日常生活中应忌心情波动',0,6),
    ('2021-05-22 13:15:29',7,1 ,'用药:一日三次; 日常生活中应忌剧烈运动',0,7),
    ('2021-05-16 13:15:46',8,1 ,'用药:一日三次; 日常生活中应忌心情波动',0,8),
    ('2021-05-19 08:15:30',9,1 ,'用药:两日一次; 日常生活中应适度运动',0,9),
    ('2021-05-20 08:15:49',10,1 ,'用药:一日三次; 日常生活中应清淡饮食',0,10),
    ('2021-05-20 08:15:05',11,1 ,'用药:一日三次; 日常生活中应低蛋白饮食',0,11),
    ('2021-05-21 08:15:14',12,1 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,12),
    ('2021-05-17 08:15:28',13,1 ,'用药:一日两次; 日常生活中应低蛋白饮食',0,13),
    ('2021-05-18 13:15:37',14,1 ,'用药:一日两次; 日常生活中应注意平躺',0,14),
    ('2021-05-19 13:15:47',15,1 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,15),
    ('2021-05-18 13:15:43',16,1 ,'用药:一日一次; 日常生活中应适度运动',0,16),
    ('2021-05-16 08:15:20',17,1 ,'用药:两日一次; 日常生活中应注意平躺',0,17),
    ('2021-05-20 08:15:00',18,1 ,'用药:两日一次; 日常生活中应忌心情波动',0,18),
    ('2021-05-21 13:15:27',19,1 ,'用药:一日两次; 日常生活中应注意休息',0,19),
    ('2021-05-19 08:15:29',20,1 ,'用药:两日一次; 日常生活中应低蛋白饮食',0,20),
    ('2021-05-16 13:20:11',21,1 ,'用药:一日一次; 日常生活中应注意休息',0,1),
    ('2021-05-21 08:20:11',22,1 ,'用药:两日一次; 日常生活中应适度运动',0,2),
    ('2021-05-18 13:20:18',23,1 ,'用药:一日一次; 日常生活中应忌心情波动',0,3),
    ('2021-05-19 13:20:00',24,1 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,4),
    ('2021-05-17 13:20:06',25,1 ,'用药:一日一次; 日常生活中应忌剧烈运动',0,5),
    ('2021-05-20 13:20:29',26,1 ,'用药:一日一次; 日常生活中应注意平躺',0,6),
    ('2021-05-22 13:20:27',27,1 ,'用药:一日一次; 日常生活中应忌心情波动',0,7),
    ('2021-05-16 13:20:32',28,1 ,'用药:一日两次; 日常生活中应适度运动',0,8),
    ('2021-05-19 08:20:40',29,1 ,'用药:一日两次; 日常生活中应适度运动',0,9),
    ('2021-05-20 08:20:07',30,1 ,'用药:两日一次; 日常生活中应注意休息',0,10),
    ('2021-05-20 08:20:38',31,1 ,'用药:两日一次; 日常生活中应适度运动',0,11),
    ('2021-05-21 08:20:56',32,1 ,'用药:一日一次; 日常生活中应适度运动',0,12),
    ('2021-05-17 08:20:18',33,1 ,'用药:一日两次; 日常生活中应防晒',0,13),
    ('2021-05-18 13:20:31',34,1 ,'用药:一日两次; 日常生活中应清淡饮食',0,14),
    ('2021-05-19 13:20:20',35,1 ,'用药:两日一次; 日常生活中应适度运动',0,15),
    ('2021-05-18 13:20:59',36,1 ,'用药:一日三次; 日常生活中应忌剧烈运动',0,16),
    ('2021-05-16 08:20:01',37,1 ,'用药:一日两次; 日常生活中应忌食海鲜类食物',0,17),
    ('2021-05-20 08:20:44',38,1 ,'用药:一日两次; 日常生活中应清淡饮食',0,18),
    ('2021-05-21 13:20:30',39,1 ,'用药:一日两次; 日常生活中应低蛋白饮食',0,19),
    ('2021-05-19 08:20:43',40,1 ,'用药:一日两次; 日常生活中应忌食海鲜类食物',0,20),
    ('2021-05-16 13:23:19',41,1 ,'用药:一日一次; 日常生活中应高蛋白饮食',0,1),
    ('2021-05-21 08:23:01',42,1 ,'用药:一日三次; 日常生活中应注意休息',0,2),
    ('2021-05-18 13:23:40',43,1 ,'用药:一日三次; 日常生活中应适度运动',0,3),
    ('2021-05-19 13:23:56',44,1 ,'用药:一日三次; 日常生活中应低蛋白饮食',0,4),
    ('2021-05-17 13:23:22',45,1 ,'用药:一日两次; 日常生活中应适度运动',0,5),
    ('2021-05-20 13:23:06',46,1 ,'用药:一日两次; 日常生活中应注意平躺',0,6),
    ('2021-05-22 13:23:42',47,1 ,'用药:一日两次; 日常生活中应适度运动',0,7),
    ('2021-05-16 13:23:00',48,1 ,'用药:一日两次; 日常生活中应清淡饮食',0,8),
    ('2021-05-19 08:23:06',49,1 ,'用药:一日三次; 日常生活中应防晒',0,9),
    ('2021-05-20 08:23:33',50,1 ,'用药:一日三次; 日常生活中应低蛋白饮食',0,10),
    ('2021-05-20 08:23:24',51,1 ,'用药:一日一次; 日常生活中应注意平躺',0,11),
    ('2021-05-21 08:23:08',52,1 ,'用药:一日三次; 日常生活中应忌心情波动',0,12),
    ('2021-05-17 08:23:13',53,1 ,'用药:一日三次; 日常生活中应忌食海鲜类食物',0,13),
    ('2021-05-18 13:23:17',54,1 ,'用药:一日两次; 日常生活中应注意平躺',0,14),
    ('2021-05-19 13:23:03',55,1 ,'用药:一日三次; 日常生活中应清淡饮食',0,15),
    ('2021-05-18 13:23:11',56,1 ,'用药:两日一次; 日常生活中应防晒',0,16),
    ('2021-05-16 08:23:19',57,1 ,'用药:两日一次; 日常生活中应忌心情波动',0,17),
    ('2021-05-20 08:23:23',58,1 ,'用药:一日三次; 日常生活中应忌剧烈运动',0,18),
    ('2021-05-21 13:23:13',59,1 ,'用药:两日一次; 日常生活中应防晒',0,19),
    ('2021-05-19 08:23:06',60,1 ,'用药:两日一次; 日常生活中应适度运动',0,20),
    ('2021-05-17 13:11:50',61,7 ,'用药:一日三次; 日常生活中应忌剧烈运动',0,21),
    ('2021-05-22 13:26:10',62,1 ,'用药:一日三次; 日常生活中应注意平躺',0,22),
    ('2021-05-16 08:09:08',63,0 ,'用药:无需用药; 日常生活中应清淡饮食',1,23),
    ('2021-05-19 13:11:02',64,1 ,'用药:一日一次; 日常生活中应清淡饮食',1,24),
    ('2021-05-19 13:14:14',65,4 ,'用药:一日两次; 日常生活中应忌心情波动',0,25),
    ('2021-05-21 13:11:01',66,1 ,'用药:两日一次; 日常生活中应防晒',1,26),
    ('2021-05-17 08:24:52',67,0 ,'用药:无需用药; 日常生活中应清淡饮食',0,27),
    ('2021-05-17 13:11:23',68,1 ,'用药:一日三次; 日常生活中应高蛋白饮食',1,28),
    ('2021-05-17 13:29:49',69,4 ,'用药:两日一次; 日常生活中应适度运动',1,29),
    ('2021-05-17 13:09:12',70,0 ,'用药:无需用药; 日常生活中应注意休息',1,30),
    ('2021-05-22 08:25:23',71,3 ,'用药:一日一次; 日常生活中应清淡饮食',0,31),
    ('2021-05-21 08:28:42',72,8 ,'用药:一日一次; 日常生活中应注意休息',1,32),
    ('2021-05-19 13:11:27',73,8 ,'用药:一日三次; 日常生活中应注意平躺',0,33),
    ('2021-05-20 13:09:22',74,4 ,'用药:一日三次; 日常生活中应忌食海鲜类食物',0,34),
    ('2021-05-16 13:29:24',75,8 ,'用药:两日一次; 日常生活中应忌食海鲜类食物',0,35),
    ('2021-05-20 08:21:29',76,4 ,'用药:一日一次; 日常生活中应忌心情波动',1,36),
    ('2021-05-22 08:21:57',77,2 ,'用药:两日一次; 日常生活中应注意平躺',0,37),
    ('2021-05-18 08:09:48',78,7 ,'用药:一日一次; 日常生活中应注意休息',1,38),
    ('2021-05-19 13:06:17',79,7 ,'用药:一日两次; 日常生活中应适度运动',1,39),
    ('2021-05-22 08:17:39',80,5 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,40),
    ('2021-05-16 08:07:11',81,3 ,'用药:一日三次; 日常生活中应低蛋白饮食',1,41),
    ('2021-05-22 08:11:54',82,1 ,'用药:一日两次; 日常生活中应忌心情波动',1,42),
    ('2021-05-22 08:30:50',83,0 ,'用药:无需用药; 日常生活中应注意休息',0,43),
    ('2021-05-20 13:12:25',84,2 ,'用药:一日两次; 日常生活中应防晒',1,44),
    ('2021-05-17 08:23:02',85,4 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',1,45),
    ('2021-05-19 08:09:37',86,1 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',1,46),
    ('2021-05-20 08:11:22',87,0 ,'用药:无需用药; 日常生活中应适度运动',0,47),
    ('2021-05-17 08:07:07',88,6 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,48),
    ('2021-05-17 13:26:30',89,4 ,'用药:一日两次; 日常生活中应忌食海鲜类食物',1,49),
    ('2021-05-16 08:10:03',90,3 ,'用药:一日两次; 日常生活中应低蛋白饮食',1,50),
    ('2021-05-18 13:18:21',91,3 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,51),
    ('2021-05-16 13:17:40',92,8 ,'用药:一日两次; 日常生活中应低蛋白饮食',1,52),
    ('2021-05-22 13:13:39',93,7 ,'用药:一日三次; 日常生活中应低蛋白饮食',1,53),
    ('2021-05-22 13:07:50',94,1 ,'用药:一日一次; 日常生活中应防晒',1,54),
    ('2021-05-21 08:06:04',95,3 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',1,55),
    ('2021-05-22 08:15:03',96,2 ,'用药:两日一次; 日常生活中应注意平躺',0,56),
    ('2021-05-19 08:09:52',97,6 ,'用药:一日两次; 日常生活中应适度运动',1,57),
    ('2021-05-17 13:08:33',98,2 ,'用药:一日一次; 日常生活中应清淡饮食',1,58),
    ('2021-05-18 13:23:18',99,3 ,'用药:两日一次; 日常生活中应注意平躺',0,59),
    ('2021-05-22 13:25:30',100,2 ,'用药:两日一次; 日常生活中应低蛋白饮食',1,60),
    ('2021-05-22 13:30:35',101,5 ,'用药:一日一次; 日常生活中应清淡饮食',1,61),
    ('2021-05-22 08:20:18',102,2 ,'用药:一日三次; 日常生活中应忌心情波动',0,62),
    ('2021-05-19 08:26:26',103,0 ,'用药:无需用药; 日常生活中应注意休息',1,63),
    ('2021-05-22 08:22:47',104,3 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,64),
    ('2021-05-16 08:21:20',105,5 ,'用药:两日一次; 日常生活中应忌剧烈运动',0,65),
    ('2021-05-17 08:11:27',106,8 ,'用药:一日三次; 日常生活中应忌剧烈运动',1,66),
    ('2021-05-18 08:05:24',107,1 ,'用药:一日两次; 日常生活中应注意休息',0,67),
    ('2021-05-20 08:16:15',108,8 ,'用药:一日两次; 日常生活中应防晒',1,68),
    ('2021-05-16 13:11:57',109,1 ,'用药:一日两次; 日常生活中应低蛋白饮食',0,69),
    ('2021-05-21 08:22:57',110,1 ,'用药:一日两次; 日常生活中应防晒',1,70),
    ('2021-05-20 08:27:20',111,0 ,'用药:无需用药; 日常生活中应低蛋白饮食',1,71),
    ('2021-05-17 08:28:58',112,3 ,'用药:一日两次; 日常生活中应注意休息',0,72),
    ('2021-05-19 13:17:24',113,1 ,'用药:一日三次; 日常生活中应忌剧烈运动',0,73),
    ('2021-05-22 13:13:39',114,0 ,'用药:无需用药; 日常生活中应忌食海鲜类食物',0,74),
    ('2021-05-21 08:22:19',115,8 ,'用药:一日两次; 日常生活中应忌心情波动',1,75),
    ('2021-05-20 13:21:32',116,1 ,'用药:一日两次; 日常生活中应清淡饮食',1,76),
    ('2021-05-17 08:11:09',117,4 ,'用药:一日两次; 日常生活中应适度运动',0,77),
    ('2021-05-19 13:17:51',118,2 ,'用药:一日三次; 日常生活中应低蛋白饮食',0,78),
    ('2021-05-17 08:17:34',119,0 ,'用药:无需用药; 日常生活中应清淡饮食',1,79),
    ('2021-05-19 13:11:27',120,0 ,'用药:无需用药; 日常生活中应清淡饮食',0,80),
    ('2021-05-20 13:25:11',121,1 ,'用药:两日一次; 日常生活中应高蛋白饮食',1,81),
    ('2021-05-16 13:27:21',122,3 ,'用药:两日一次; 日常生活中应注意休息',1,82),
    ('2021-05-19 08:11:15',123,8 ,'用药:两日一次; 日常生活中应忌食海鲜类食物',0,83),
    ('2021-05-19 08:05:53',124,5 ,'用药:一日两次; 日常生活中应适度运动',1,84),
    ('2021-05-22 08:29:50',125,5 ,'用药:两日一次; 日常生活中应忌食海鲜类食物',1,85),
    ('2021-05-16 08:06:59',126,0 ,'用药:无需用药; 日常生活中应适度运动',0,86),
    ('2021-05-22 08:19:36',127,5 ,'用药:一日两次; 日常生活中应忌心情波动',1,87),
    ('2021-05-17 08:19:31',128,1 ,'用药:一日两次; 日常生活中应低蛋白饮食',1,88),
    ('2021-05-19 13:24:10',129,1 ,'用药:一日一次; 日常生活中应忌食海鲜类食物',0,89),
    ('2021-05-16 08:05:23',130,8 ,'用药:一日一次; 日常生活中应忌剧烈运动',1,90),
    ('2021-05-16 13:15:01',131,5 ,'用药:一日两次; 日常生活中应忌食海鲜类食物',0,91),
    ('2021-05-16 13:19:57',132,0 ,'用药:无需用药; 日常生活中应注意休息',1,92),
    ('2021-05-20 08:15:24',133,0 ,'用药:无需用药; 日常生活中应清淡饮食',1,93),
    ('2021-05-17 13:05:38',134,1 ,'用药:两日一次; 日常生活中应防晒',1,94),
    ('2021-05-16 08:26:25',135,8 ,'用药:一日一次; 日常生活中应清淡饮食',1,95),
    ('2021-05-16 13:28:05',136,5 ,'用药:一日一次; 日常生活中应适度运动',0,96),
    ('2021-05-22 08:22:42',137,1 ,'用药:一日三次; 日常生活中应清淡饮食',1,97),
    ('2021-05-16 08:10:50',138,6 ,'用药:一日两次; 日常生活中应注意平躺',1,98),
    ('2021-05-16 13:07:30',139,8 ,'用药:一日两次; 日常生活中应清淡饮食',0,99),
    ('2021-05-17 13:29:33',140,6 ,'用药:一日一次; 日常生活中应清淡饮食',1,100),
    ('2021-05-16 08:12:13',141,1 ,'用药:一日三次; 日常生活中应清淡饮食',1,101);
-- 处方细节
-- 处方细节记录编号,细节编号,药品数量,药品编号,处方记录编号
insert into outpatient_prescriptiondetail values 
    (1,1,7,'A00001',1),
    (2,1,7,'A00002',21),
    (3,1,7,'A00003',41),
    (4,1,7,'A00004',2),
    (5,1,7,'A00005',22),
    (6,1,7,'A00006',42),
    (7,1,7,'A00007',3),
    (8,1,7,'A00008',23),
    (9,1,7,'A00009',43),
    (10,1,7,'A00010',4),
    (11,1,7,'A00011',24),
    (12,1,7,'A00012',44),
    (13,1,7,'A00014',5),
    (14,1,7,'A00015',25),
    (15,1,7,'A00016',45),
    (16,1,7,'A00017',6),
    (17,1,7,'A00018',26),
    (18,1,7,'A00019',46),
    (19,1,7,'A00020',7),
    (20,1,7,'A00021',27),
    (21,1,7,'A00022',47),
    (22,1,7,'A00023',8),
    (23,1,7,'A00024',28),
    (24,1,7,'A00025',48),
    (25,1,7,'A00026',9),
    (26,1,7,'A00027',29),
    (27,1,7,'A00028',49),
    (28,1,7,'A00029',10),
    (29,1,7,'A00030',30),
    (30,1,7,'A00031',50),
    (31,1,7,'A00034',11),
    (32,1,7,'A00035',31),
    (33,1,7,'A00036',51),
    (34,1,7,'A00037',12),
    (35,1,7,'A00038',32),
    (36,1,7,'A00039',52),
    (37,1,7,'A00041',13),
    (38,1,7,'A00042',33),
    (39,1,7,'A00043',53),
    (40,1,7,'A00044',14),
    (41,1,7,'A00045',34),
    (42,1,7,'A00046',54),
    (43,1,7,'A00047',15),
    (44,1,7,'A00048',35),
    (45,1,7,'A00049',55),
    (46,1,7,'A00050',16),
    (47,1,7,'A00052',36),
    (48,1,7,'A00053',56),
    (49,1,7,'A00054',17),
    (50,1,7,'A00055',37),
    (51,1,7,'A00056',57),
    (52,1,7,'A00057',18),
    (53,1,7,'A00058',38),
    (54,1,7,'A00059',58),
    (55,1,7,'A00060',19),
    (56,1,7,'A00061',39),
    (57,1,7,'A00062',59),
    (58,1,7,'A00063',20),
    (59,1,7,'A00064',40),
    (60,1,7,'A00065',60),
    (61,1,7,'A00066',61),
    (62,2,7,'A00067',61),
    (63,3,7,'A00068',61),
    (64,4,7,'A00069',61),
    (65,5,7,'A00070',61),
    (66,6,7,'A00071',61),
    (67,7,7,'A00072',61),
    (68,1,7,'A00073',62),
    (69,1,7,'A00074',64),
    (70,1,7,'A00075',65),
    (71,2,7,'A00076',65),
    (72,3,7,'A00077',65),
    (73,4,7,'A00078',65),
    (74,1,7,'A00079',66),
    (75,1,7,'A00080',68),
    (76,1,7,'A00081',69),
    (77,2,7,'A00082',69),
    (78,3,7,'A00083',69),
    (79,4,7,'A00084',69),
    (80,1,7,'A00085',71),
    (81,2,7,'A00086',71),
    (82,3,7,'A00087',71),
    (83,1,7,'A00088',72),
    (84,2,7,'A00089',72),
    (85,3,7,'A00090',72),
    (86,4,7,'A00091',72),
    (87,5,7,'A00092',72),
    (88,6,7,'A00093',72),
    (89,7,7,'A00094',72),
    (90,8,7,'A00095',72),
    (91,1,7,'A00096',73),
    (92,2,7,'A00097',73),
    (93,3,7,'A00098',73),
    (94,4,7,'A00099',73),
    (95,5,7,'A00100',73),
    (96,6,7,'A00101',73),
    (97,7,7,'A00102',73),
    (98,8,7,'A00103',73),
    (99,1,7,'A00104',74),
    (100,2,7,'A00105',74),
    (101,3,7,'A00106',74),
    (102,4,7,'A00107',74),
    (103,1,7,'A00108',75),
    (104,2,7,'A00109',75),
    (105,3,7,'A00110',75),
    (106,4,7,'A00111',75),
    (107,5,7,'A00112',75),
    (108,6,7,'A00113',75),
    (109,7,7,'A00114',75),
    (110,8,7,'A00115',75),
    (111,1,7,'A00116',76),
    (112,2,7,'A00117',76),
    (113,3,7,'A00118',76),
    (114,4,7,'A00119',76),
    (115,1,7,'A00120',77),
    (116,2,7,'A00121',77),
    (117,1,7,'A00122',78),
    (118,2,7,'A00123',78),
    (119,3,7,'A00124',78),
    (120,4,7,'A00125',78),
    (121,5,7,'A00126',78),
    (122,6,7,'A00127',78),
    (123,7,7,'A00128',78),
    (124,1,7,'A00129',79),
    (125,2,7,'A00130',79),
    (126,3,7,'A00131',79),
    (127,4,7,'A00132',79),
    (128,5,7,'A00133',79),
    (129,6,7,'A00134',79),
    (130,7,7,'A00135',79),
    (131,1,7,'A00136',80),
    (132,2,7,'A00137',80),
    (133,3,7,'A00138',80),
    (134,4,7,'A00139',80),
    (135,5,7,'A00140',80),
    (136,1,7,'A00141',81),
    (137,2,7,'A00142',81),
    (138,3,7,'A00143',81),
    (139,1,7,'A00144',82),
    (140,1,7,'A00145',84),
    (141,2,7,'A00146',84),
    (142,1,7,'A00147',85),
    (143,2,7,'A00148',85),
    (144,3,7,'A00149',85),
    (145,4,7,'A00150',85),
    (146,1,7,'A00151',86),
    (147,1,7,'A00152',88),
    (148,2,7,'A00153',88),
    (149,3,7,'A00154',88),
    (150,4,7,'A00155',88),
    (151,5,7,'A00156',88),
    (152,6,7,'A00157',88),
    (153,1,7,'A00158',89),
    (154,2,7,'A00159',89),
    (155,3,7,'A00160',89),
    (156,4,7,'A00161',89),
    (157,1,7,'A00162',90),
    (158,2,7,'A00163',90),
    (159,3,7,'A00164',90),
    (160,1,7,'A00165',91),
    (161,2,7,'A00166',91),
    (162,3,7,'A00167',91),
    (163,1,7,'A00168',92),
    (164,2,7,'A00169',92),
    (165,3,7,'A00170',92),
    (166,4,7,'A00171',92),
    (167,5,7,'A00172',92),
    (168,6,7,'A00173',92),
    (169,7,7,'A00174',92),
    (170,8,7,'A00175',92),
    (171,1,7,'A00176',93),
    (172,2,7,'A00177',93),
    (173,3,7,'A00178',93),
    (174,4,7,'A00179',93),
    (175,5,7,'A00180',93),
    (176,6,7,'A00181',93),
    (177,7,7,'A00182',93),
    (178,1,7,'A00183',94),
    (179,1,7,'A00184',95),
    (180,2,7,'A00185',95),
    (181,3,7,'A00186',95),
    (182,1,7,'A00187',96),
    (183,2,7,'A00188',96),
    (184,1,7,'A00189',97),
    (185,2,7,'A00190',97),
    (186,3,7,'A00191',97),
    (187,4,7,'A00192',97),
    (188,5,7,'A00193',97),
    (189,6,7,'A00194',97),
    (190,1,7,'A00195',98),
    (191,2,7,'A00196',98),
    (192,1,7,'A00197',99),
    (193,2,7,'A00198',99),
    (194,3,7,'A00199',99),
    (195,1,7,'A00200',100),
    (196,2,7,'A00201',100),
    (197,1,7,'A00202',101),
    (198,2,7,'A00203',101),
    (199,3,7,'A00204',101),
    (200,4,7,'A00205',101),
    (201,5,7,'A00206',101),
    (202,1,7,'A00207',102),
    (203,2,7,'A00208',102),
    (204,1,7,'A00209',104),
    (205,2,7,'A00210',104),
    (206,3,7,'A00211',104),
    (207,1,7,'A00212',105),
    (208,2,7,'A00213',105),
    (209,3,7,'A00214',105),
    (210,4,7,'A00215',105),
    (211,5,7,'A00216',105),
    (212,1,7,'A00217',106),
    (213,2,7,'A00218',106),
    (214,3,7,'A00219',106),
    (215,4,7,'A00220',106),
    (216,5,7,'A00221',106),
    (217,6,7,'A00222',106),
    (218,7,7,'A00223',106),
    (219,8,7,'A00224',106),
    (220,1,7,'A00225',107),
    (221,1,7,'A00226',108),
    (222,2,7,'A00227',108),
    (223,3,7,'A00228',108),
    (224,4,7,'A00229',108),
    (225,5,7,'A00230',108),
    (226,6,7,'A00231',108),
    (227,7,7,'A00232',108),
    (228,8,7,'A00233',108),
    (229,1,7,'A00234',109),
    (230,1,7,'A00235',110),
    (231,1,7,'A00236',112),
    (232,2,7,'A00237',112),
    (233,3,7,'A00238',112),
    (234,1,7,'A00239',113),
    (235,1,7,'A00240',115),
    (236,2,7,'A00241',115),
    (237,3,7,'A00242',115),
    (238,4,7,'A00243',115),
    (239,5,7,'A00244',115),
    (240,6,7,'A00245',115),
    (241,7,7,'A00246',115),
    (242,8,7,'A00247',115),
    (243,1,7,'A00248',116),
    (244,1,7,'A00249',117),
    (245,2,7,'A00250',117),
    (246,3,7,'A00251',117),
    (247,4,7,'A00252',117),
    (248,1,7,'A00253',118),
    (249,2,7,'A00254',118),
    (250,1,7,'A00255',121),
    (251,1,7,'A00256',122),
    (252,2,7,'A00257',122),
    (253,3,7,'A00258',122),
    (254,1,7,'A00259',123),
    (255,2,7,'A00260',123),
    (256,3,7,'A00261',123),
    (257,4,7,'A00262',123),
    (258,5,7,'A00263',123),
    (259,6,7,'A00264',123),
    (260,7,7,'A00265',123),
    (261,8,7,'A00266',123),
    (262,1,7,'A00267',124),
    (263,2,7,'A00268',124),
    (264,3,7,'A00269',124),
    (265,4,7,'A00270',124),
    (266,5,7,'A00271',124),
    (267,1,7,'A00272',125),
    (268,2,7,'A00273',125),
    (269,3,7,'A00274',125),
    (270,4,7,'A00275',125),
    (271,5,7,'A00276',125),
    (272,1,7,'A00277',127),
    (273,2,7,'A00278',127),
    (274,3,7,'A00279',127),
    (275,4,7,'A00280',127),
    (276,5,7,'A00281',127),
    (277,1,7,'A00282',128),
    (278,1,7,'A00283',129),
    (279,1,7,'A00284',130),
    (280,2,7,'A00285',130),
    (281,3,7,'A00286',130),
    (282,4,7,'A00287',130),
    (283,5,7,'A00288',130),
    (284,6,7,'A00289',130),
    (285,7,7,'A00290',130),
    (286,8,7,'A00291',130),
    (287,1,7,'A00292',131),
    (288,2,7,'A00293',131),
    (289,3,7,'A00294',131),
    (290,4,7,'A00295',131),
    (291,5,7,'A00296',131),
    (292,1,7,'A00297',134),
    (293,1,7,'A00298',135),
    (294,2,7,'A00299',135),
    (295,3,7,'A00300',135),
    (296,4,7,'A00301',135),
    (297,5,7,'A00302',135),
    (298,6,7,'A00303',135),
    (299,7,7,'A00304',135),
    (300,8,7,'A00305',135),
    (301,1,7,'A00306',136),
    (302,2,7,'A00307',136),
    (303,3,7,'A00308',136),
    (304,4,7,'A00309',136),
    (305,5,7,'A00310',136),
    (306,1,7,'A00311',137),
    (307,1,7,'A00312',138),
    (308,2,7,'A00313',138),
    (309,3,7,'A00314',138),
    (310,4,7,'A00315',138),
    (311,5,7,'A00316',138),
    (312,6,7,'A00317',138),
    (313,1,7,'A00318',139),
    (314,2,7,'A00319',139),
    (315,3,7,'A00320',139),
    (316,4,7,'A00321',139),
    (317,5,7,'A00322',139),
    (318,6,7,'A00323',139),
    (319,7,7,'A00324',139),
    (320,8,7,'A00325',139),
    (321,1,7,'A00326',140),
    (322,2,7,'A00327',140),
    (323,3,7,'A00328',140),
    (324,4,7,'A00329',140),
    (325,5,7,'A00330',140),
    (326,6,7,'A00331',140),
    (327,1,7,'A00332',141);
