from itertools import chain
import pymysql
from faker import Faker
import random

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
military_list = ['步兵', '摩托化步兵', '机械化步兵', '装甲兵', '炮兵', '陆军防空兵', '陆军航空兵',
                 '电子对抗兵', '工程兵', '通信兵', '防化兵', '侦察部队', '气象部队', '测绘部队']


def search_resident():
    sql = "SELECT person_id FROM dim_hrssb_personal  WHERE birth > DATE_SUB(CURDATE(),INTERVAL 45 YEAR)"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def search_people(pid):
    sql = "SELECT person_id, person_name, political_status, nation, person_phone, address FROM dim_hrssb_personal WHERE person_id = '{pid}';".format(pid=pid)
    cur.execute(sql)
    return cur.fetchone()


def insert_veteran(people_id, person_name, enlist_time, retire_time, military_age, retire_no, military_class,
                   political_status, nation, phone):
    sql = "INSERT INTO dim_ova_veteran() VALUES ('{people_id}', '{person_name}', '{enlist_time}', '{retire_time}', " \
          "'{military_age}', '{retire_no}', '{military_class}', '{political_status}', '{nation}', '{phone}')"\
        .format(people_id=people_id, person_name=person_name, enlist_time=enlist_time, retire_time=retire_time,
                military_age=military_age, retire_no=retire_no, military_class=military_class, political_status=political_status,
                nation=nation, phone=phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_veteran():
    people_id_list = search_resident()
    random.shuffle(people_id_list)
    for i in range(10000):
        people = search_people(people_id_list[i])
        person_id = people[0]
        person_name = people[1]
        enlist_time = str(int(person_id[6:10]) + random.randint(18, 22)) + "-0" + str(random.randint(1, 8)) + "-01"
        retire_time = str(int(enlist_time[0:4])+2)+enlist_time[4:]
        military_age = 2
        retire_no = fake.random_number(digits=8)
        military_class = random.choice(military_list)
        political_status = people[2]
        nation = people[3]
        phone = people[4]
        insert_veteran(person_id, person_name, enlist_time, retire_time, military_age, retire_no, military_class,
                       political_status, nation, phone)


if __name__ == '__main__':
    generate_veteran()
    cur.close()
