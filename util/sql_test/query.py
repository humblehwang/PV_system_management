from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4')

def get_user_record_by_pronum(pronum):

    sql = '''select * from user_record;'''

    df = pd.read_sql_query(sql, engine)

    user_data = df[df['pro_num']==pronum]

    return user_data.iloc[0]