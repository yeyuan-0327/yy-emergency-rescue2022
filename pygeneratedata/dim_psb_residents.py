from faker import Faker
import queue
import asyncio
from random import shuffle
import random
import psycopg2
import pymysql

fake = Faker('zh_CN')
# 连接PostgreSQL数据库
pg_conn = psycopg2.connect(database='postgres', user='postgres', password='gpadmin', host='192.168.101.105',
                           port='54321')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')


# 按比例生成的民族打乱顺序
class MyQueue(asyncio.Queue):
    def shuffle(self):
        shuffle(self._queue)


async def generate_nation():
    q_nation = MyQueue()
    for i in range(652):
        await q_nation.put('汉族')
    for i in range(122):
        await q_nation.put('苗族')
    for i in range(79):
        await q_nation.put('布依族')
    for i in range(46):
        await q_nation.put('侗族')
    for i in range(41):
        await q_nation.put('土家族')
    for i in range(24):
        await q_nation.put('彝族')
    for i in range(16):
        await q_nation.put('仡佬族')
    for i in range(10):
        await q_nation.put('水族')
    for i in range(5):
        await q_nation.put('白族')
    for i in range(5):
        await q_nation.put('回族')
    q_nation.shuffle()

    q_n = queue.Queue(1000)
    while not q_nation.empty():
        item = await q_nation.get()
        q_n.put(item)
    return q_n


# 生成出生日期
async def generate_birth():
    q_data = MyQueue()
    for i in range(240):
        year = str(2021 - random.randint(0, 14))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        if int(month) < 10:
            month = "0" + month
        if int(day) < 10:
            day = "0" + day
        birth = year + "-" + month + "-" + day
        await q_data.put(birth)
    for i in range(607):
        year = str(2021 - random.randint(15, 59))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        if int(month) < 10:
            month = "0" + month
        if int(day) < 10:
            day = "0" + day
        birth = year + "-" + month + "-" + day
        await q_data.put(birth)
    for i in range(153):
        year = str(2021 - random.randint(60, 80))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        if int(month) < 10:
            month = "0" + month
        if int(day) < 10:
            day = "0" + day
        birth = year + "-" + month + "-" + day
        await q_data.put(birth)
    q_data.shuffle()
    q_n = queue.Queue(1000)
    while not q_data.empty():
        item = await q_data.get()
        q_n.put(item)
    return q_n


# 生成教育
async def generate_edu():
    q_edu = MyQueue()
    for i in range(110):
        await q_edu.put("大学（指大专及以上）")
    for i in range(99):
        await q_edu.put("高中（含中专）")
    for i in range(305):
        await q_edu.put("初中")
    for i in range(420):
        await q_edu.put("小学")
    for i in range(66):
        await q_edu.put("无教育经历")
    q_edu.shuffle()
    q_n = queue.Queue(1000)
    while not q_edu.empty():
        item = await q_edu.get()
        q_n.put(item)
    return q_n


# 生成户口性质
def generate_family_type():
    q_type = queue.Queue(1000)
    for i in range(532):
        q_type.put("城镇户口")
    for i in range(468):
        q_type.put("农村户口")
    return q_type


# 生成籍贯
async def generate_native_city():
    q_city = MyQueue()
    for i in range(178):
        await q_city.put("贵州省毕节市")
    for i in range(171):
        await q_city.put("贵州省遵义市")
    for i in range(243):
        await q_city.put("贵州省贵阳市")
    for i in range(97):
        await q_city.put("贵州省黔东南州")
    for i in range(90):
        await q_city.put("贵州省黔南州")
    for i in range(79):
        await q_city.put("贵州省六盘水市")
    for i in range(78):
        await q_city.put("贵州省黔西南州")
    for i in range(64):
        await q_city.put("贵州省安顺市")
    q_city.shuffle()
    q_n = queue.Queue(1000)
    while not q_city.empty():
        item = await q_city.get()
        q_n.put(item)
    return q_n


