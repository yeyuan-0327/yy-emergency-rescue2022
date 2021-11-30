from faker import Faker
import psycopg2
import pymysql

fake = Faker('zh_CN')
# 连接GreenPlum数据库
gp_conn = psycopg2.connect(database='postgis', user='gpadmin', password='gpadmin', host='192.168.101.105',
                           port='15432')
gp_cur = gp_conn.cursor()
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
mysql_cur = mysql_conn.cursor()


def SearchSpareResource():
    spare_map = {}
    table_list = []
    for i in table_list:
        sql = "SELECT  FROM ;"
        mysql_cur.execute(sql)
        for j in mysql_cur.fetchall():
            spare_map[j[0]] = i
    return spare_map


def InsertSpareResources(spare_resources_name, address, address_geom, spare_resources_type, contact_person, contact_person_phone):
    sql = ""
    print(sql)
    gp_cur.execute(sql)
    gp_conn.commit()


def GenerateSpare():
    spare_map = SearchSpareResource()
    for i in spare_map:
        spare_resources_name = ""
        address = ""
        address_geom = ""
        spare_resources_type = ""
        contact_person = ""
        contact_person_phone = ""
        InsertSpareResources(spare_resources_name, address, address_geom, spare_resources_type, contact_person, contact_person_phone)


if __name__ == '__main__':
    GenerateSpare()
    mysql_conn.close()
    gp_conn.close()
