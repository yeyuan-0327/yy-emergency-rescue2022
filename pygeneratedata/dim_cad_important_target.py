import pymysql
from faker import Faker
import random

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()


def InsertTarget(affiliated_enterprise, unified_social_credit_identifier, target_name, address, brief_content,
                 manage_enterprise, manage_person, manage_person_phone):
    sql = "INSERT INTO dim_cad_important_target() VALUES('{affiliated_enterprise}', '{unified_social_credit_identifier}', " \
          "'{target_name}', '{address}', '{brief_content}', '{manage_enterprise}', '{manage_person}', '{manage_person_phone}');"\
        .format(affiliated_enterprise=affiliated_enterprise, unified_social_credit_identifier=unified_social_credit_identifier,
                target_name=target_name, address=address, brief_content=brief_content, manage_enterprise=manage_enterprise,manage_person=manage_person,
                manage_person_phone=manage_person_phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def tempFunction(result_map, sql):
    cur.execute(sql)
    for i in cur.fetchall():
        l_info = list()
        for j in range(1, len(i)):
            l_info.append(i[j])
        result_map[i[0]] = l_info
    return result_map


def SearchEnterprise():
    result_map = {}
    sql = "SELECT enterprise_name,unified_social_credit_identifier, transport_enterprise_address FROM dim_mta_transport_enterprise ORDER BY RAND() LIMIT 30"
    tempFunction(result_map, sql)
    sql = "SELECT enterprise_name,unified_social_credit_identifier, address FROM dim_msb_enterprise ORDER BY RAND() LIMIT 70"
    tempFunction(result_map, sql)
    return result_map


def GenerateTarget():
    enterprise_list = SearchEnterprise()
    for i in enterprise_list:
        affiliated_enterprise = i
        unified_social_credit_identifier = enterprise_list[i][0]
        target_name = enterprise_list[i][1][:int(len(enterprise_list[i][1])/2)] + "中心"
        address = enterprise_list[i][1]
        brief_content = fake.text()
        manage_enterprise = fake.company_prefix()
        manage_person = fake.name()
        manage_person_phone = fake.phone_number()
        InsertTarget(affiliated_enterprise, unified_social_credit_identifier, target_name, address, brief_content,
                     manage_enterprise, manage_person, manage_person_phone)


if __name__ == '__main__':
    GenerateTarget()
    mysql_conn.close()