# 生成结婚
async def generate_marry():
    q_m = MyQueue()
    for i in range(300):
        await q_m.put("已婚")
    for i in range(700):
        await q_m.put("未婚")
    q_m.shuffle()
    q_n = queue.Queue(1000)
    while not q_m.empty():
        item = await q_m.get()
        q_n.put(item)
    return q_n


# 生成职业
async def generate_occupation():
    q_o = MyQueue()
    for i in range(17):
        await q_o.put('国家机关、党群组织、企业、事业单位负责人')
    for i in range(55):
        await q_o.put('专业技术人员')
    for i in range(30):
        await q_o.put('办事人员和有关人员')
    for i in range(90):
        await q_o.put('商业、服务业人员')
    for i in range(650):
        await q_o.put('农、林、牧、渔、水利业生产人员')
    for i in range(155):
        await q_o.put('生产、运输设备操作人员及有关人员')
    for i in range(3):
        await q_o.put('其他')
    q_o.shuffle()
    q_n = queue.Queue(1000)
    while not q_o.empty():
        item = await q_o.get()
        q_n.put(item)
    return q_n


# 是否为退役军人
async def generate_military():
    q_m = MyQueue()
    for i in range(200):
        await q_m.put(1)
    for i in range(800):
        await q_m.put(0)
    q_m.shuffle()
    q_n = queue.Queue(1000)
    while not q_m.empty():
        item = await q_m.get()
        q_n.put(item)
    return q_n


# pg数据库生成随机地址队列
def generate_address():
    q_address = queue.Queue(1000)
    cur = pg_conn.cursor()
    sql = "SELECT address FROM countys WHERE type = 'room' order by random() LIMIT 1000;"
    cur.execute(sql)
    rows = cur.fetchall()
    for i in range(1000):
        q_address.put(rows[i][0])
    pg_conn.commit()
    cur.close()
    return q_address


# 插入数据到数据库相关
# 防止出现本科学历 年龄小于18岁情况
def check_edu_age(q_edu, age):
    education = q_edu.get()
    if (education == '大学（指大专及以上）') & (age > 18):
        return education
    elif (education == '高中（含中专）') & (age > 16):
        return education
    elif (education == '初中') & (age > 13):
        return education
    elif (education == '小学') & (age > 7):
        return education
    else:
        education = '无教育经历'
        return education


# 防止出现180 年龄小于15岁情况
def check_hi_age(sex, age):
    if sex == '男':
        if age > 18:
            height = 169.35 + random.randint(0, 10)
        elif 18 > age > 12:
            height = 159.35 + random.randint(0, 15)
        else:
            height = ''
    else:
        if age > 18:
            height = 159.36 + random.randint(0, 10)
        elif 18 > age > 12:
            height = 149.36 + random.randint(0, 15)
        else:
            height = ''
    return str(height)


# 防止出现性别男 姓名女的情况
def check_sex_name(sex):
    two_or_three = random.randint(2, 3)
    if sex == '男':
        if two_or_three == 2:
            person_name = fake.last_name_male() + fake.first_name_male()
        else:
            person_name = fake.last_name_male() + fake.last_name_male() + fake.first_name_male()
    else:
        if two_or_three == 2:
            person_name = fake.last_name_female() + fake.first_name_female()
        else:
            person_name = fake.last_name_female() + fake.last_name_female() + fake.first_name_female()
    return person_name


# 防止出现退役军人 年龄小于18的情况
def check_age_military(age, q_military):
    military_status = q_military.get()
    if (military_status == 1) & (age > 18):
        return military_status
    else:
        military_status = 0
        return military_status


# 防止出现低于16岁工作情况
def check_age_occupation(age, q_occupation):
    if age > 16:
        occupation = q_occupation.get()
    else:
        occupation = "无职业"
    return occupation


