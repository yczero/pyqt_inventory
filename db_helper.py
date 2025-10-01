import pymysql

DB_CONFIG = dict(
    host = "localhost",
    user = "root",
    password = "qwer1234",
    database = "fruit_inverntory",
    charset = "utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config
    
    def connect(self):
        return pymysql.connect(**self.config)
    
        # 로그인 검증
    def verify_user(self, username, password):
        sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, password))
                count, = cur.fetchone()
                return count == 1
 
    def fetch_all_fruits(self):
        sql = "SELECT fruit_id, fruit_name, stock, price FROM fruits"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
    
    def insert_fruit(self, fruit_name, stock=0, price=0):
        sql = "INSERT INTO fruits (fruit_name, stock, price) VALUES (%s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (fruit_name, stock, price))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False
    
    def delete_fruit_by_name(self, fruit_name):
        sql = "DELETE FROM fruits WHERE fruit_name = %s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (fruit_name,))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False
            
    def update_fruit(self, fruit_name, stock, price):
        sql = "UPDATE fruits SET stock=%s, price=%s WHERE fruit_name=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (stock, price, fruit_name))
                conn.commit()
                return True
            except Exception as e:
                print("수정 오류:", e)
                conn.rollback()
                return False   





# # db_helper.py
# import pymysql

# DB_CONFIG = dict(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="sampledb",
#     charset="utf8"
# )

# class DB:
#     def __init__(self, **config):
#         self.config = config

#     def connect(self):
#         return pymysql.connect(**self.config)

#     # 로그인 검증
#     def verify_user(self, username, password):
#         sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
#         with self.connect() as conn:
#             with conn.cursor() as cur:
#                 cur.execute(sql, (username, password))
#                 count, = cur.fetchone()
#                 return count == 1

#     # 멤버 전체 조회
#     def fetch_members(self):
#         sql = "SELECT id, name, email FROM members ORDER BY id"
#         with self.connect() as conn:
#             with conn.cursor() as cur:
#                 cur.execute(sql)
#                 return cur.fetchall()  # [(id, name, email), ...]

#     # 멤버 추가
#     def insert_member(self, name, email):
#         sql = "INSERT INTO members (name, email) VALUES (%s, %s)"
#         with self.connect() as conn:
#             try:
#                 with conn.cursor() as cur:
#                     cur.execute(sql, (name, email))
#                 conn.commit()
#                 return True
#             except Exception:
#                 conn.rollback()
#                 return False