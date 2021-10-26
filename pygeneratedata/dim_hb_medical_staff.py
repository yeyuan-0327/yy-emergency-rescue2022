import pymysql
from faker import Faker
import random
from dim_psb_residents import check_sex_name

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
medical_type_list = ['临床执业医师', '口腔执业医师', '公共卫生执业医师', '中西医结合执业医师', ]
medical_small_type_list = ['临床执业助理医师', '口腔执业助理医师', '公共卫生执业助理医师', '乡村全科执业助理医师', '中西医结合执业助理医师']
department = ['内科', '外科', '妇产科', '男科', '儿科', '五官科', '肿瘤科', '中医科', '麻醉科']
hospital_list = ['贵州省人民医院',
                 '贵阳市妇幼保健院',
                 '贵州中建医院',
                 '贵州中医药大学第二附属医院',
                 '贵阳市第二人民医院',
                 '贵阳市第一人民医院',
                 '贵州中医药大学第一附属医院',
                 '贵州医科大学附属医院',
                 '贵州省第二人民医院',
                 '贵阳市第三人民医院',
                 '贵州省骨科医院',
                 '贵阳市第四人民医院',
                 '贵阳市第五人民医院',
                 '贵阳市第六人民医院',
                 '贵阳市口腔医院',
                 '贵阳市口腔医院',
                 '贵阳市花溪区人民医院',
                 '贵阳市肺科医院',
                 '贵阳市云岩区人民医院',
                 '贵阳市南明区人民医院',
                 '贵阳市白云区人民医院',
                 '贵阳市乌当区人民医院']


def insert_medical_staff(person_id, person_name, sex, profess_name, certificate_no, medical_type,
                         medical_department, profess_class, affiliated_hospital):
    sql = "INSERT INTO dim_hb_medical_staff() VALUES ('{person_id}', '{person_name}', '{sex}', '{profess_name}'" \
          ",'{certificate_no}'," \
          "'{medical_type}', '{medical_department}', '{profess_class}', '{affiliated_hospital}')" \
        .format(person_id=person_id, person_name=person_name, sex=sex, profess_name=profess_name,
                certificate_no=certificate_no, medical_type=medical_type, medical_department=medical_department,
                profess_class=profess_class, affiliated_hospital=affiliated_hospital)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_medical_staff():
    for i in range(6430):
        person_id = fake.ssn()
        year = str(2021 - random.randint(23, 70))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        person_id = '522' + person_id[3:6] + year + month + day + person_id[14:18]
        sex = '男' if random.randint(0, 1) == 1 else '女'
        person_name = check_sex_name(sex)
        age = 2021 - int(year)
        profess_name = random.choice(medical_type_list) if age > 30 else random.choice(medical_small_type_list)
        certificate_no = '11' + fake.numerify() + fake.numerify() + fake.numerify() + fake.numerify()
        medical_type = '医师'
        medical_department = random.choice(department)
        profess_class = '初级职业医师'
        if 25 >= age > 23:
            profess_class = '初级职业医师'
        elif 30 >= age > 25:
            profess_class = '规培住院医师'
        elif 40 >= age > 30:
            profess_class = '中级职称主治医师'
        elif 50 >= age > 40:
            profess_class = '副高级职称主任医师'
        elif age > 50:
            profess_class = '正高级职主任治医师'
        affiliated_hospital = random.choice(hospital_list)
        insert_medical_staff(person_id, person_name, sex, profess_name, certificate_no, medical_type,
                             medical_department, profess_class, affiliated_hospital)


def generate_medical_nurse_staff():
    for i in range(7610):
        person_id = fake.ssn()
        year = str(2021 - random.randint(20, 60))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        person_id = '522' + person_id[3:6] + year + month + day + person_id[14:18]
        sex = '男' if random.randint(0, 9) == 0 else '女'
        person_name = check_sex_name(sex)
        age = 2021 - int(year)
        profess_name = '执业护士'
        certificate_no = '11' + fake.numerify() + fake.numerify() + fake.numerify() + fake.numerify()
        medical_type = '护士'
        medical_department = random.choice(department)
        profess_class = '护士'
        if 30 >= age > 25:
            profess_class = '初级护士'
        elif 40 >= age > 30:
            profess_class = '主管护士'
        elif 50 >= age > 40:
            profess_class = '副主任护士'
        elif age > 50:
            profess_class = '主任护士'
        affiliated_hospital = random.choice(hospital_list)
        insert_medical_staff(person_id, person_name, sex, profess_name, certificate_no, medical_type,
                             medical_department, profess_class, affiliated_hospital)


if __name__ == '__main__':
    # 生成医师
    generate_medical_staff()
    # 生成护士
    generate_medical_nurse_staff()
    cur.close()