# 防止结婚年龄低于法定结婚年龄
def check_age_marry(age, sex, q_m):
    m = q_m.get()
    if (m == '已婚') & (sex == '女') & (age >= 20):
        return m
    elif (m == '已婚') & (sex == '男') & (age >= 22):
        return m
    else:
        return '未婚'


# 检查主键是否有重复
def check_duplicate_id(person_id, cur):
    while True:
        select_sql = "SELECT person_id FROM dim_psb_residents WHERE person_id='{person_id}';". \
            format(person_id=person_id)
        cur.execute(select_sql)
        if cur.rowcount == 1:
            mid_n = person_id[6:14]
            new_person_id = fake.ssn()
            person_id = new_person_id[0:6] + mid_n + new_person_id[14:18]
        else:
            break
    return person_id


# 插入一条生成的数据
def insertSingle(person_id, nation, sex, person_name, birth, education, family_type, family_id, height, military_status,
                 address, native_place, occupation, marital_status, cur):
    # 先查询主键是否重复
    person_id = check_duplicate_id(person_id, cur)
    # 再进行插入
    sql = "INSERT INTO dim_psb_residents() VALUES('{person_id}','{nation}','{sex}','{person_name}','{birth}'," \
          "'{education}','{family_type}','{family_id}','{height}','{military_status}','{address}','{native_place}'," \
          "'{occupation}','{marital_status}');".format(person_id=person_id, nation=nation, sex=sex,
                                                       person_name=person_name, birth=birth, education=education,
                                                       family_type=family_type, family_id=family_id, height=height,
                                                       military_status=military_status, address=address,
                                                       native_place=native_place, occupation=occupation,
                                                       marital_status=marital_status)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def insertQueueIntoDatabase(q_id, q_nation, q_sex, q_birth, q_edu, q_family_type, q_family_id, q_military, q_address,
                            q_city, q_occupation, q_m):
    cur = mysql_conn.cursor()
    while not q_id.empty():
        person_id = q_id.get()
        nation = q_nation.get()
        sex = q_sex.get()
        person_name = check_sex_name(sex)
        birth = q_birth.get()
        b_s = birth.split('-')
        person_id = '522' + person_id[3:6] + b_s[0] + b_s[1] + b_s[2] + person_id[14:18]
        age = 2021 - int(b_s[0])
        education = check_edu_age(q_edu, age)
        family_type = q_family_type.get()
        family_id = q_family_id.get()
        height = check_hi_age(sex, age)
        military_status = check_age_military(age, q_military)
        address = q_address.get()
        native_place = q_city.get()
        occupation = check_age_occupation(age, q_occupation)
        marital_status = check_age_marry(age, sex, q_m)
        insertSingle(person_id, person_name, nation, sex, birth, education, family_type, family_id, height,
                     military_status, address, native_place, occupation, marital_status, cur)
    cur.close()


# 生成数据主函数
def generate1000():
    q_id = queue.Queue(1000)
    q_nation = asyncio.run(generate_nation())
    q_sex = queue.Queue(1000)
    q_birth = asyncio.run(generate_birth())
    q_edu = asyncio.run(generate_edu())
    q_family_type = generate_family_type()
    q_family_id = queue.Queue(1000)
    q_military = asyncio.run(generate_military())
    q_address = generate_address()
    q_city = asyncio.run(generate_native_city())
    q_occupation = asyncio.run(generate_occupation())
    q_m = asyncio.run(generate_marry())
    for i in range(510):
        q_id.put(fake.ssn())
        q_sex.put('男')
        q_family_id.put(random.randint(1000000, 9999999))
    for i in range(490):
        q_id.put(fake.ssn())
        q_sex.put('女')
        q_family_id.put(random.randint(1000000, 9999999))
    insertQueueIntoDatabase(q_id, q_nation, q_sex, q_birth, q_edu, q_family_type, q_family_id, q_military, q_address,
                            q_city, q_occupation, q_m)


if __name__ == '__main__':
    for x in range(100):
        generate1000()
