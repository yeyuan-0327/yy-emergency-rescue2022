from faker import Faker
import queue
import asyncio
from random import shuffle
import random
import pymysql


fake = Faker('zh_CN')

# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')

disable_list = ['视力残疾', '听力残疾', '言语残疾', '肢体残疾', '智力残疾', '精神残疾', '多重残疾']
disable_level = ['一级', '二级', '三级', '四级']


class MyQueue(asyncio.Queue):
    def shuffle(self):
        shuffle(self._queue)


# 从已存在于人口库中得到
def existed_people(cur):
    sql = "SELECT * FROM dim_psb_residents WHERE RAND() ORDER BY birth < '2000' LIMIT 6340"
    cur.execute(sql)
    return cur.fetchall()


# 插入到数据库
def insert_disable_person(person_id, person_name, nation, sex, birth, age, tel, marital_status, address, education, guardianship,
                          native_place, family_type, guardian_name, guardian_id, guardian_phone, disable_code,
                          is_military_disable, cur):
    sql = "INSERT INTO dim_df_disable_info() VALUES('{person_id}', '{person_name}', '{nation}', '{sex}', '{birth}', '{age}', '{tel}', " \
          "'{marital_status}', '{address}', '{education}', '{guardianship}', '{native_place}', '{family_type}', " \
          "'{guardian_name}', '{guardian_id}', '{guardian_phone}', '{disable_code}', '{is_military_disable}');"\
        .format(person_id=person_id, person_name=person_name, nation=nation, sex=sex, birth=birth, age=age, tel=tel,
                marital_status=marital_status, address=address, education=education, guardianship=guardianship,
                native_place=native_place, family_type=family_type, guardian_name=guardian_name, guardian_id=guardian_id,
                guardian_phone=guardian_phone, disable_code=disable_code, is_military_disable=is_military_disable)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


# 生成1000残疾人数据
def generate_not_exist1000(cur):
    q_id = queue.Queue(1000)

    while not q_id.empty():
        person_id = q_id.get()
        person_name = ''
        nation = ''
        sex = ''
        birth = ''
        age = ''
        marital_status = ''
        address = ''
        education = ''
        guardianship = ''
        native_place = ''
        family_type = ''
        # 从数据库中得到监护人
        guardian_name, guardian_id, guardian_phone = guardian_people(person_id, age, cur)
        disable_code = random.choice(disable_list) + random.choice(disable_level)
        is_military_disable = ''
        # insert_disable_person()
    pass


# 监护人信息
# 监护人不存在存在
def not_exist_guardian(param, cur):
    sql = "SELECT person_id FROM dim_df_disable_info WHERE person_id = '{person_id}'".format(person_id=param)
    cur.execute(sql)
    return cur.rowcount == 1


# 随机弹出监护人
def guardian_people(person_id, age, cur):
    sql = "SELECT person_id, person_name, person_phone FROM dim_hrssb_personal_info WHERE " \
          "person_id!='{person_id}' AND birth >= '{age}' ORDER BY RAND() LIMIT 1".format(person_id=person_id, age=2000-age)
    cur.execute(sql)
    rows = cur.fetchall()
    while not_exist_guardian(rows[0][0], cur):
        sql = "SELECT person_id, person_name, person_phone FROM dim_hrssb_personal_info WHERE " \
              "person_id!='{person_id}' AND birth >= '{age}' ORDER BY RAND() LIMIT 1".format(person_id=person_id,
                                                                                             age=1999 - age)
        cur.execute(sql)
        rows = cur.fetchall()
    return rows[0][0], rows[0][1], rows[0][2]


def generate_disable_people():
    cur = mysql_conn.cursor()
    exist_list = existed_people(cur)
    for i in exist_list:
        # print(i)
        person_id = i[0]
        person_name = i[1]
        nation = i[2]
        sex = i[3]
        birth = i[4]
        age = 2021 - int(str(birth).split('-')[0])
        tel = fake.phone_number()
        marital_status = i[-1]
        address = i[-4]
        education = i[5]
        guardianship = '父母'
        native_place = i[-3]
        family_type = i[6]
        # 从数据库中得到监护人
        guardian_name, guardian_id, guardian_phone = guardian_people(person_id, age, cur)
        disable_code = random.choice(disable_list) + random.choice(disable_level)
        is_military_disable = '否' if i[9] == 0 else '是'
        insert_disable_person(person_id, person_name, nation, sex, birth, age, tel, marital_status, address,
                              education, guardianship, native_place, family_type, guardian_name, guardian_id,
                              guardian_phone, disable_code, is_military_disable, cur)
    # for i in range(10):
    #     generate_not_exist1000(cur)
    cur.close()


if __name__ == '__main__':
    generate_disable_people()
