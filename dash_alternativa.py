import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from datetime import datetime
from streamlit_modal import Modal
import plotly.graph_objects as go

st.set_page_config(
    page_title="Remama",  # título da página
    page_icon=":dragon:",  # ícone da página (opcional)
    layout="wide",  # ou "wide", se preferir layout mais amplo
    initial_sidebar_state="collapsed",
)


st.sidebar.image("banner-remama-01-440x153.png", use_container_width=True)


query = "SELECT * FROM tb_dados"    # Consulta com o banco de dados.
df = conexao(query)                 # Carregar os dados do MySQL.

df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])  # Converter para datetime

# MENU LATERAL
st.sidebar.header('Selecione a informação para gerar o gráfico')

# Seleção de colunas X
colunaX = st.sidebar.selectbox(
    'Eixo X',
    options=['tempo_registro', 'oximetro_saturacao_oxigenio', 'oximetro_frequencia_pulso', 'frequencia_cardiaca', 'temperatura'],
    index=0
)

# Seleção de colunas Y
colunaY = st.sidebar.selectbox(
    'Eixo Y',
    options=['tempo_registro', 'oximetro_saturacao_oxigenio', 'oximetro_frequencia_pulso', 'frequencia_cardiaca', 'temperatura'],
    index=1
)

# Verificar se a coluna selecionada está nos eixos X ou Y
def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro de Range -> SLIDER
st.sidebar.header('Selecione o Filtro')

# Oximetro Saturação Oxigênio
if filtros('oximetro_saturacao_oxigenio'):
    oxigenio_range = st.sidebar.slider(
        'Saturação do Oxigênio',
        min_value=float(df['oximetro_saturacao_oxigenio'].min()),
        max_value=float(df['oximetro_saturacao_oxigenio'].max()),
        value=(float(df['oximetro_saturacao_oxigenio'].min()), float(df['oximetro_saturacao_oxigenio'].max())),
        step=0.1
    )

# Frequência Pulso
if filtros('oximetro_frequencia_pulso'):
    pulso_range = st.sidebar.slider(
        'Frequencia do Pulso',
        min_value=float(df['oximetro_frequencia_pulso'].min()),
        max_value=float(df['oximetro_frequencia_pulso'].max()),
        value=(float(df['oximetro_frequencia_pulso'].min()), float(df['oximetro_frequencia_pulso'].max())),
        step=0.1
    )

# Frequência Cardíaca
if filtros('frequencia_cardiaca'):
    pressao_range = st.sidebar.slider(
        'Frequência Cardiaca',
        min_value=float(df['frequencia_cardiaca'].min()),
        max_value=float(df['frequencia_cardiaca'].max()),
        value=(float(df['frequencia_cardiaca'].min()), float(df['frequencia_cardiaca'].max())),
        step=0.1
    )

# Temperatura
if filtros('temperatura'):
    altitude_range = st.sidebar.slider(
        'Temperatura',
        min_value=float(df['temperatura'].min()),
        max_value=float(df['temperatura'].max()),
        value=(float(df['temperatura'].min()), float(df['temperatura'].max())),
        step=0.1
    )

# Cria uma cópia do df original
df_selecionado = df.copy()

# Aplicando os filtros de acordo com os ranges selecionados
if filtros('oximetro_saturacao_oxigenio'):
    df_selecionado = df_selecionado[
        (df_selecionado['oximetro_saturacao_oxigenio'] >= oxigenio_range[0]) &
        (df_selecionado['oximetro_saturacao_oxigenio'] <= oxigenio_range[1])
    ]

if filtros('oximetro_frequencia_pulso'):
    df_selecionado = df_selecionado[
        (df_selecionado['oximetro_frequencia_pulso'] >= pulso_range[0]) &
        (df_selecionado['oximetro_frequencia_pulso'] <= pulso_range[1])
    ]

if filtros('frequencia_cardiaca'):
    df_selecionado = df_selecionado[
        (df_selecionado['frequencia_cardiaca'] >= pressao_range[0]) &
        (df_selecionado['frequencia_cardiaca'] <= pressao_range[1])
    ]

if filtros('temperatura'):
    df_selecionado = df_selecionado[
        (df_selecionado['temperatura'] >= altitude_range[0]) &
        (df_selecionado['temperatura'] <= altitude_range[1])
    ]



# Exibir Tabela
def Home():
    with st.expander('Tabela'):
        mostrarDados = st.multiselect(
            'Filtros: ',
            df_selecionado.columns,
            default=[],
            key='showData_home'
        )

        if mostrarDados:
            st.write(df_selecionado[mostrarDados])

    if not df_selecionado.empty:
        media_cardiaca = df_selecionado['frequencia_cardiaca'].mean()
        media_oxigenio = df_selecionado['oximetro_saturacao_oxigenio'].mean()

        media1, media2 = st.columns(2, gap='large')

        with media1:
            st.info('Média de Frequência Cardíaca', icon='📍')
            st.metric(label='Média', value=f'{media_cardiaca:.2f}')

        with media2:
            st.info('Média de Saturação de Oxigênio', icon='📍')
            st.metric(label='Média', value=f'{media_oxigenio:.2f}')

        st.markdown('''-----------''')


