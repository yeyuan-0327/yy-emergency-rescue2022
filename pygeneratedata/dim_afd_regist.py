import pymysql
from faker import Faker
import random
fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()


def search_student():
    sql = "SELECT * FROM dim_eb_student WHERE admission_time > DATE_SUB(CURDATE(),INTERVAL 18 YEAR);"
    cur.execute(sql)
    return cur.fetchall()


def insert_register(person_id, person_name, student_is_enlisted, student_no, graduate_school, study_major, education,
                    admission_time, graduate_time, register_time, political_status, nation, student_phone):
    sql = "INSERT INTO dim_afd_regist() VALUES ('{person_id}', '{person_name}', '{student_is_enlisted}', '{student_no}'," \
          "'{graduate_school}', " \
          "'{study_major}', '{education}', '{admission_time}', '{graduate_time}', '{register_time}', '{political_status}', '{nation}'," \
          " '{student_phone}')"\
        .format(person_id=person_id, person_name=person_name, student_is_enlisted=student_is_enlisted, student_no=student_no,
                graduate_school=graduate_school,
                study_major=study_major, education=education, admission_time=admission_time, graduate_time=graduate_time,
                register_time=register_time, political_status=political_status, nation=nation, student_phone=student_phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate_register():
    student_list = search_student()
    for i in student_list:
        person_id = i[0]
        person_name = i[1]
        student_is_enlisted = '是' if random.randint(0, 4) == 0 else '否'
        student_no = i[2]
        graduate_school = i[3]
        study_major = i[4]
        education = i[5]
        admission_time = i[6]
        graduate_time = i[7]
        register_time = str(int(str(i[6]).split('-')[0]) + random.randint(1, 3)) + "-0" + str(random.randint(1, 8)) + "-01"
        political_status = i[8]
        nation = i[9]
        student_phone = i[10]
        insert_register(person_id, person_name, student_is_enlisted, student_no, graduate_school, study_major, education,
                        admission_time, graduate_time, register_time, political_status, nation, student_phone)


if __name__ == '__main__':
    generate_register()
    cur.close()
