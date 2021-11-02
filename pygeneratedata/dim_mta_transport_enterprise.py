import pymysql
from faker import Faker
import random

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
tra_enter_list = open("transport_enterprise.txt", encoding='utf-8', errors='ignore').readlines()


def random_generate_date():
    year = str(random.randint(2011, 2021))
    month = "-0" + str(random.randint(1, 9))
    day = "-" + str(random.randint(10, 28))
    return year, month, day


def insert_transport_enter(unified_social_credit_identifier, enterprise_name,
                           transport_class, certified_date, certified_no, legal_person, legal_person_phone,
                           validity_date, business_scope, transport_enterprise_address, transport_range):
    sql = "INSERT INTO dim_mta_transport_enterprise() VALUES ('{unified_social_credit_identifier}', '{enterprise_name}', " \
          "'{transport_class}', '{certified_date}', '{certified_no}', '{legal_person}', " \
          "'{legal_person_phone}', '{validity_date}', '{business_scope}', '{transport_enterprise_address}', '{transport_range}');"\
        .format(unified_social_credit_identifier=unified_social_credit_identifier, enterprise_name=enterprise_name,
                transport_enterprise_address=transport_enterprise_address, transport_class=transport_class,
                certified_date=certified_date, certified_no=certified_no, legal_person=legal_person,
                legal_person_phone=legal_person_phone, validity_date=validity_date, business_scope=business_scope,
                transport_range=transport_range)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_transport():
    for i in tra_enter_list:
        temp_enter = i.split('\t')
        unified_social_credit_identifier = fake.random_number(digits=18)
        enterprise_name = temp_enter[0]
        transport_enterprise_address = temp_enter[1]
        transport_class = temp_enter[2].replace('\n', '')
        year, month, day = random_generate_date()
        certified_date = year + month + day
        certified_no = fake.random_number(digits=12)
        legal_person = fake.name()
        legal_person_phone = fake.phone_number()
        validity_date = str(int(year)+10) + month + day
        business_scope = "工业、交通、邮政、交通运输、交通运输管理部门和机构"
        transport_range = "贵阳"
        insert_transport_enter(unified_social_credit_identifier, enterprise_name,
                               transport_class, certified_date, certified_no, legal_person, legal_person_phone,
                               validity_date, business_scope, transport_enterprise_address, transport_range)


if __name__ == '__main__':
    generate_transport()
    mysql_conn.close()
