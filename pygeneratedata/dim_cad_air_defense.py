import pymysql
from faker import Faker
import random

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
defense_list = ['贵阳市朝阳路', '贵阳市六盘水路', '贵阳市三桥北路', '贵阳市黄岭路', '贵阳市学士路',
                '贵阳市贵铝职业教育学院内', '贵阳市扶风住宅小区北门', '贵阳市福楼旺邸东南门', '贵阳市交警支队二大队',
                '贵阳市黔灵山公园外空置人防掩蔽工程']
use_list = ['指挥工程：保障人防指挥机关战时工作的人防工程(包括防空地下室)。', '医疗救护工程：战时对伤员独立进行早期救治工作的人防工程(包括防空地下室)。按照医疗分级和任务的不同，医疗救护工程可分为中心医院、急救医院和救护站等。',
            '防空专业队工程：保障防空专业队掩蔽和执行某些勤务的人防工程(包括防空地下室)，一般称防空专业队掩蔽所。一个完整的防空专业队掩蔽所一般包括专业队队员掩蔽部和专业队装备(车辆)掩蔽部两个部分。但在目前的人防工程建设中，也可以将两个部分分开单独修建。'
            '人员掩蔽工程：主要用于保障人员掩蔽的人防工程(包括防空地下室)。按照战时掩蔽人员的作用，人员掩蔽工程共分为两等：一等人员掩蔽所，指供战时坚持工作的政府机关、城市生活重要保障部门(电信、供电、供气、供水、食品等)、重要厂矿企业和其它战时有人员进出要求的人员掩蔽工程；二等人员掩蔽所，指战时留城的普通居民掩蔽所。',
            '配套工程：系指战时的保障性人防工程(即指挥工程、医疗救护工程、防空专业队工程和人员掩蔽工程以外的人防工程总合)，主要包括区域电站、区域供水站、人防物资库、人防汽车库、食品站、生产车间、人防交通于(支)道、警报站、核生化监测中心等工程。']


def InsertDefense(air_defense_name, usual_use, war_use, address, protect_level, indoor, outdoor, usage_area, response_person, response_person_phone):
    sql = "INSERT INTO dim_cad_air_defense() VALUE ('{air_defense_name}', '{usual_use}', '{war_use}', '{address}', " \
          "'{protect_level}', '{indoor}', '{outdoor}', '{usage_area}', '{response_person}', '{response_person_phone}')"\
        .format(air_defense_name=air_defense_name, usual_use=usual_use, war_use=war_use, address=address, protect_level=protect_level,
                indoor=indoor, outdoor=outdoor, usage_area=usage_area, response_person=response_person, response_person_phone=response_person_phone)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def GenerateDefense():
    for i in defense_list:
        air_defense_name = i
        usual_use = "参观旅游，达到提升防控意识、自救互救，最大限度减轻灾害伤害的目的。"
        war_use = random.choice(use_list)
        address = i
        protect_level = random.randint(1, 6)
        indoor = random.randint(2, 10)
        outdoor = random.randint(2, 5)
        usage_area = str(random.randint(50, 150))+"0 ㎡"
        response_person = fake.name()
        response_person_phone = fake.phone_number()
        InsertDefense(air_defense_name, usual_use, war_use, address, protect_level, indoor, outdoor, usage_area,
                      response_person, response_person_phone)


if __name__ == '__main__':
    GenerateDefense()
    mysql_conn.close()
