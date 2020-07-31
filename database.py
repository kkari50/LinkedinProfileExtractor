import pyodbc
import pandas as pd
import xlrd
import sqlalchemy
import urllib
from input_details import *



#create table in database and write data to table:---!!

def get_data(db_instance_name, db_name, uid=None,password=None):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={db_instance_name};'
        f'DATABASE={db_name};'
        f'Trusted_Connection=Yes;'
    )
    # cursor = conn.cursor()

    return conn

def database_handler(db_instance_name, db_name, db_table_name, data):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={db_instance_name};'
        f'DATABASE={db_name};'
        f'Trusted_Connection=Yes;'
    )

    conn.autocommit = True
    cursor = conn.cursor()

    q_use_db = f'USE {db_name}'
    cursor.execute(q_use_db)

    # if db_table_name == 'linkedin_profiles':
    #     # if table doesn't exist in database create table:
    #     q_create_table = f"IF NOT Exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME= '{db_table_name}')" \
    #         f'CREATE TABLE {db_table_name} (' \
    #         f'p_name varchar(max),' \
    #         f'p_role varchar(max),' \
    #         f'p_location varchar(max)),' \
    #         f'p_username varchar(max),' \
    #         f'p_user_link varchar(max),' \
    #         f'p_company_q varchar(max)' \
    #         f')'
    #     cursor.execute(q_create_table)


    params = urllib.parse.quote_plus(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={db_instance_name};"
                                     f"DATABASE={db_name};"
                                     f"autocommit=True;"
                                     f"Trusted_Connection=Yes;")

    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    data.to_sql(db_table_name, schema='dbo', con=engine, index=False, if_exists='append')

    print('Write to Database Successful..!!')

    cursor.close()
    conn.close()


def check_exisiting(cursor,table_name, username):
    query = f"select count(*) from {table_name} where p_username ='{username}';"
    res = cursor.execute(query)

    val = res.fetchall()[0][0]

    return val