#Home()


col1, col2 = st.columns([2,1])


with col1:
    st.subheader('Dashboard de Monitoramento')
    
    # Gráfico de Barras
    with st.container():
        grupo_dados = df.groupby(by=[colunaX]).size().reset_index(name='Contagem')
        fig_bar = px.bar(grupo_dados, x=colunaX, y='Contagem', title=f'Contagem de Registros por {colunaX.capitalize()}')
        st.plotly_chart(fig_bar, use_container_width=True)
        

    # Gráfico Linear
    with st.container():
        grupo_dados2 = df.groupby(by=[colunaX])[colunaY].mean().reset_index(name=colunaY)
        fig_line = px.line(grupo_dados2, x=colunaX, y=colunaY, title=f"{colunaX.capitalize()} vs {colunaY.capitalize()}")
        st.plotly_chart(fig_line, use_container_width=True)
        
with col2:
    st.subheader("Tempo real")
    
    with st.container(): 
        
        oximetro_saturacao_oxigenio = conexao("SELECT AVG (oximetro_saturacao_oxigenio) FROM tb_dados")
        oximetro_frequencia_pulso = conexao("SELECT AVG (oximetro_frequencia_pulso) FROM tb_dados")
        frequencia_cardiaca = conexao("SELECT AVG (frequencia_cardiaca) FROM tb_dados")
                    
        oximetro_saturacao_valor = oximetro_saturacao_oxigenio.iloc[0, 0] if not oximetro_saturacao_oxigenio.empty else 0
        oximetro_frequencia_valor = oximetro_frequencia_pulso.iloc[0, 0] if not oximetro_frequencia_pulso.empty else 0
        frequencia_cardiaca_valor = frequencia_cardiaca.iloc[0, 0] if not frequencia_cardiaca.empty else 0
                    
        def calcular_peso(valor, tipo):
                        if tipo == "Saturação do Oxigenio":
                            if valor >= 95:
                                return 5
                            elif 90 <= valor < 95:
                                return 4
                            elif 85 <= valor < 90:
                                return 3
                            elif 80 <= valor < 85:
                                return 2
                            else:
                                return 1
                            
                        elif tipo == "oximetro_frequencia" or tipo == "frequencia_cardiaca":
                            if 60 <= valor <= 100:
                                return 5
                            elif 101 <= valor <= 120:
                                return 4
                            elif 121 <= valor <= 140:
                                return 3
                            elif 141 <= valor <= 160:
                                return 2
                            else:
                                return 1
                            
        peso_oximetro_saturacao = calcular_peso(oximetro_saturacao_valor, "Saturação do Oxigenio")
        peso_oximetro_pulso = calcular_peso(oximetro_frequencia_valor, "oximetro_frequencia")
        peso_frequencia_cardiaca = calcular_peso(frequencia_cardiaca_valor, "frequencia_cardiaca")
                    
        grupo_dados3 = pd.DataFrame({
                    'Métrica': ['Saturação do Oxigenio', 'Oximetro Pulso', 'Frequência Cardíaca'],
                    'Valor': [peso_oximetro_saturacao, peso_oximetro_pulso, peso_frequencia_cardiaca]})
                            
        grupo_dados3 = pd.DataFrame(dict(
                    Métrica = ['Saturação do Oxigenio', 'Oximetro Pulso', 'Frequência Cardíaca'],
                    Valor = [peso_oximetro_saturacao, peso_oximetro_pulso, peso_frequencia_cardiaca]))

                    # Gráfico de radar
        fig_valores3 = px.line_polar(
                        grupo_dados3,
                        r = grupo_dados3["Valor"],  
                        theta = grupo_dados3["Métrica"], 
                        line_close=True,
                        title="Avaliação dos Parâmetros de Saúde"
                    )
                    
        fig_valores3.update_traces(fill = "toself", line_color = "#0083b8")
                    
        fig_valores3.update_layout(
                        width=350,
                        height=350,
                        polar=dict(
                        angularaxis=dict(tickfont=dict(size=12)),
                        radialaxis=dict(tickfont=dict(size=14, color='black'))))

                    
        st.plotly_chart(fig_valores3, use_container_width=True)
        
    st.subheader("Frequência Cardíaca")
    
    # Gráfico de Medidor para Frequência Cardíaca
    with st.container():
    
    # Adiciona o velocímetro abaixo do gráfico de radar
     fig_velocimetro = go.Figure(go.Indicator(
        mode="gauge+number",
        value=frequencia_cardiaca_valor,  # Pode substituir pelo valor que deseja monitorar
        title={'text': "Frequência Cardíaca"},
        gauge={
            'axis': {'range': [0, 200]},  # Intervalo do velocímetro
            'bar': {'color': "#0083b8"},
            'steps': [
                {'range': [0, 100], 'color': "lightgray"},
                {'range': [100, 140], 'color': "gray"},
                {'range': [140, 200], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 160  # Limite para alerta
            }
        }
    ))

    fig_velocimetro.update_layout(width=350, height=350)  # Tamanho menor do velocímetro
    st.plotly_chart(fig_velocimetro, use_container_width=True)
        
    
if st.button("Atualizar dados"):
    df = conexao(query)