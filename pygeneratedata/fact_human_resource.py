# 事实表
from faker import Faker
import psycopg2
import pymysql
import urllib
import json
import requests

fake = Faker('zh_CN')
# 连接GreenPlum数据库
gp_conn = psycopg2.connect(database='postgis', user='gpadmin', password='gpadmin', host='192.168.101.105',
                           port='15432')
gp_cur = gp_conn.cursor()
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
mysql_cur = mysql_conn.cursor()


def SearchHuman():
    human_map = {}
    human_list = ["dim_psb_residents", "dim_hb_medical_staff", "dim_mta_vehicle_driver"]
    for table in human_list:
        sql = "SELECT person_id FROM {table_name};".format(table_name=table)
        mysql_cur.execute(sql)
        for i in mysql_cur.fetchall():
            human_map[i[0]] = table
    return human_map


def FetchGeoFromGaoDe(address):
    try:
        addr = urllib.parse.quote(address)
        key = "fffd055b5ec8552655adf5797cda205f"
        url = "http://restapi.amap.com/v3/geocode/geo?key="
        new_url = url + key + "&address=" + addr
        res = requests.get(new_url)
        json_data = json.loads(res.text)
        x = str(json_data['geocodes'][0]['location']).split(',')[0]
        y = str(json_data['geocodes'][0]['location']).split(',')[1]
        wkb_geometry = "POINT(" + x + " " + y + ")"
        return wkb_geometry
    except Exception as e:
        print(e)
        return "POINT(0 0)"


def FetchOneSelectPid(select, table, pid):
    try:
        sql = "SELECT {select} FROM {table} WHERE person_id = '{pid}';".format(select=select, table=table, pid=pid)
        print(sql)
        mysql_cur.execute(sql)
        return mysql_cur.fetchone()[0]
    except Exception as e:
        print(e)
        return "None"


def InsertFactHuman(person_id, person_name, native_place, nation, height, education, birth, sex, address, address_geom,
                    person_phone, political_status, military_status, marital_status, is_disable, is_college, is_student_enlisted,
                    is_militia, is_retire_soldier, is_medical_person, is_mobilize_political_person, is_bound_vehicle):
    sql = "INSERT INTO fact_human_resource(person_id, person_name, native_place, nation, height, education, birth, sex, address," \
          "address_geom, person_phone, political_status, military_status, marital_status, is_disable, is_college, is_student_enlisted," \
          "is_militia, is_retire_soldier, is_medical_person, is_mobilize_political_person, is_bound_vehicle) VALUES ('{person_id}', '{person_name}', '{native_place}', '{nation}', '{height}', '{education}', '{birth}', '{sex}', " \
          "'{address}', ST_GeomFromText('{address_geom}',4326), '{person_phone}', '{political_status}', '{military_status}', '{marital_status}', '{is_disable}', " \
          "'{is_college}', '{is_student_enlisted}', '{is_militia}', '{is_retire_soldier}', '{is_medical_person}', '{is_mobilize_political_person}', " \
          "'{is_bound_vehicle}')".format(person_id=person_id, person_name=person_name, native_place=native_place, nation=nation,
                                         height=height, education=education, birth=birth, sex=sex, address=address, address_geom=address_geom,
                                         person_phone=person_phone, political_status=political_status, military_status=military_status, marital_status=marital_status,
                                         is_disable=is_disable, is_college=is_college, is_student_enlisted=is_student_enlisted, is_militia=is_militia,
                                         is_retire_soldier=is_retire_soldier, is_medical_person=is_medical_person, is_mobilize_political_person=is_mobilize_political_person,
                                         is_bound_vehicle=is_bound_vehicle)
    print(sql)
    gp_cur.execute(sql)
    gp_conn.commit()


def ConvertPID(person_id):
    birth = person_id[6:14]
    return birth[0:4]+"-"+birth[4:6]+"-"+birth[6:]


def ConvertDim(param):
    param = "dim_hrssb_personal" if param == "dim_psb_residents" else param
    return param


def SetMedicalStaff(param):
    if param == "None":
        return 0
    elif param == "医师":
        return 1
    else:
        return 2


def SearchExistHuman(exist_id, fact_table):
    sql = "SELECT {exist_id} FROM {table_name};".format(exist_id=exist_id, table_name=fact_table)
    gp_cur.execute(sql)
    return gp_cur.fetchall()


def PopExist(pop_map, exist_id, fact_table):
    exist_human = SearchExistHuman(exist_id, fact_table)
    for i in exist_human:
        pop_map.pop(i[0])


def GenerateFactHuman():
    human_map = SearchHuman()
    PopExist(human_map, "person_id", "fact_human_resource")
    for i in human_map:
        person_id = i
        person_name = FetchOneSelectPid("person_name", human_map[i], person_id)
        native_place = FetchOneSelectPid("native_place", human_map[i], person_id)
        nation = FetchOneSelectPid("nation", human_map[i], person_id)
        height = FetchOneSelectPid("height", human_map[i], person_id)
        education = FetchOneSelectPid("education", human_map[i], person_id)
        birth = ConvertPID(person_id)  # 从PID转换
        sex = FetchOneSelectPid("sex", human_map[i], person_id)  # 医务单独 运输车单独
        address = FetchOneSelectPid("address", ConvertDim(human_map[i]), person_id)  # 如果为dim_psb_residents 则变为dim_hrssb_personal
        address_geom = "POINT(0 0)" if address == "None" else FetchGeoFromGaoDe(address)  # 从高德api获取到地址经纬度
        person_phone = FetchOneSelectPid("person_phone", ConvertDim(human_map[i]), person_id)  # 如果为dim_psb_residents 则变为dim_hrssb_personal
        political_status = FetchOneSelectPid("political_status", ConvertDim(human_map[i]), person_id)  # 如果为dim_psb_residents 则变为dim_hrssb_personal
        military_status = False if FetchOneSelectPid("military_status", human_map[i], person_id) == 0 else True
        marital_status = FetchOneSelectPid("marital_status", human_map[i], person_id)  # 空 未婚 已婚
        is_disable = False if FetchOneSelectPid("disable_code", "dim_df_disable", person_id) == "None" else True
        is_college = False if FetchOneSelectPid("student_no", "dim_eb_student", person_id) == "None" else True
        is_student_enlisted = False if FetchOneSelectPid("student_is_enlisted", "dim_afd_regist", person_id) == "None" else True
        is_militia = False if FetchOneSelectPid("military_class", "dim_afd_militia", person_id) == "None" else True
        is_retire_soldier = False if FetchOneSelectPid("retire_no", "dim_ova_veteran", person_id) == "None" else True
        is_medical_person = SetMedicalStaff(FetchOneSelectPid("medical_type", "dim_hb_medical_staff", person_id))
        is_mobilize_political_person = False if FetchOneSelectPid("certified", "dim_mobilize_political_genies", person_id) == "None" else True
        is_bound_vehicle = False if FetchOneSelectPid("bound_vehicle", "dim_mta_vehicle_driver", person_id) == "None" else True  # 是
        InsertFactHuman(person_id, person_name, native_place, nation, height, education, birth, sex,
                        address, address_geom, person_phone, political_status, military_status, marital_status, is_disable,
                        is_college, is_student_enlisted, is_militia, is_retire_soldier, is_medical_person, is_mobilize_political_person,
                        is_bound_vehicle)


if __name__ == '__main__':
    GenerateFactHuman()
    mysql_conn.close()
    gp_conn.close()
