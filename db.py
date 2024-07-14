import mysql.connector.pooling
import os

class Database:
    def __init__(self):
        self.pool_name = "my_pool"
        self.pool_size = 5
        self.cnxpool = self.create_pool()

    def create_pool(self):
        return mysql.connector.pooling.MySQLConnectionPool(
            pool_name=self.pool_name,
            pool_size=self.pool_size,
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            collation='utf8mb4_unicode_ci'
        )

    def get_connection(self):
        return self.cnxpool.get_connection()

    def close_connection(self, connection):
        connection.close()

    def query(self,query    ):
        print(query)
