from django.utils import dateparse

import random


random.seed(36814)


class IDInfoQuery:

    FIRST_NAME_LIST = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', 
        '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', 
        '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', '奚', 
        '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', 
        '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', 
        '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '堪', '汪', '祁', 
        '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁'
    ]

    def __init__(self, idnum):
        self.idnum = idnum
    
    def get_birthday(self):
        year, month, day = self.idnum[6:10], self.idnum[10:12], self.idnum[12:14]
        return dateparse.parse_date("{}-{}-{}".format(year, month, day))
    
    def get_gender(self):
        return random.randint(0, 1)

    def gen_han_use_gb2312(self):
        # GB2312: [0xB0-0xF7][0xA1-0xFE]
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)
        val = f"{head:x}{body:x}"
        han_str = bytes.fromhex(val).decode("gb2312")
        return han_str

    def first_name(self):
        n = random.randint(0, len(IDInfoQuery.FIRST_NAME_LIST) - 1)
        f_name = IDInfoQuery.FIRST_NAME_LIST[n]
        return f_name

    def create_han_name(self, name_len:int):
        name = self.first_name()
        for i in range(name_len - 1):
            s = self.gen_han_use_gb2312()
            name += s
        return name
    
    def get_name(self):
        name_len = random.randint(2, 5)
        return self.create_han_name(name_len)
