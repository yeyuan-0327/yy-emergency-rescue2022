import requests
import re
from faker import Faker
import random
import pymysql

fake = Faker('zh_CN')
user_agent = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
              'Version/5.1 Safari/534.50 ',
              'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 '
              'Safari/534.50',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
              'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1']
# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')


# 插入到数据库
def insertQccEnterprise(enterprise_name, legal_person, business_status, capital, register_date, legal_person_phone,
                        address, cur):
    unified_social_credit_identifier = fake.ean8() + fake.ean8() + str(random.randint(10, 99))
    try:
        sql = "INSERT INTO qcc_enterprise_spider() VALUE ('{unified_social_credit_identifier}','{enterprise_name}', " \
              "'{legal_person}', '{legal_person_phone}', '{business_status}', '{capital}', '{register_date}', " \
              "'{address}')" \
            .format(unified_social_credit_identifier=unified_social_credit_identifier, enterprise_name=enterprise_name,
                    legal_person=legal_person, legal_person_phone=legal_person_phone, business_status=business_status,
                    capital=capital, register_date=register_date, address=address)
        print(sql)
        cur.execute(sql)
        mysql_conn.commit()
    except Exception as e:
        print(e)
        pass


def get_one_page(urls):
    try:
        headers = {'User-Agent': random.choice(user_agent)}
        response = requests.get(urls, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(e)


def parse(html_content):
    tds = re.findall(r"<td>(.*?)</td>", html_content, re.S | re.M)  # 因为<tr>标签大多数不是在同一行，所以要加 re.S和re.M多行匹配
    cur = mysql_conn.cursor()
    for td in tds:
        title = re.findall(r">(.*?)</a>", td)
        enterprise_name = title[0]
        legal_person = title[1]
        span = re.findall(r"<span class=(.*?)</span>", td, re.S | re.M)
        p = re.findall(r"<p class=\"m-t-xs\">(.*?)</p>", td, re.S | re.M)
        business_status = '存续'
        capital = '-'
        register_date = '-'
        legal_person_phone = '-'
        address = '-'
        for i in span:
            s = i.split('>')[1]
            if '经营异常' in s:
                business_status = '注销'
            elif '注册资本' in s:
                capital = s.split('：')[1]
            elif '成立日期' in s:
                register_date = s.split('：')[1]
            elif '电话' in s:
                legal_person_phone = s.split('：')[1]
                if len(legal_person_phone) > 13:
                    legal_person_phone = legal_person_phone[:13]
            else:
                continue
        for i in p:
            s = i.split('：')
            if '地址' in s[0]:
                address = s[1].replace('\n', '').replace(' ', '')
                pass
        insertQccEnterprise(enterprise_name, legal_person, business_status, capital, register_date, legal_person_phone,
                            address, cur)
    cur.close()


if __name__ == '__main__':
    for x in range(1, 501):
        print(x)
        url = 'https://www.qcc.com/g_GZ_520100_' + str(x)
        html = get_one_page(url)
        parse(html)
    # sleep(1)
