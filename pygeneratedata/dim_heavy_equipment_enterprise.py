import pymysql
from faker import Faker
import random
from openpyxl import load_workbook

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
workbook = load_workbook(filename="大型设备.xlsx")
sheet = workbook["Sheet1"]


def insert_heavy_equipment(unified_social_credit_identifier, enterprise_name, enterprise_address, response_person,
                           response_person_phone, legal_person, legal_person_id, legal_person_phone, qualification,
                           business_status):
    sql = "INSERT INTO dim_heavy_equipment_enterprise() VALUES ('{unified_social_credit_identifier}', " \
          "'{enterprise_name}', '{enterprise_address}', '{response_person}', '{response_person_phone}', " \
          "'{legal_person}', '{legal_person_id}', '{legal_person_phone}', '{qualification}', '{business_status}')"\
        .format(unified_social_credit_identifier=unified_social_credit_identifier, enterprise_name=enterprise_name,
                enterprise_address=enterprise_address, response_person=response_person, response_person_phone=response_person_phone,
                legal_person=legal_person, legal_person_id=legal_person_id, legal_person_phone=legal_person_phone, qualification=qualification,
                business_status=business_status)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_heavy_equipment_enterprise():
    emp_add_map = {}
    emp_cell = sheet["D1:D1389"]
    address_cell = sheet["G1:G1389"]
    for i in range(len(emp_cell)):
        x = emp_cell[i][0]
        y = address_cell[i][0]
        emp_add_map[x.value] = y.value
    for i in emp_add_map:
        unified_social_credit_identifier = fake.random_number(digits=18)
        enterprise_name = i
        enterprise_address = emp_add_map[i]
        f = random.randint(0, 10)  # 判断男女
        response_person = fake.name_male() if f == 0 else fake.name_female()
        response_person_phone = fake.phone_number()
        f = random.randint(0, 10)
        legal_person = fake.name_male() if f == 0 else fake.name_female()
        legal_person_id = fake.ssn()
        legal_person_phone = fake.phone_number()
        qualification = "已登记"
        business_status = "存续"
        insert_heavy_equipment(unified_social_credit_identifier, enterprise_name, enterprise_address, response_person,
                               response_person_phone, legal_person, legal_person_id, legal_person_phone, qualification,
                               business_status)


if __name__ == '__main__':
    generate_heavy_equipment_enterprise()
    cur.close()
