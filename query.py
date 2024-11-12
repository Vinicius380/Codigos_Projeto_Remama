import mysql.connector
import pandas as pd

def conexao(query):
    conn = mysql.connector.connect(
        host ='127.0.0.1',
        port='3306',
        user='root',
        password='525748', #senai%40134
        db='bd_sensores'
              
    )
    
    dataframe = pd.read_sql(query, conn)
    
    conn.close()
    
    return dataframe