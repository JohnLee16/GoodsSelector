import pymysql

def get_connection():
    conn = pymysql.connect(
        host='localhost',
        port=3306,user='root',
        passwd='',
        db='pytest')
    return conn

def insert(sql):
    conn = get_connection()
    #get the cursor
    cursor = conn.cursor()
    result = cursor.execute(sql)
    print(result)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    sql = 'INSERT INTO test_student_table VALUES(1,\'zhang\',12);'
    insert(sql)