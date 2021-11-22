import pymysql
from faker import Faker
import random

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
team_list = ['抢险抢修专业队', '医疗救护专业队', '消防专业队', '治安专业队', '防化防疫专业队', '通信专业队', '运输专业队']
team_map = {'抢险抢修专业队': '主要负责抢建、抢修人防工程、电力、道路、桥梁、供水、供气、广播电视及其他重要设施，抢救人员和重要物资，清除爆炸物。',
            '医疗救护专业队': '主要负责抢运抢救伤病员，指导群众进行自救互救。',
            '消防专业队': '主要负责重要目标、设施的防火、灭火，指导群众扑灭火灾，配合防化专业队进行洗消任务。',
            '治安专业队': '主要负责治安、警戒、保卫、交通管制，监督灯火管制，协助指挥人员、车辆就地疏散隐蔽。',
            '防化防疫专业队': '主要负责人民防空指挥所、重点人员掩蔽工程的防化保障，实施防化观测、侦察、监测和化验，对受沾染人员、设备、物资及重要道路进行洗消，组织防疫灭菌，指导群众防护、洗消和进行“三防”（防核、防化、防生物武器）知识教育。',
            '通信专业队': '主要负责城市防空袭斗争指挥提供通信保障，抢修通信设施设备。',
            '运输专业队': '主要负责城市防空袭斗争中人员和物资的运输。'}
equipment_list = ['化学防护服', '气密性重型防护服', '工业有毒有害气体检测仪', '侦毒器', '军用辐射仪', '放射性检测仪', '救援抛绳器', '生命探测仪',
                  '锯木机', '锯路机', '金属救援撑杆', '坑道排烟机', '手动破拆工具', '剪扩钳']
district_list = ['贵阳市南明区', '贵阳市云岩区', '贵阳市花溪区', '贵阳市乌当区', '贵阳市白云区', '贵阳市观山湖区', '贵阳市息烽县',
                '贵阳市清镇市', '贵阳市修文县', '贵阳市开阳县']


def InsertTeam(team_name, create_time, main_mission, self_equipment, team_member_num, response_person, response_person_phone,
               address):
    sql = "INSERT INTO dim_cad_perfessional_team() VALUES ('{team_name}', '{create_time}', '{main_mission}', '{self_equipment}', " \
          "'{team_member_num}', '{response_person}', '{response_person_phone}', '{address}');" \
        .format(team_name=team_name, create_time=create_time, main_mission=main_mission, team_member_num=team_member_num,
                self_equipment=self_equipment, response_person=response_person, response_person_phone=response_person_phone,
                address=address)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def setEquipment(team_member_num):
    result = ""
    random.shuffle(equipment_list)
    result += equipment_list[0] + " " + str(random.randint(5, 10))
    if team_member_num <= 50:
        for i in range(1, 5):
            result += "," + equipment_list[i] + " " + str(random.randint(5, 10))
        return result
    elif 50 < team_member_num <= 150:
        for i in range(1, 9):
            result += "," + equipment_list[i] + " " + str(random.randint(5, 20))
        return result
    else:
        for i in range(1, 14):
            result += "," + equipment_list[i] + " " + str(random.randint(5, 30))
        return result


def GenerateTeam():
    for i in range(100):
        team_name = random.choice(team_list)
        create_time = str(random.randint(2000, 2021)) + fake.date()[4:]
        main_mission = team_map[team_name]
        team_member_num = int(random.randint(12, 500) * 0.7)
        self_equipment = setEquipment(team_member_num)
        response_person = fake.name()
        response_person_phone = fake.phone_number()
        address = random.choice(district_list)
        InsertTeam(team_name, create_time, main_mission, self_equipment, team_member_num, response_person, response_person_phone,
                   address, )


if __name__ == '__main__':
    GenerateTeam()
    mysql_conn.close()
