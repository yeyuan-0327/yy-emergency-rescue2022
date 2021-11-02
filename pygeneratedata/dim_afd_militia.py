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
military_list = ""


def search_resident():
    sql = "SELECT person_id FROM dim_hrssb_personal  WHERE birth > DATE_SUB(CURDATE(),INTERVAL 35 YEAR)"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def insert_militia(person_id, person_name, military_class, political_status, nation, address, phone):
    sql = "INSERT INTO dim_afd_militia() VALUES('{person_id}', '{person_name}', '{military_class}', " \
          "'{political_status}', '{nation}', '{address}', '{phone}')"\
        .format(person_id=person_id, person_name=person_name, military_class=military_class,
                political_status=political_status, nation=nation, address=address, phone=phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def is_veteran(person_id):
    sql = "SELECT person_id FROM dim_ova_veteran WHERE person_id='{person_id}';".format(person_id=person_id)
    cur.execute(sql)
    return cur.fetchone() is not None


def generate_militia():
    militia_list = search_resident()
    random.shuffle(militia_list)
    for i in range(10000):
        people = search_people(militia_list[i])
        person_id = people[0]
        person_name = people[1]
        age = datetime.datetime.now().year - int(person_id[6:10])
        military_class = "基干民兵" if (age < 28) & is_veteran(person_id) else "普通民兵"
        political_status = people[2]
        nation = people[3]
        phone = people[4]
        address = people[5]
        insert_militia(person_id, person_name, military_class, political_status, nation, address, phone)


if __name__ == '__main__':
    generate_militia()
    mysql_conn.close()
