from faker import Faker
import psycopg2
import pymysql

from fact_human_resource import FetchGeoFromGaoDe, PopExist

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
    table_list = ["dim_cad_important_target", "dim_cad_perfessional_team", "dim_cad_air_defense", "dim_cad_evacuation_conceal"]
    for table in table_list:
        sql = "SELECT name FROM {table_name};".format(table_name=table)
        mysql_cur.execute(sql)
        for i in mysql_cur.fetchall():
            spare_map[i[0]] = table
    return spare_map


def InsertSpareResources(spare_resources_name, address, address_geom, spare_resources_type, response_person, response_phone):
    sql = "INSERT INTO fact_spare_resources(spare_resources_name, address, address_geom, spare_resources_type, " \
          "response_person, response_phone) VALUES('{spare_resources_name}', '{address}', '{address_geom}', " \
          "'{spare_resources_type}', '{response_person}', '{response_phone}')"\
        .format(spare_resources_name=spare_resources_name, address=address, address_geom=address_geom, spare_resources_type=spare_resources_type,
                response_person=response_person, response_phone=response_phone)
    print(sql)
    gp_cur.execute(sql)
    gp_conn.commit()


def FetchOneSelectName(select, table, name):
    try:
        sql = "SELECT {select} FROM {table} WHERE name = '{name}';" \
            .format(select=select, table=table, name=name)
        print(sql)
        mysql_cur.execute(sql)
        return mysql_cur.fetchone()[0]
    except Exception as e:
        print(e)
        return "None"


def SetResourceType(table):
    if table == "dim_cad_important_target":
        return 1
    elif table == "dim_cad_perfessional_team":
        return 2
    elif table == "dim_cad_air_defense":
        return 3
    elif table == "dim_cad_evacuation_conceal":
        return 4


def GenerateSpare():
    spare_map = SearchSpareResource()
    PopExist(spare_map, "spare_resources_name", "fact_spare_resources")
    for i in spare_map:
        spare_resources_name = i
        address = FetchOneSelectName("district", spare_map[i], i) if spare_map[i] == "dim_cad_evacuation_conceal" else FetchOneSelectName("address", spare_map[i], i)
        address_geom = FetchGeoFromGaoDe(address)
        spare_resources_type = SetResourceType(spare_map[i])
        response_person = FetchOneSelectName("response_person", spare_map[i], i)
        response_phone = FetchOneSelectName("response_phone", spare_map[i], i)
        InsertSpareResources(spare_resources_name, address, address_geom, spare_resources_type, response_person, response_phone)


if __name__ == '__main__':
    GenerateSpare()
    mysql_conn.close()
    gp_conn.close()
