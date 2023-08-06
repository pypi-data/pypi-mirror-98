from dataclasses import dataclass

import pymysql
import sqlalchemy as sqlalchemy
from sqlalchemy.engine.url import URL
import pandas as pd

@dataclass
class DBProperty:
    database_name: str = None
    user: str = None
    password: str = None
    host: str = None



class DB:
    database_name = None
    sqlalchemy_connector = None
    db_property = None

    def __init__(self, db_property: DBProperty):
        self.db_property = db_property
        self.sqlalchemy_connector = self._get_sqlalchemy_connector()
        self.pymysql_connector = self._get_pymysql_connector()
        self.pymysql_cursor = self.pymysql_connector.cursor()

    def _get_sqlalchemy_connector(self):
        pymysql.install_as_MySQLdb()
        conn = sqlalchemy.create_engine(URL(
            drivername='mysql',
            username=self.db_property.user,
            password=self.db_property.password,
            host=self.db_property.host,
            database=self.db_property.database_name
        ))
        return conn

    def _get_pymysql_connector(self):
        return pymysql.connect(
            host=self.db_property.host,
            user=self.db_property.user,
            password=self.db_property.password,
            db=self.db_property.database_name,
            charset='utf8'
        )

    def con_close(self):
        self.pymysql_connector.close()
        self.sqlalchemy_connector.dispose()

    def get_sqlalchemy_connector(self):
        return self.sqlalchemy_connector

    def get_pymysql_connector(self):
        return self.pymysql_connector

    def get_tables(self) -> list:
        sql = "show tables"
        table_df = pd.read_sql(sql=sql, con=self.sqlalchemy_connector)
        return table_df[table_df.columns[0]].to_list()

    def drop_table(self, table_name):
        sql = f"drop table {table_name}"
        self.pymysql_cursor.execute(sql)

    def drop_all_table(self):
        list(map(self.drop_table, self.get_tables()))


if __name__ == "__main__":
    db_prop = DBProperty()
    db_prop.database_name = 'krx'
    db_prop.user = 'root'
    db_prop.password = '3844'
    db_prop.host = 'localhost'
    db = DB(db_prop)

    print(db.get_tables())