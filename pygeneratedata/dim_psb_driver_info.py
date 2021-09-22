import pymysql
from faker import Faker
import random
from itertools import chain
import datetime


fake = Faker('zh_CN')
statue = ['正常', '正常', '正常', '正常', '正常', '正常', '超分', '超分', '撤销']
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')


def search(cur):
    sql = "SELECT t1.person_id FROM dim_psb_residents t1 ,( SELECT ROUND(DATEDIFF(CURDATE(), birth)/365.2422) AS age, person_id AS id FROM dim_psb_residents) t2 WHERE t1.person_id = t2.id AND age BETWEEN 18 AND 70;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def insert(person_id, name, sex, birth, certified_date, validity_date, drive_model, phone, certified_status, address,
           issue_authority, register_district, cur):
    sql = "INSERT INTO dim_psb_driver_info() VALUE('{person_id}'," \
          "'{name}','{sex}','{birth}','{certified_date}','{validity_date}','{drive_model}'," \
          "'{phone}','{certified_status}','{address}','{issue_authority}','{register_district}')".\
        format(person_id=person_id, name=name, sex=sex, birth=birth, certified_date=certified_date,
               validity_date=validity_date, drive_model=drive_model, phone=phone, certified_status=certified_status,
               address=address, issue_authority=issue_authority, register_district=register_district)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_driver():
    cur = mysql_conn.cursor()
    a = search(cur)
    random.shuffle(a)
    n = round(len(a) * 0.32)
    for i in range(n):
        sql = "SELECT person_id, person_name, sex, birth, address FROM dim_psb_residents WHERE person_id = '{person_id}'".\
            format(person_id=a[i])
        cur.execute(sql)
        p = cur.fetchone()
        year = int(str(p[3]).split("-")[0]) + 18 + random.randint(0, 10)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        certified_date = datetime.date(year, month, day)
        validity_date = datetime.date(year+6, month, day)
        drive_model = '小型汽车'
        certified_status = random.choice(statue)
        phone = fake.phone_number()
        issue_authority = "贵阳市公安局交通警察支队车辆管理所"
        register_district = '贵州省贵阳市白云区'
        insert(p[0], p[1], p[2], p[3], certified_date, validity_date, drive_model, phone, certified_status,
               p[4], issue_authority, register_district, cur)
    cur.close()


if __name__ == '__main__':
    generate_driver()
