import pymysql
from faker import Faker
import random
import re

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
school_list = list(filter(lambda x: x != '\n', open("school.txt", encoding='utf-8', errors='ignore').readlines()))
major_list = list(filter(lambda x: re.match('.*类', x) is None,
                  filter(lambda x: x != '\n', open("major.txt", encoding='utf-8', errors='ignore').readlines()))
                  )
education_list = ['本科', '硕士研究生', '博士研究生']
education_year = {'本科': 4, '硕士研究生': 3, '博士研究生': 5}


def search():
    sql = "SELECT person_id, person_name, education, political_status, nation, person_phone, birth " \
          "FROM dim_hrssb_personal_info " \
          "WHERE education = '大学（指大专及以上）'"
    cur.execute(sql)
    return cur.fetchall()


def insert(person_id, person_name, student_no, graduate_school, study_major, education, admission_time, graduate_time,
           political_status, nation, student_phone):
    sql = "INSERT INTO dim_eb_student() VALUES ('{person_id}', '{person_name}', '{student_no}', '{graduate_school}', " \
          "'{study_major}', '{education}', '{admission_time}', '{graduate_time}', '{political_status}', '{nation}', " \
          "'{student_phone}')"\
        .format(person_id=person_id, person_name=person_name, student_no=student_no, graduate_school=graduate_school,
                study_major=study_major, education=education, admission_time=admission_time, graduate_time=graduate_time,
                political_status=political_status, nation=nation, student_phone=student_phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate():
    student = search()
    for i in student:
        person_id = i[0]
        person_name = i[1]
        student_no = fake.random_number(digits=10)
        graduate_school = random.choice(school_list).replace('\n', '')
        study_major = random.choice(major_list).replace('\n', '')
        education = random.choice(education_list)
        year = int(str(i[6]).split("-")[0]) + random.randint(18, 25)
        admission_time = str(year) + "-09" + "-01"
        graduate_time = str(year + education_year[education]) + "-07" + "-01"
        political_status = i[3]
        nation = i[4]
        student_phone = i[5]
        insert(person_id, person_name, student_no, graduate_school, study_major, education, admission_time, graduate_time,
               political_status, nation, student_phone)


if __name__ == '__main__':
    generate()
    cur.close()
