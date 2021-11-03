import pymysql
from faker import Faker
import random
from itertools import chain

from dim_mta_transport_enterprise import random_generate_date

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
driver_model_list = ['大型客车', '牵引车', '城市公交车', '中型客车', '大型货车']


def search_driver():
    sql = ""
    cur.execute(sql)
    return cur.fetchall()


def generate_number():
    code = ""
    li = list('A B C D E F G H'.split(' '))
    ll = list('A B C D E F G H 1 2 3 4 5 6 7 8 9 0'.split(' '))
    for i in range(5):
        code += random.choice(ll)
    return '贵' + random.choice(li) + '-' + code


def get_enterprise_no():
    sql = "SELECT unified_social_credit_identifier FROM dim_mta_transport_enterprise;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def search_random_address():
    sql = "SELECT address FROM dim_psb_residents;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def search_enterprise():
    sql = "SELECT unified_social_credit_identifier FROM dim_msb_enterprise;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def insert_vehicle_driver(person_id, person_name, bound_vehicle, affiliated_enterprise, phone, work_year,
                          certified_date, validity_date, area, sex, address, drive_model, certified_status,
                          point_deduction, zhima_credit, service_unit):
    sql = "INSERT INTO dim_mta_vehicle_driver() VALUES ('{person_id}', '{person_name}', '{bound_vehicle}', '{affiliated_enterprise}', " \
          "'{phone}', '{work_year}', '{certified_date}', '{validity_date}', '{area}', '{sex}', '{address}', '{drive_model}', " \
          "'{certified_status}', '{point_deduction}', '{zhima_credit}', '{service_unit}');"\
        .format(person_id=person_id, person_name=person_name, bound_vehicle=bound_vehicle, affiliated_enterprise=affiliated_enterprise,
                phone=phone, work_year=work_year, certified_date=certified_date, validity_date=validity_date, area=area, sex=sex,
                address=address, drive_model=drive_model, certified_status=certified_status, point_deduction=point_deduction, zhima_credit=zhima_credit,
                service_unit=service_unit)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_vehicle_driver():
    enter_id_list = get_enterprise_no()
    address_list = search_random_address()
    enter_list = search_enterprise()
    for i in range(10000):
        person_id = "520100" + str(random.randint(1980, 2000)) + fake.ssn()[10:]
        f = random.randint(0, 10)
        person_name = fake.name_male() if f == 0 else fake.name_female()
        bound_vehicle = generate_number()
        affiliated_enterprise = random.choice(enter_id_list)
        phone = fake.phone_number()
        work_year = random.randint(3, 20)
        year, month, day = random_generate_date()
        certified_date = year + month + day
        validity_date = str(int(year) + 6) + month + day
        area = "贵阳市"
        sex = "女" if f == 0 else "男"
        address = random.choice(address_list)
        drive_model = random.choice(driver_model_list)
        certified_status = "正常"
        point_deduction = random.randint(0, 9)
        zhima_credit = random.randint(600, 799)
        service_unit = random.choice(enter_list)
        insert_vehicle_driver(person_id, person_name, bound_vehicle, affiliated_enterprise, phone, work_year,
                              certified_date, validity_date, area, sex, address, drive_model, certified_status,
                              point_deduction, zhima_credit, service_unit)


if __name__ == '__main__':
    generate_vehicle_driver()
    mysql_conn.close()
