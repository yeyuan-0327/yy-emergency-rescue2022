import pymysql
from faker import Faker
import random
from itertools import chain

from dim_mta_transport_enterprise import random_generate_date
from dim_mta_vehicle_driver import generate_number

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
fuel_list = ['汽油', '柴油', '油电混合', '纯电动', '插电式混合动力', '增程式']
brand_list = ['解放FAW', '东风DFM', '中国重汽CNHTC', '福田欧曼AUMAN', '江淮汽车JAC', '上汽红岩', '大运DAYUN', '北奔重汽',
              '华菱星马CAMC', '三一重卡SANY', '比亚迪']
range_list = ['南明', '云岩', '花溪', '乌当', '白云', '观山湖', '清镇', '开阳', '息烽', '修文']
driver_model_list = ['大型客车', '牵引车', '城市公交车', '中型客车', '大型货车']
color_list = ['红', '黄', '蓝', '绿', '青', '白', '黑', '橙色']


def random_type():
    wd = list('A B C D E F G H I 1 2 3 4 5 6 7 8 9 0 J K L M N O P Q R S T U V W X Y Z'.split(' '))
    i = 12
    res = ''
    while i > 0:
        res += random.choice(wd)
        i -= 1
    return res


def random_address():
    sql = "SELECT transport_enterprise_address FROM dim_mta_transport_enterprise;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def insert_vehicle(vehicle_no, area, drive_model, fuel_type, vehicle_type, vehicle_brand, address, phone, passenger_num,
                   actual_weight, vehicle_color, register_date, expiration_date, insurance_end, transport_range):
    sql = "INSERT INTO dim_mta_vehicle() VALUES ('{vehicle_no}', '{area}', '{drive_model}', " \
          "'{fuel_type}', '{vehicle_type}', '{vehicle_brand}', '{address}', '{phone}', '{passenger_num}', " \
          "'{actual_weight}', '{vehicle_color}', '{register_date}', '{expiration_date}', '{insurance_end}', '{transport_range}')"\
        .format(vehicle_no=vehicle_no, area=area, drive_model=drive_model, fuel_type=fuel_type, vehicle_type=vehicle_type,
                vehicle_brand=vehicle_brand, address=address, phone=phone, passenger_num=passenger_num, actual_weight=actual_weight,
                vehicle_color=vehicle_color, register_date=register_date, expiration_date=expiration_date, insurance_end=insurance_end,
                transport_range=transport_range)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_vehicle():
    add = random_address()
    s = set()
    while len(s) != 10000:
        s.add(generate_number())
    while len(s) > 0:
        vehicle_no = s.pop()
        area = "贵阳市"
        drive_model = random.choice(driver_model_list)
        fuel_type = random.choice(fuel_list)
        vehicle_type = random_type()
        vehicle_brand = random.choice(brand_list)
        address = random.choice(add)
        phone = fake.phone_number()
        passenger_num = 2 if (drive_model != "城市公交车") | (drive_model != "大型客车") else random.randint(10, 30)
        actual_weight = str(random.randint(10, 20)) + "t"
        vehicle_color = random.choice(color_list)
        year, month, day = random_generate_date()
        register_date = year + month + day
        expiration_date = str(int(year) + 6) + month + day
        insurance_end = str(int(year) + 1) + month + day
        transport_range = random.choice(range_list) + "-" + random.choice(range_list)
        insert_vehicle(vehicle_no, area, drive_model, fuel_type, vehicle_type, vehicle_brand, address,
                       phone, passenger_num, actual_weight, vehicle_color, register_date, expiration_date,
                       insurance_end, transport_range)


if __name__ == '__main__':
    generate_vehicle()
    mysql_conn.close()
