import csv

ENCODING = "utf-8"
DELIMITER = "\t"
CSV_PATH = "./db_data_insert/通知知会科室.csv"
HEADERS = ["知会编号", "通知编号", "知会科室"]
NUM = 50
MAX_NOTICE = 9


notice_dept_csv = open(CSV_PATH, 'w', encoding = ENCODING, newline = "")
notice_dept_csv_w = csv.writer(notice_dept_csv, delimiter = DELIMITER)
notice_dept_csv_w.writerow(HEADERS)

datarows = []
j = 1
for i in range(1, NUM + 1):
    for n in range(1, MAX_NOTICE + 1):
        datarows.append((j, i, n))
        j += 1

notice_dept_csv_w.writerows(datarows)
notice_dept_csv.close()
