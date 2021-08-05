from faker import Faker
import queue
import asyncio
from random import shuffle
import random
import urllib
import json
import requests
import psycopg2

fake = Faker('zh_CN')


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
def generate_birth():
    q_data = queue.Queue()
    for i in range(240):
        year = str(2021-random.randint(0, 14))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        if int(month) < 10:
            month = "0" + month
        if int(day) < 10:
            day = "0" + day
        birth = year + "-" + month + "-" + day
        q_data.put(birth)
    for i in range(607):
        year = str(2021-random.randint(15, 59))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        if int(month) < 10:
            month = "0" + month
        if int(day) < 10:
            day = "0" + day
        birth = year + "-" + month + "-" + day
        q_data.put(birth)
    for i in range(153):
        year = str(2021-random.randint(60, 100))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        if int(month) < 10:
            month = "0" + month
        if int(day) < 10:
            day = "0" + day
        birth = year + "-" + month + "-" + day
        q_data.put(birth)
    return q_data


# 生成教育
def generate_edu():
    q_edu = queue.Queue()
    for i in range(110):
        q_edu.put("大学（指大专及以上）")
    for i in range(99):
        q_edu.put("高中（含中专）")
    for i in range(305):
        q_edu.put("初中")
    for i in range(320):
        q_edu.put("小学")
    return q_edu


# 生成户口性质
def generate_family_type():
    q_type = queue.Queue()
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
    q_n = queue.Queue()
    while not q_city.empty():
        item = await q_city.get()
        q_n.put(item)
    return q_n


# 生成数据主函数
def generate1000():
    q_id = queue.Queue(1000)
    q_sex = queue.Queue(1000)
    q_name = queue.Queue(1000)
    q_family_id = queue.Queue(1000)
    for i in range(510):
        q_id.put(fake.ssn())
        q_name.put(fake.name_male())
        q_sex.put('男')
        q_family_id.put(random.randint(1000000, 9999999))
    for i in range(490):
        q_id.put(fake.ssn())
        q_name.put(fake.name_female())
        q_sex.put('女')
        q_family_id.put(random.randint(1000000, 9999999))
    q_nation = asyncio.run(generate_nation())
    q_birth = generate_birth()

    print(q_birth.maxsize)
    print(q_nation.maxsize)
    print(q_sex.maxsize)


if __name__ == '__main__':
    conn = psycopg2.connect(database='postgis', user='gpadmin', password='gpadmin', host='192.168.100.30',
                            port='5432')
    generate1000()
    print(fake.name())



