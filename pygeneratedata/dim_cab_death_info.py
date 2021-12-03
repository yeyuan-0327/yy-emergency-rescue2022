import pymysql
from itertools import chain
import random
import datetime
from dateutil.relativedelta import relativedelta

# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')


def search(cur):
    sql = "SELECT t1.person_id FROM dim_psb_residents t1 ,(SELECT ROUND(DATEDIFF(CURDATE(), birth)/365.2422) AS age, person_id AS id FROM dim_psb_residents) t2 WHERE t1.person_id = t2.id AND age > 40;"
    cur.execute(sql)
    return list(chain.from_iterable(cur.fetchall()))


def insert(person_id, name, is_death, death_date, cur):
    sql = "INSERT INTO dim_cab_death_info() VALUES('{person_id}', '{name}', '{is_death}', '{death_date}')"\
        .format(person_id=person_id, name=name, is_death=is_death, death_date=death_date)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_data():
    cur = mysql_conn.cursor()
    a = search(cur)
    random.shuffle(a)
    n = round(len(a) * 0.0704)  # 2020年中国人口死亡率7.07‰
    for i in range(n):
        sql = "SELECT  person_id, person_name, birth FROM dim_psb_residents WHERE person_id='{person_id}';".format(person_id=a[i])
        cur.execute(sql)
        p = cur.fetchone()
        person_id = p[0]
        name = p[1]
        is_death = '是'
        death_date = p[2] + relativedelta(years=random.randint(30, 80)) + datetime.timedelta(days=random.randint(1, 180))
        insert(person_id, name, is_death, death_date, cur)


if __name__ == '__main__':
    generate_data()
