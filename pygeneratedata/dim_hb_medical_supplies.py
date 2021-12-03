import pymysql
from faker import Faker
import random

fake = Faker('zh_CN')
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')
cur = mysql_conn.cursor()
company_list = ['3M中国有限公司', '上海兴诺康纶纤维科技股份有限公司', '霍尼韦尔(中国）有限公司', '优唯斯(广州)安全防护用品有限公司',
                '兴和通商股份有限公司',
                '稳健医疗用品股份有限公司', '广州阳普医疗科技股份有限公司', '白元日用品制造(深圳)有限公司',
                '利洁时家化(中国)有限公司', '建德市朝美日化有限公司'
                ]
supplies_class_l = ["防护用品", "消杀物品", "药品", "诊断类用品"]
supplies_class_list = {"防护用品": ["N95口罩(个)", "医用外科口罩(个)", "防护服(套)", "医用防护头罩(个)", "护目镜(个)",
                                "防冲击眼罩、防护面罩(双)", "医用橡胶手套(双)", "隔离衣(套)", "一次性医用口罩(个)", "医用帽(个)",
                                "鞋套/靴套(双)"],
                       "消杀物品": ["漂白精粉(kg)", "84消毒液(l)", "二氧化氯消毒液(l)", "医用酒精(l)"],
                       "药品": ["干扰素(mg)", "奥司他韦(mg)", "洛匹那韦利托那韦片(mg)", "阿比多尔(mg)",
                              "金花清感颗粒(mg)", "连花清瘟(mg)", "金叶败毒(mg)", "免疫球蛋白(mg)", "甲泼尼龙(mg)"],
                       "诊断类用品": ["手持红外体温测试仪(台)", "诊断试剂(支)"]
                       }
