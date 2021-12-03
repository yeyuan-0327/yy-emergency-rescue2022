# -*- coding:utf-8 -*-
from faker import Faker
import random
import pymysql

fake = Faker('zh_CN')

# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')

enterprise_class_list = ['农、林、牧、渔业', '采矿业', '制造业', '电力、热力、燃气及水生产和供应业', '建筑业', '批发和零售业',
                         '交通运输、仓库和邮政业', '住宿和餐饮业', '信息运输、软件和信息技术服务业', '金融业', '房地产业',
                         '租赁和商务服务业', '科学研究和技术服务业', '水利、环境和公共管理业', '居民服务、修理和其他服务业',
                         '教育', '卫生和社会工作', '文化、体育和娱乐业', '公共管理、社会保障和社会组织']

scope_list = ['文化艺术交流与策划，市场营销策划，企业营销策划，企业形象策划，市场信息咨询与调查（不得从事社会调查、社会调研、民意调查、民意测验），商务咨询，企业管理咨询，会务服务，翻译服务，展览展示服务，设计、制作、发布各类广告，计算机网络工程，服装服饰、工艺礼品、日用百货、文化办公用品、办公设备的销售，从事教育软件科技、计算机网络科技领域内的技术服务、技术开发、技术咨询、技术转让',
              '资产收购、转让、经营、管理、开发；投资咨询；物业管理；房地产经纪；房地产开发、经营。', '道路货物运输，货物运输代理，仓储（除危险化学品），汽车租赁（不得从事金融租赁），物流信息咨询。',
              '教育管理、咨询、培训、服务，从事计算机网络科技（不得从事科技中介）领域内的技术开发、技术咨询，会务服务，文教用品，办公用品销售。', '投资咨询（除金融、证券），企业管理咨询，商务咨询。',
              '一般项目：餐饮企业管理，会务服务，企业管理咨询，商务咨询，食用农产品、厨房设备及用品、一般劳防用品、电脑及耗材、服装鞋帽、办公用品的销售，餐饮服务（限分支机构经营）。',
              '知识产权代理，商标代理，商务信息咨询，企业形象策划，计算机系统服务，市场营销策划，展示展览服务，企业管理咨询，企业登记代理。', '计算机系统设计；平面及立体设计制作；网页设计；计算机系统集成；网络设备安装与维护；计算机技术服务与技术咨询；智能网络控制系统设备的设计及安装；网络系统工程设计与安装；安全防范设备的安装与维护。',
              '设计、制作、发布、代理国内外各类广告，商务信息咨询，会展会务、展览展示服务，企业形象策划，文化艺术交流活动策划（演出经纪除外），公关活动组织策划，体育赛事活动策划，建筑装饰装修建设工程设计施工一体化，广告装饰材料、工艺品（文物除外）的批发、网上零售、进出口、佣金代理（拍卖除外），并提供相关的配套服务；代办商标在国外注册；自营和代理除国家有特殊规定的进出口商品外的进出口业务。',
              '企业登记，代理记帐，财税咨询、审计咨询、投资咨询。税控机技术咨询。', '建设项目管理，工程咨询，招标代理，工程监理，建筑工程，市政、园林绿化工程，建筑装潢，建设项目业务咨询领域内的技术开发、技术转让、技术咨询、技术服务，建筑装潢材料及建筑设备的采购、销售，建筑机械租赁，会展会务服务；',
              '医疗器械及相关产品的设计、制造、开发和销售，实业投资，技术服务及对外合资合作，金属材料，化工材料（除危险品），包装材料，橡胶结合剂砂轮（限分支机构经营），本企业及其成员企业自产产品及技术的出口业务，本企业及其成员企业生产、科研所需的原辅材料、仪器仪表、机械设备、零配件及技术的进口业务（国家限定公司经营国家禁止进出口的商品及技术除外），进料加工和“三来一补”业务，日用百货销售。',
              '年度会计报表审计、验资，绩效评价考核审计、经理离任审计、内部审计、清算审计、公司转让审计、公司收购审计、特定项目审计、协助鉴别经济案件证据。涉税事项鉴证、审核、代理、咨询（顾问）和培训，税收筹划；资产评估：企业价值、房地产、机器设备评估，企业投资等评估；管理咨询：财务会计咨询顾问（总监），会计制度设计、项目可行性研究，会计人员培训，企业管理咨询；会计服务：账目清理、代理记账及其他会计咨询和会计服务；商务服务：代办公司注册、筹建、年审、清算，公司秘书等服务（持企业登记代理资格证经营）',
              '货运代理，水上国际货运代理，国际公路货运代理，航空国际货运代理，仓储服务（除成品油、危险品），从事货物及技术的进出口业务，商务咨询。','许可证批准范围内的危险化学品、农药生产及销售；（有效期限以许可证为准）；84消毒液的生产及销售（有效氯≤5%）；焊接气瓶的检验检测、安全阀校验维修（凭许可证经营）。化工机械生产销售；该公司生产科研所需原材料、机械设备、仪器、仪表、配件、中间体的进口及相关技术的服务；进出口业务（进出口国营贸易管理货物除外）；（以下限分公司经营）化学肥料生产销售。（依法须经批准的项目，经相关部门批准后方可开展经营活动）',
              '经营中国籍国际船舶以及经交通部核准的自有方便旗船舶和自营（期租和光租）船舶的国际船舶代理及相关业务；联系引水、*泊、装卸；组织承揽海运货物、集装箱；办理货物、集装箱订仓、报关、转运、仓储和多式联运；代签提单；代办船舶供应、租船、船员旅客服务等委托业务；许可范围内的船舶维修业务',
              '国内航线除香港、澳门、台湾地区航线外的航空客运代理业务（在证书批准有效期内经营）、代订客房，代订火车票，相关的信息咨询。 维修许可限定的航空器及地面设备维修，客货运输代理；国内旅游（限旅行社）及信息咨询。',
              '轻工新产品、原料的技术开发、成果转让、咨询服务；日用化学品（不含化学危险品）、摩托车、轻工业专用机械、马口铁、钢材、木材、家用电器、建筑材料销售；空调、制冷设备的销售与售后服务；许可范围内的葡萄酒及葡萄制品的生产、销售。',
              '物业管理，停车场管理服务，家政服务，专业保洁、清洗、消毒服务，房屋维修，建筑设备维修，园林绿化工程，环境卫生公共设施安装服务','光缆线路通信网络建设施工、技术开发维护、抢修、监测；智能大厦综合布线工程、计算机网络工程开发、施工；通信器材及设备销售。',
              '会议及文体活动策划、公共关系策划及咨询、市场信息咨询服务。', '蔬菜的种植、销售；水产品、牲畜、家禽养殖、销售；饮用水的生产、销售，饮水机销售；花卉、苗木的种植、销售。',
              '环保设备、水处理设备、净水设备、超纯水设备及水处理相关配件的设计、研制、开发、技术成果转让、技术服务及销售。水处理滤芯、滤材的设计、研制、开发、技术成果转让、技术服务及销售。开关电源设备及相关设备的设计、研制、开发、销售、技术成果转让。']


