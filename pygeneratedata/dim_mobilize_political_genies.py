from itertools import chain
import pymysql
from faker import Faker
import random
import datetime

from dim_ova_veteran import search_people

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
school_list = list(filter(lambda x: x != '\n', open("school.txt", encoding='utf-8', errors='ignore').readlines()))
certified_list = ['新闻采编', '记者证', '律师', '教师']


def search_genies():
    sql = "SELECT person_id FROM dim_hrssb_personal WHERE political_status = '中共党员' ;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def insert_genies(person_id, person_name, phone, sex, nation, political_status, marital_status, age, address, birth,
                  graduate_school, education, certified, work_year):
    sql = "INSERT INTO dim_mobilize_political_genies() VALUES ('{person_id}', '{person_name}', '{phone}', '{sex}', '{nation}', " \
          "'{political_status}', '{marital_status}', '{age}', '{address}', '{birth}', '{graduate_school}', '{education}', " \
          "'{certified}', '{work_year}')".format(person_id=person_id, person_name=person_name, phone=phone, sex=sex,
                                                 nation=nation,
                                                 political_status=political_status, marital_status=marital_status,
                                                 age=age,
                                                 address=address, birth=birth, graduate_school=graduate_school,
                                                 education=education,
                                                 certified=certified, work_year=work_year)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def search_marry(person_id):
    sql = "SELECT person_id FROM dim_cab_marriage WHERE person_id='{person_id}';".format(person_id=person_id)
    cur.execute(sql)
    return cur.fetchone() is None


def search_school(person_id):
    sql = "SELECT graduate_school FROM dim_eb_student WHERE person_id='{person_id}';".format(person_id=person_id)
    cur.execute(sql)
    return cur.fetchone()


def generate_genies():
    genies_list = search_genies()
    random.shuffle(genies_list)
    for i in genies_list:
        people = search_people(i)
        person_id = people[0]
        person_name = people[1]
        political_status = people[2]
        nation = people[3]
        phone = people[4]
        address = people[5]
        sex = people[6]
        birth = people[7]
        marital_status = '未婚' if search_marry(person_id) else '已婚'
        age = datetime.datetime.now().year - int(person_id[6:10])
        graduate_school = search_school(person_id)[0] if search_school(person_id) is not None else random.choice(
            school_list)
        education = people[8]
        is_certified = random.choice(certified_list)
        work_year = random.randint(1, 8)
        insert_genies(person_id, person_name, phone, sex, nation, political_status, marital_status, age, address, birth,
                      graduate_school, education, is_certified, work_year)


if __name__ == '__main__':
    generate_genies()
    mysql_conn.close()
