import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from datetime import datetime
from streamlit_modal import Modal


query = "SELECT * FROM tb_dados"    # Consulta com o banco de dados.

df = conexao(query)                 # Carregar os dados do MySQL.

df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])  # Converter para datetime

if st.button("Atualizar dados"):     # Botão para atualização dos dados.
    df = conexao(query)

# MENU LATERAL
st.sidebar.header('Selecione a informação para gerar o gráfico')

# Seleção de colunas X      - SELECTBOX > Cria uma caixa de seleção na barra lateral
colunaX = st.sidebar.selectbox(
    'Eixo X',
    options=['tempo_registro', 'oximetro_saturacao_oxigenio', 'oximetro_frequencia_pulso', 'frequencia_cardiaca', 'temperatura'],
    index=0
)

colunaY = st.sidebar.selectbox(
    'Eixo X',
    options=['tempo_registro', 'oximetro_saturacao_oxigenio', 'oximetro_frequencia_pulso', 'frequencia_cardiaca', 'temperatura'],
    index=1
)

# Verificar quais os atributos do filtro
def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro de Range -> SLIDER
st.sidebar.header('Selecione o Filtro')


# UMIDADE
if filtros('oximetro_saturacao_oxigenio'):
    umidade_range = st.sidebar.slider(
        'Oximetro Saturação Oxigênio',
        # Valor Mínimo
        min_value=float(df['oximetro_saturacao_oxigenio'].min()),
        # Valor Máximo
        max_value=float(df['oximetro_saturacao_oxigenio'].max()),
        # Faixa de valores selecionados
        value=(float(df['oximetro_saturacao_oxigenio'].min()), float(df['oximetro_saturacao_oxigenio'].max())),
        # Incremento para cada movimento do slider
        step=0.1
    )


# TEMPERATURA
if filtros('oximetro_frequencia_pulso'):
    oximetro_frequencia_pulso = st.sidebar.slider(
        'Frequencia Pulso',
        # Valor Mínimo
        min_value=float(df['oximetro_frequencia_pulso'].min()),
        # Valor Máximo
        max_value=float(df['oximetro_frequencia_pulso'].max()),
        # Faixa de valores selecionados
        value=(float(df['oximetro_frequencia_pulso'].min()), float(df['oximetro_frequencia_pulso'].max())),
        # Incremento para cada movimento do slider
        step=0.1
    )


# PRESSAO
if filtros('frequencia_cardiaca'):
    pressao_range = st.sidebar.slider(
        'Frequência Cardiaca',
        # Valor Mínimo
        min_value=float(df['frequencia_cardiaca'].min()),
        # Valor Máximo
        max_value=float(df['frequencia_cardiaca'].max()),
        # Faixa de valores selecionados
        value=(float(df['frequencia_cardiaca'].min()), float(df['frequencia_cardiaca'].max())),
        # Incremento para cada movimento do slider
        step=0.1
    )


# ALTITUDE
if filtros('temperatura'):
    altitude_range = st.sidebar.slider(
        'Temperatura',
        # Valor Mínimo
        min_value=float(df['temperatura'].min()),
        # Valor Máximo
        max_value=float(df['temperatura'].max()),
        # Faixa de valores selecionados
        value=(float(df['temperatura'].min()), float(df['temperatura'].max())),
        # Incremento para cada movimento do slider
        step=0.1
    )


# Cria uma cópia do df original
df_selecionado = df.copy()

if filtros('oximetro_saturacao_oxigenio'):
    df_selecionado - df_selecionado[df_selecionado
    (df_selecionado['oximetro_saturacao_oxigenio'] >= oximetro_frequencia_pulso[0]) &
    (df_selecionado['oximetro_saturacao_oxigenio'] <= oximetro_frequencia_pulso[1])
    ]

if filtros('oximetro_frequencia_pulso'):
    df_selecionado - df_selecionado[df_selecionado
    (df_selecionado['oximetro_frequencia_pulso'] >= oximetro_frequencia_pulso[0]) &
    (df_selecionado['oximetro_frequencia_pulso'] <= oximetro_frequencia_pulso[1])
    ]

if filtros('frequencia_cardiaca'):
    df_selecionado - df_selecionado[df_selecionado
    (df_selecionado['frequencia_cardiaca'] >= oximetro_frequencia_pulso[0]) &
    (df_selecionado['frequencia_cardiaca'] <= oximetro_frequencia_pulso[1])
    ]

if filtros('temperatura'):
    df_selecionado - df_selecionado[df_selecionado
    (df_selecionado['temperatura'] >= oximetro_frequencia_pulso[0]) &
    (df_selecionado['temperatura'] <= oximetro_frequencia_pulso[1])
    ]

if filtros('tempo_registro'):
    df_selecionado - df_selecionado[df_selecionado
    (df_selecionado['tempo_registro'] >= oximetro_frequencia_pulso[0]) &
    (df_selecionado['tempo_registro'] <= oximetro_frequencia_pulso[1])
    ]


# GRAFICOS
def Home():
    with st.expander('Tabela'):
        mostrarDados = st.multiselect(
            'Filtro: ',
            df_selecionado.columns,
            default=[],
            key='showData_home'
        )

        if mostrarDados:
            st.write(df_selecionado[mostrarDados])

    if not df_selecionado.empty:
        media_cardiaca = df_selecionado['frequencia_cardiaca'].mean(),
        media_oxigenio = df_selecionado['oximetro_saturacao_oxigenio'].mean()

        media1, media2 = st.columns(2, gap='large')

        with media1:
            st.info('Média de Registros de Frequência Cardíaca', icon='📍')
            st.metric(label='Média', value=f'{media_cardiaca:.2f}')

        with media2:
            st.info('Média de Registros de Oxigênio', icon='📍')
            st.metric(label='Média', value=f'{media_oxigenio:.2f}')

        st.markdown('''-----------''')


# GRÁFICOS
def graficos():
    st.title('Dashboard Monitoramento')

    aba1 = st.table(['Gráfico de Linha', 'Gráfico de Dispersão'])

    with aba1:
        if df_selecionado.empty:
            st.write('Nenhum dado está disponível para gerar o gráfico')
            return
        
        if colunaX == colunaY:
            st.warning('Selecione uma opção diferente para os eixos X e Y')
            return
        
        try:
            grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name='contagem')

            fig_valores = px.bar(
                grupo_dados1,
                x=colunaX,
                y='Contagem',
                orientation='h',
                title=f'Contagem de Registros por {colunaX.capitalize()}',
                color_discrete_sequence=['#0083b8'],
                template='plotly_white'
            )

        except Exception as e:
            st.error(f'Erro ao criar o gráfico de linha: {e}')

        st.plotly_chart(fig_valores, use_container_width=True)