component_list = ['公有经济', '国有经济', '集体经济', '非公有经济', '私有经济', '港澳台经济', '外商经济', '其他所有制']


# 插入到企业基本信息维度表
def insertEnterpriseInfo(unified_social_credit_identifier, enterprise_name, enterprise_class, business_scope,
                         business_status, register_date, legal_person, legal_person_id, legal_person_phone,
                         register_capital, economic_component, address, district, is_delete, cur):
    sql = "INSERT INTO dim_msb_enterprise_info() VALUES('{unified_social_credit_identifier}', '{enterprise_name}', " \
          "'{enterprise_class}', '{business_scope}', '{business_status}', '{register_date}', " \
          "'{legal_person}', '{legal_person_id}', '{legal_person_phone}', '{register_capital}', " \
          "'{economic_component}', '{address}', '{district}', '{is_delete}')".\
        format(unified_social_credit_identifier=unified_social_credit_identifier, enterprise_name=enterprise_name,
               enterprise_class=enterprise_class, business_scope=business_scope, business_status=business_status,
               register_date=register_date, legal_person=legal_person, legal_person_id=legal_person_id,
               legal_person_phone=legal_person_phone, register_capital=register_capital,
               economic_component=economic_component, address=address,
               district=district, is_delete=is_delete)
    print(sql)
    cur.execute(sql)
    mysql_conn.commit()


# 得到爬虫拿的企查查数据
def qcc_enterprise(cur):
    sql = "SELECT * FROM qcc_enterprise_spider;"
    cur.execute(sql)
    return cur.fetchall()


# 生成企业基本信息维度数据
# 生成身份证号
def get_personal_id():
    ids = fake.ssn()
    year = str(2021 - random.randint(20, 59))
    month = str(random.randint(1, 12))
    day = str(random.randint(1, 28))
    if int(month) < 10:
        month = "0" + month
    if int(day) < 10:
        day = "0" + day
    res = '522' + ids[3:6] + year + month + day + ids[14:18]
    return res


def generate_enterprise1000():
    cur = mysql_conn.cursor()
    qcc_list = qcc_enterprise(cur)
    for i in qcc_list:
        unified_social_credit_identifier = i[0]
        enterprise_name = i[1]
        enterprise_class = random.choice(enterprise_class_list)
        business_scope = random.choice(scope_list)
        business_status = i[4]
        register_date = i[6]
        legal_person = i[2]
        legal_person_id = get_personal_id()
        legal_person_phone = i[3]
        if legal_person_phone == '-':
            legal_person_phone = fake.phone_number()
        register_capital = i[5]
        economic_component = random.choice(component_list)
        address = i[7]
        district = i[7][6:9]
        is_delete = '否'
        if business_status != '存续':
            is_delete = '是'
        insertEnterpriseInfo(unified_social_credit_identifier, enterprise_name, enterprise_class, business_scope,
                             business_status, register_date, legal_person, legal_person_id, legal_person_phone,
                             register_capital, economic_component, address, district, is_delete, cur)
    cur.close()


if __name__ == '__main__':
    generate_enterprise1000()
    pass
