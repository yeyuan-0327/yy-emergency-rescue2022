from faker import Faker
import psycopg2
import pymysql
import urllib
import json
import requests
from fact_human_resource import PopExist, FetchGeoFromGaoDe

fake = Faker('zh_CN')
# 连接GreenPlum数据库
gp_conn = psycopg2.connect(database='postgis', user='gpadmin', password='gpadmin', host='192.168.101.105',
                           port='15432')
gp_cur = gp_conn.cursor()
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
mysql_cur = mysql_conn.cursor()


def SearchEnterpriseResource():
    enterprise_map = {}
    table_list = ['dim_msb_enterprise', 'dim_hb_hospital', 'dim_mta_transport_enterprise', 'dim_heavy_equipment_enterprise']
    for table in table_list:
        sql = "SELECT unified_social_credit_identifier FROM {table_name};".format(table_name=table)
        mysql_cur.execute(sql)
        for i in mysql_cur.fetchall():
            enterprise_map[i[0]] = table
    return enterprise_map


def FetchOneSelectEid(select, table, eid):
    try:
        sql = "SELECT {select} FROM {table} WHERE unified_social_credit_identifier = '{eid}';" \
            .format(select=select, table=table, eid=eid)
        print(sql)
        mysql_cur.execute(sql)
        return mysql_cur.fetchone()[0]
    except Exception as e:
        print(e)
        return "None"


def SetExistType(table):
    if table == 'dim_msb_enterprise':
        return 0
    elif table == 'dim_hb_hospital':
        return 1
    elif table == 'dim_mta_transport_enterprise':
        return 2
    elif table == 'dim_heavy_equipment_enterprise':
        return 3


def FetchDistrict(address):
    try:
        addr = urllib.parse.quote(address)
        key = "fffd055b5ec8552655adf5797cda205f"
        url = "http://restapi.amap.com/v3/geocode/geo?key="
        new_url = url + key + "&address=" + addr
        res = requests.get(new_url)
        json_data = json.loads(res.text)
        district = str(json_data['geocodes'][0]['district'])
        return district
    except Exception as e:
        print(e)
        return ""


def SetScope(table, i):
    if table == "dim_hb_hospital":
        return "医院"
    elif table == "dim_heavy_equipment_enterprise":
        return "工业、交通、邮政、交通运输、交通运输管理部门和机构"
    else:
        return FetchOneSelectEid("business_scope", table, i)


def InsertEnterpriseFact(unified_social_credit_identifier, enterprise_name, business_scope, is_exist, legal_person,
                         legal_person_id, phone, address, address_geom, district):
    sql = "INSERT INTO fact_enterprise_resource(unified_social_credit_identifier, enterprise_name, business_scope, is_exist," \
          "legal_person, legal_person_id, phone, address, address_geom, district) " \
          "VALUES('{unified_social_credit_identifier}', '{enterprise_name}', '{business_scope}', '{is_exist}', " \
          "'{legal_person}', '{legal_person_id}', '{phone}', '{address}', '{address_geom}', '{district}')"\
        .format(unified_social_credit_identifier=unified_social_credit_identifier, enterprise_name=enterprise_name, business_scope=business_scope,
                is_exist=is_exist, legal_person=legal_person, legal_person_id=legal_person_id, phone=phone, address=address,
                address_geom=address_geom, district=district)
    print(sql)
    gp_cur.execute(sql)
    gp_conn.commit()


def GenerateEnterpriseFact():
    enterprise_map = SearchEnterpriseResource()
    PopExist(enterprise_map, "unified_social_credit_identifier", "fact_enterprise_resource")
    for i in enterprise_map:
        unified_social_credit_identifier = i
        enterprise_name = FetchOneSelectEid("enterprise_name", enterprise_map[i], i)
        business_scope = SetScope(enterprise_map[i], i)
        is_exist = SetExistType(enterprise_map[i])
        legal_person = FetchOneSelectEid("legal_person", enterprise_map[i], i)
        legal_person_id = FetchOneSelectEid("legal_person_id", enterprise_map[i], i)
        phone = FetchOneSelectEid("phone", enterprise_map[i], i)
        address = FetchOneSelectEid("address", enterprise_map[i], i)
        address_geom = FetchGeoFromGaoDe(address)
        district = FetchDistrict(address)
        InsertEnterpriseFact(unified_social_credit_identifier, enterprise_name, business_scope, is_exist,
                             legal_person, legal_person_id, phone, address, address_geom, district)


if __name__ == '__main__':
    GenerateEnterpriseFact()
    mysql_conn.close()
    gp_conn.close()
