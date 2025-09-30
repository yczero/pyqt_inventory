import pymysql

DB_CONFIG = dict(
    host = "localhost",
    user = "root",
    password = "qwer1234",
    database = "fruit_inventory",
    charset = "utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config
    
    def connect(self):
        return pymysql.connect(**self.config)
 