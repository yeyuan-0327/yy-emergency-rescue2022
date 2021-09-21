import pymysql

# 连接MySQL数据库
mysql_conn = pymysql.connect(host="192.168.101.105", user="root", password="123456", db="dim", port=3306,
                             charset='utf8')


def search(cur):
    sql = "SELECT person_id , person_name, date_add(birth, interval 20 year) as check_time FROM dim_psb_residents WHERE sex = '男' AND marital_status = '已婚' ORDER BY birth DESC;"
    cur.execute(sql)
    a = cur.fetchall()
    sql = "SELECT person_id , person_name FROM dim_psb_residents WHERE sex = '女'  AND marital_status = '已婚' ORDER BY birth DESC;"
    cur.execute(sql)
    b = cur.fetchall()
    return a, b


def insert(a, b, cur):
    for i in range(len(a)):
        man = a[i]
        woman = b[i]
        check_time = man[2]
        sql = "INSERT INTO dim_cab_marriage_info() VALUES('{man_person_id}','{man_person_name}','{check_time}'," \
              "'{woman_person_id}','{woman_person_name}')".format(man_person_id=man[0], man_person_name=man[1],
                                                                  check_time=check_time, woman_person_id=woman[0],
                                                                  woman_person_name=woman[1])
        print(sql)
        cur.execute(sql)
        mysql_conn.commit()

def generate_marriage():
    cur = mysql_conn.cursor()
    a, b = search(cur)
    insert(a, b, cur)
    cur.close()


if __name__ == '__main__':
    generate_marriage()
