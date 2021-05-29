import random


class DeptLocQuery:
    """
    根据科室名称或科室编号查询科室地址
    """
    def __init__(self, dept_name_or_id, is_outpatient = False, *args, **kwargs) -> None:
        self.dept_id = None
        self.dept_name = None
        self.is_outpatient = is_outpatient
        if isinstance(dept_name_or_id, int):
            self.dept_id = dept_name_or_id
        else:
            self.dept_name = dept_name_or_id
    
    def query(self):
        BUILDING = ["门诊部", "住院部", "康复中心", "信息部", "行政部"]
        FLOOR_RANGE = [1, 10]
        OUTPATIENT_ROOM_RANGE = [1, 20]
        DEPT_OUTPATIENT_ROOM_RANG = [1, 5]
        dept_loc = ""
        # 大楼
        if self.is_outpatient:
            dept_loc += BUILDING[0]
        else:
            dept_loc += random.choice(BUILDING[1:])
        # 楼层
        dept_loc += (str(random.randint(*FLOOR_RANGE)) + "层")
        # 门诊诊疗室
        if self.is_outpatient:
            num = random.randint(*DEPT_OUTPATIENT_ROOM_RANG)
            outpatient_room_ids = sorted(random.sample(range(*OUTPATIENT_ROOM_RANGE), num))
            dept_loc += '、'.join(map(str, outpatient_room_ids)) + "号诊疗室"
        
        return dept_loc
            