detail_supplies = {"N95口罩(个)": "符合美国国家职业安全卫生研究所（NIOSH）规定的NIOSH空气过滤等级标准“N95”级别、可阻挡95%直径0.3微米以上的非油性颗粒的口罩",
                   "医用外科口罩(个)": "应用于戴在手术室医务人员口鼻部位，以防止皮屑、呼吸道微生物传播到开放的手术创面，并阻止手术病人的体液向医务人员传播，起到双向生物防护的作用。",
                   "防护服(套)": "应用于消防、军工、船舶、石油、化工、喷漆、清洗消毒、实验室等行业与部门。",
                   "医用防护头罩(个)": "应用于防止来自患者的病原微生物向医务人员传播、隔离和预防感染的一体式医用防护头罩。",
                   "护目镜(个)": "应用于医疗机构中检查治疗时起防护作用，阻隔体液、血液飞溅或泼溅的隔离眼罩。",
                   "防冲击眼罩、防护面罩(双)": "应用于医疗机构中检查治疗时起防护作用，阻隔体液、血液飞溅或泼溅的隔离眼罩、面罩。",
                   "医用橡胶手套(双)": "医学上用以保护手部不受伤害的用品。",
                   "隔离衣(套)": "适用于为医务人员工作时接触具有潜在感染性患者的体液、分泌物、排泄物、使用过的物品等提供阻隔、防护作用的医用防护隔离衣产品。",
                   "一次性医用口罩(个)": "适用于覆盖使用者的口、鼻及下颌，用于普通医疗环境中佩戴、阻隔口腔和鼻腔呼出或喷出污染物的一次性使用口罩。",
                   "医用帽(个)": "适用于医疗系统在临床卫生护理时用的医疗用品，用于医疗机构门诊、病房、检验室等作普通隔离。",
                   "鞋套/靴套(双)": "适用于医务人员使用，也可作卫生防护使用。",
                   "漂白精粉(kg)": "应用于游泳池、工业循环水。饮用水、杀菌卫生防疫、纸浆纱布等的消毒，其用途非常广泛。",
                   "84消毒液(l)": "广泛应用于杀灭细菌和病毒、预防疾病并抑制传播的产品。",
                   "二氧化氯消毒液(l)": "具备杀菌谱广、杀菌能力强、作用速度快、稳定性好、毒性低、腐蚀性 、刺激性小（应该是无毒、无残留、无腐蚀、无刺激）、易溶于水、对人和动物安全及价廉易得、对环境污染程度低等特点。",
                   "医用酒精(l)": "酒精度高，制成品出量高，含酒精以外的醚、醛成分比酒多，主要用于消毒、杀菌。",
                   "干扰素(mg)": "一类糖蛋白，它具有高度的种属特异性，故动物的干扰素对人无效，干扰素具有抗病毒、抑制细胞增殖、调节免疫及抗肿瘤作用。",
                   "奥司他韦(mg)": "一种作用于神经氨酸酶的特异性抑制剂，其抑制神经氨酸酶的作用，可以抑制成熟的流感病毒脱离宿主细胞，从而抑制流感病毒在人体内的传播以起到治疗流行性感冒的作用。",
                   "洛匹那韦利托那韦片(mg)": "适用于与其它抗反转录病毒药物联合用药，治疗人类免疫缺陷病毒-1",
                   "阿比多尔(mg)": "一种抗病毒药物，主要适应症是A类、B类流感病毒引起的流行性感冒。",
                   "金花清感颗粒(mg)": "用于外感时邪引起的发热，恶寒轻或不恶寒，咽红咽痛，鼻塞流涕，口渴，咳嗽或咳而有痰等，舌质红，苔薄黄，脉数。",
                   "连花清瘟(mg)": "连花清瘟颗粒，清瘟解毒，宣肺泄热。用于治疗流行性感冒属热毒袭肺证",
                   "金叶败毒(mg)": "金叶败毒颗粒，清热解毒。用于风温肺热病热",
                   "免疫球蛋白(mg)": "由健康人血浆，经分离纯化，去除抗补体活性并经病毒灭活处理、冻干制成，其中免疫球蛋白不低于蛋白质总量的96%。",
                   "甲泼尼龙(mg)": "一种有机化合物，分子式为C22H30O5，具有较强的抗炎作用",
                   "手持红外体温测试仪(台)": "是将物体发射的红外线具有的辐射能转变成电信号，红外线辐射能的大小与物体本身的温度相对应，根据转变成电信号大小，可以确定物体的温度。",
                   "诊断试剂(支)": "采用免疫学、微生物学、分子生物学等原理或方法制备的、在体外用于对人类疾病的诊断、检测及流行病学调查等的诊断试剂。",
                   }


def search():
    sql = "SELECT unified_social_credit_identifier,enterprise_name,phone,hospital_address FROM dim_hb_hospital_info;"
    cur.execute(sql)
    return cur.fetchall()


def insert(unified_social_credit_identifier,
           hospital_name, phone, address, supplies_class, medical_name, manufacturer, quantity, description):
    sql = "INSERT INTO dim_hb_medical_supplies() VALUES ('{unified_social_credit_identifier}','{hospital_name}','{phone}','{address}'," \
          "'{supplies_class}','{medical_name}', '{manufacturer}', '{quantity}', '{description}')"\
        .format(unified_social_credit_identifier=unified_social_credit_identifier, hospital_name=hospital_name,
                phone=phone, address=address, supplies_class=supplies_class, medical_name=medical_name,
                manufacturer=manufacturer, quantity=quantity, description=description)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


def generate():
    hospital_list = search()
    for i in range(0, 1000):
        hospital = hospital_list[random.randint(0, 19)]
        usc_ud = hospital[0]
        hospital_name = hospital[1]
        phone = hospital[2]
        address = hospital[3]
        supplies_class = random.choice(supplies_class_l)
        medical_name = random.choice(supplies_class_list[supplies_class])
        manufacturer = random.choice(company_list)
        quantity = random.randint(1000, 10000)
        description = detail_supplies[medical_name]
        #
        insert(usc_ud, hospital_name, phone, address, supplies_class, medical_name, manufacturer, quantity, description)


if __name__ == '__main__':
    generate()
    cur.close()
