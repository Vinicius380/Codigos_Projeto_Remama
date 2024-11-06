# pip install mysql-connector-python
# pip install streamlit

import mysql.connector
import pandas as pd
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

# ********************** CONEXÃO COM O BANCO DE DADOS **********************

app = Flask("Sensores")     # Nome do aplicativo.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Configura o SQLAlchemy para rastrear modificações. 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_sensores'

mybd = SQLAlchemy(app)      # Cria uma instância do SQLAlchemy, passando a aplicação Flask como parâmetro. 

def conexao(query):
    conn = mysql.connector.connect(
        host ='127.0.0.1',
        port='3306',
        user='root',
        password='senai@134',
        db='bd_sensores'
              
    )
    
    dataframe = pd.read_sql(query, conn)
    
    conn.close()
    
    return dataframe