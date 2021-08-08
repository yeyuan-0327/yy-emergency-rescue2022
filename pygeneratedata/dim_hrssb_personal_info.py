from faker import Faker
import queue
import asyncio
from random import shuffle
import random
import pymysql

fake = Faker('zh_CN')
Blood_type = ['A型血', 'B型血', 'AB型血', 'O型血']
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')


# 从居民表中找出有工作的人
def get_resident(cur):
    sql = 'SELECT person_id, person_name, nation, sex, birth, education, family_type, military_status, ' \
          'address, occupation ' \
          'FROM dim_psb_residents WHERE birth < \'2013\' AND occupation <> \'无职业\';'
    print(sql)
    cur.execute(sql)
    return cur.fetchall()


# 插入单条个人数据
def insertInfoToPersonal(person_id, person_name, nation, sex, birth, education, family_type,
                         unit_social_credit_identifier, unit_name, person_status,
                         person_phone, address, is_peasant_worker, political_status, blood_type, bank_account, email,
                         military_serviced, cancel_mark, cur):
    sql = "INSERT INTO dim_hrssb_personal_info() VALUES('{person_id}', '{person_name}', '{nation}', '{sex}', " \
          "'{birth}', '{education}', '{family_type}', '{unit_social_credit_identifier}', '{unit_name}', " \
          "'{person_status}', '{person_phone}', '{address}', '{is_peasant_worker}', '{political_status}', " \
          "'{blood_type}', '{bank_account}', '{email}', '{military_serviced}', '{cancel_mark}');"\
        .format(person_id=person_id, person_name=person_name, nation=nation, sex=sex, birth=birth, education=education,
                family_type=family_type, unit_social_credit_identifier=unit_social_credit_identifier,
                unit_name=unit_name, person_status=person_status, person_phone=person_phone, address=address,
                is_peasant_worker=is_peasant_worker, political_status=political_status, blood_type=blood_type,
                bank_account=bank_account, email=email, military_serviced=military_serviced, cancel_mark=cancel_mark)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


# 随机弹出单位统一社会号和名称
def pop_unit(cur):
    sql = "SELECT unified_social_credit_identifier,enterprise_name FROM qcc_enterprise_spider order by RAND() LIMIT 1;"
    cur.execute(sql)
    data = cur.fetchone()
    return data[0], data[1]


# 生成政治面貌队列
class MyQueue(asyncio.Queue):
    def shuffle(self):
        shuffle(self._queue)


async def generate_political():
    q_data = MyQueue()
    for i in range(70):
        await q_data.put('中共党员')
    for i in range(70):
        await q_data.put('预备党员')
    for i in range(160):
        await q_data.put('工青团员')
    for i in range(600):
        await q_data.put('群众')
    for i in range(20):
        await q_data.put('民革会员')
    for i in range(10):
        await q_data.put('民盟盟员')
    for i in range(10):
        await q_data.put('民建会员')
    for i in range(10):
        await q_data.put('民进会员')
    for i in range(10):
        await q_data.put('农工党党员')
    for i in range(10):
        await q_data.put('致公党党员')
    for i in range(10):
        await q_data.put('九三学社社员')
    for i in range(10):
        await q_data.put('台盟盟员')
    for i in range(10):
        await q_data.put('无党派人士')
    q_data.shuffle()
    q_n = queue.Queue(1000)
    while not q_data.empty():
        item = await q_data.get()
        q_n.put(item)
    return q_n


# 获取政治面貌
def get_political():
    global q_political
    if not q_political.empty():
        political_status = q_political.get()
    else:
        q_political = asyncio.run(generate_political())
        political_status = q_political.get()
    return political_status


def generate_HRSSB_personal():
    cur = mysql_conn.cursor()
    person_list = get_resident(cur)
    for i in person_list:
        person_id = i[0]
        person_name = i[1]
        nation = i[2]
        sex = i[3]
        birth = i[4]
        education = i[5]
        family_type = i[6]
        unit_social_credit_identifier, unit_name = pop_unit(cur)
        person_status = '在职'
        if random.randint(1, 1000) == 88:
            person_status = '离职'
        person_phone = fake.phone_number()
        military_status = i[7]
        address = i[8]
        # 农村户口 + 运输及农等职业 + 1/5 可能性
        is_peasant_worker = '0'
        if (family_type == '农村户口') & (i[9] == '生产、运输设备操作人员及有关人员' or i[9] == '农、林、牧、渔、水利业生产人员') \
                & (random.randint(1, 5) == 1):
            is_peasant_worker = '1'
        # if q != empty q.get() else q = generate_political()
        political_status = get_political()
        blood_type = random.choice(Blood_type)  # 血型任一弹出
        bank_account = fake.ean8() + fake.ean8() + str(random.randint(100, 999))
        email = fake.email()
        military_serviced = '0'  # 退役军人 + 国企 = 是
        if ('国家' in i[9]) & (military_status == 1):
            military_serviced = '1'
            political_status = '中共党员'
        cancel_mark = '未注销'
        if (sex == '男') & ((2021 - int(birth.strftime('%Y-%m-%d').split('-')[0])) >= 65) or (sex == '女') & \
                (2021 - int(birth.strftime('%Y-%m-%d').split('-')[0]) >= 60) & (random.randint(1, 5) == 3):
            cancel_mark = '退休'
        if cancel_mark == '退休':
            person_status = '离职'
        insertInfoToPersonal(person_id, person_name, nation, sex, birth, education, family_type,
                             unit_social_credit_identifier, unit_name, person_status,
                             person_phone, address, is_peasant_worker, political_status, blood_type, bank_account,
                             email, military_serviced, cancel_mark, cur)
    cur.close()


if __name__ == '__main__':
    q_political = asyncio.run(generate_political())
    generate_HRSSB_personal()
