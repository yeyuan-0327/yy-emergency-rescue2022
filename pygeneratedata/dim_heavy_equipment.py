import pymysql
from faker import Faker
import random
from openpyxl import load_workbook

from dim_mta_vehicle_driver import generate_number

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
workbook = load_workbook(filename="大型设备.xlsx")
sheet = workbook["Sheet1"]
range_list = ['南明', '云岩', '花溪', '乌当', '白云', '观山湖']
fuel_list = ['汽油', '柴油']


def InsertHeavyEquipment(equipment_no, affiliated_enterprise_unified_social_credit_identifier, equipment_class,
                         equipment_brand, equipment_model, address, fuel_type, actual_weight,
                         vehicle_color, use_condition, certified_no, certified_date, certified_out_date,
                         bound_name, bound_phone):
    sql = "INSERT INTO dim_heavy_equipment() VALUES ('{equipment_no}', '{affiliated_enterprise_unified_social_credit_identifier}', " \
          "'{equipment_class}', '{equipment_brand}', '{equipment_model}', '{address}', '{fuel_type}', " \
          "'{actual_weight}', '{vehicle_color}', '{use_condition}', '{certified_no}', '{certified_date}', '{certified_out_date}', " \
          "'{bound_name}', '{bound_phone}')"\
        .format(equipment_no=equipment_no, affiliated_enterprise_unified_social_credit_identifier=affiliated_enterprise_unified_social_credit_identifier,
                equipment_class=equipment_class, equipment_brand=equipment_brand, equipment_model=equipment_model,
                address=address, fuel_type=fuel_type, actual_weight=actual_weight, vehicle_color=vehicle_color, use_condition=use_condition,
                certified_no=certified_no, certified_date=certified_date, certified_out_date=certified_out_date,
                bound_name=bound_name, bound_phone=bound_phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def SearchCreditIdentifier(name):
    sql = "SELECT unified_social_credit_identifier FROM dim_heavy_equipment_enterprise WHERE enterprise_name = '{enterprise_name}';"\
        .format(enterprise_name=name)
    cur.execute(sql)
    return cur.fetchone()[0]


def GetEquipmentMapFromExcel():
    equipment_map = {}
    emp_cell = sheet["D1:D1389"]
    equipment_no_excel = sheet["K1:K1389"]
    equipment_class_excel = sheet["P1:P1389"]
    equipment_brand_excel = sheet["Y1:Y1389"]
    equipment_model_excel = sheet["I1:I1389"]
    equipment_use_condition_excel = sheet["N1:N1389"]
    certified_no_excel = sheet["Q1:Q1389"]
    certified_date_excel = sheet["R1:R1389"]
    certified_out_date_excel = sheet["S1:S1389"]
    address_excel = sheet["L1:L1389"]
    bound_name_excel = sheet["W1:W1389"]
    for i in range(len(equipment_no_excel)):
        eq_l = list()
        equipment_no = equipment_no_excel[i][0].value
        equipment_no = "无号牌" + str(i) if equipment_no == "" else equipment_no
        eq_l.append(emp_cell[i][0].value)  # 0
        eq_l.append(equipment_class_excel[i][0].value)  # 1
        eq_l.append(equipment_brand_excel[i][0].value)  # 2
        eq_l.append(equipment_model_excel[i][0].value)  # 3
        eq_l.append(equipment_use_condition_excel[i][0].value)  # 4
        eq_l.append(certified_no_excel[i][0].value)  # 5
        eq_l.append(certified_date_excel[i][0].value)  # 6
        eq_l.append(certified_out_date_excel[i][0].value)  # 7
        eq_l.append(address_excel[i][0].value)  # 8
        eq_l.append(bound_name_excel[i][0].value)  # 9
        equipment_map[equipment_no] = eq_l
    return equipment_map


def GenerateHeavyEquipment():
    equipment_map = GetEquipmentMapFromExcel()
    for i in equipment_map:
        equipment_no = i
        eq_l = equipment_map[i]
        affiliated_enterprise_unified_social_credit_identifier = SearchCreditIdentifier(eq_l[0])
        equipment_class = eq_l[1]
        equipment_brand = eq_l[2]
        equipment_model = eq_l[3]
        fuel_type = random.choice(fuel_list)
        actual_weight = str(random.randint(5, 20)) + "t"
        vehicle_color = fake.color_name()
        use_condition = eq_l[4]
        certified_no = eq_l[5]
        certified_date = eq_l[6]
        certified_out_date = eq_l[7]
        address = eq_l[8]
        bound_name = eq_l[9]
        bound_phone = fake.phone_number()
        InsertHeavyEquipment(equipment_no, affiliated_enterprise_unified_social_credit_identifier, equipment_class,
                             equipment_brand, equipment_model, address, fuel_type, actual_weight, vehicle_color, use_condition,
                             certified_no, certified_date, certified_out_date, bound_name, bound_phone)


if __name__ == '__main__':
    GenerateHeavyEquipment()
    cur.close()
