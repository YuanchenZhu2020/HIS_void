-- 设备信息 reference 设备类型
-- DB字段顺序：采购日期, 设备全局编号, 设备型号, 启用日期, 理论使用寿命（正整数）, 设备类型id
insert into laboratory_equipmentinfo values 
    ('2020-12-01', 1, 'Xray-BJ202101', '2021-01-01', 5, 1), 
    ('2020-12-01', 2, 'Xray-BJ202102', '2021-01-01', 5, 1), 
    ('2021-02-01', 3, 'Xray-BJ202101', '2021-02-15', 5, 1), 
    ('2021-02-01', 4, 'Xray-BJ202104', '2021-02-15', 8, 1), 
    ('2021-03-01', 5, 'Xray-BJ202101', '2021-03-15', 5, 1), 
    ('2021-03-01', 6, 'Xray-BJ202102', '2021-03-15', 5, 1), 
    ('2021-03-01', 7, 'Xray-BJ202104', '2021-03-15', 8, 1), 
    ('2021-05-01', 8, 'Xray-BJ202101', '2021-05-15', 5, 1), 
    ('2021-05-01', 9, 'Xray-BJ202102', '2021-05-15', 5, 1), 
    ('2021-05-01', 10, 'Xray-BJ202101', '2021-05-15', 5, 1), 
    ('2020-12-01', 11, 'Uit-BJ202101', '2021-01-01', 10, 2), 
    ('2020-12-01', 12, 'Uit-BJ202102', '2021-01-01', 10, 2), 
    ('2020-12-01', 13, 'Uit-BJ202103', '2021-01-01', 8, 2), 
    ('2021-03-01', 14, 'Uit-BJ202103', '2021-03-15', 8, 2), 
    ('2021-03-01', 15, 'Uit-BJ202102', '2021-03-15', 10, 2), 
    ('2020-12-01', 16, 'SYSMEX-F820', '2021-01-01', 10, 3), 
    ('2020-12-01', 17, 'SYSMEX-K1000', '2021-01-01', 20, 3), 
    ('2020-12-01', 18, 'SYSMEX-KX21', '2021-01-01', 15, 3), 
    ('2021-05-01', 19, 'SYSMEX-KX21N', '2021-05-15', 15, 3), 
    ('2021-05-01', 20, 'SYSMEX-K4500', '2021-05-15', 10, 3), 
    ('2021-05-01', 21, 'SYSMEX-SE9000', '2021-05-15', 20, 3), 
    ('2021-05-01', 22, 'SYSMEX-SF3000', '2021-05-15', 20, 3), 
    ('2020-12-01', 23, 'DisPET-BJ202101', '2021-01-01', 40, 4), 
    ('2020-12-01', 24, 'DisPET-BJ202102', '2021-01-01', 40, 4), 
    ('2020-12-01', 25, 'DisPET-BJ202103', '2021-01-01', 40, 4), 
    ('2020-12-01', 26, 'DisPET-BJ202104', '2021-01-01', 40, 4), 
    ('2020-12-01', 27, 'DisPET-BJ202105', '2021-01-01', 40, 4), 
    ('2020-12-01', 28, 'XWJ-BJ202101', '2021-01-01', 30, 5), 
    ('2020-12-01', 29, 'XWJ-BJ202102', '2021-01-01', 25, 5), 
    ('2021-03-01', 30, 'XWJ-BJ202101', '2021-03-15', 30, 5), 
    ('2021-03-01', 31, 'XWJ-BJ202102', '2021-03-15', 25, 5), 
    ('2021-05-01', 32, 'XWJ-BJ202101', '2021-05-15', 30, 5), 
    ('2021-05-01', 33, 'XWJ-BJ202103', '2021-05-15', 20, 5), 
    ('2021-05-01', 34, 'XWJ-BJ202103', '2021-05-15', 20, 5), 
    ('2021-05-01', 35, 'XWJ-BJ202108', '2021-05-15', 40, 5);
