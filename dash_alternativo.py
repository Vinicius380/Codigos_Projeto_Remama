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

st.sidebar.image("remama-logo.png")

query = "SELECT * FROM tb_dados"    # Consulta com o banco de dados.
df = conexao(query)                 # Carregar os dados do MySQL.

df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])  # Converter para datetime

# MENU LATERAL
st.sidebar.header('Selecione a informação para gerar o gráfico')
tela = st.sidebar.selectbox('Tela', ['Menu Principal', 'Dados por Cadastro'])

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

# Tempo Registro
if filtros("tempo_registro"):
     # Extrair as datas mínimas e máximas em formato de datetime
    min_data = df["tempo_registro"].min()
    max_data = df["tempo_registro"].max()

    # Exibir dois campos de data para seleção de intervalo no sidebar
    data_inicio = st.sidebar.date_input(
            "Data de Início", 
            min_data.date(), 
            min_value=min_data.date(), 
            max_value=max_data.date(),
            format= "DD-MM-YYYY"
        )
        
    data_fim = st.sidebar.date_input(
            "Data de Fim", 
            max_data.date(), 
            min_value=min_data.date(), 
            max_value=max_data.date(),
            format= "DD-MM-YYYY"
        )

    # Converter as datas selecionadas para datetime, incluindo hora
    tempo_registro_range = (
            pd.to_datetime(data_inicio),
            pd.to_datetime(data_fim) + pd.DateOffset(days=1) - pd.Timedelta(seconds=1)
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


def dadosUsuario():

    st.sidebar.header('Selecione a informação que deseja ver')

    # Seleção de colunas X
    filtragem = st.sidebar.selectbox(
        'Eixo X',
        options=['Oxímetro de Oxigênio', 'Frequência do Pulso', 'Frequencia Cardíaca', 'Temperatura'],
        index=0
    )
    
    colunas_map = {
        'Oxímetro de Oxigênio': 'oximetro_saturacao_oxigenio',
        'Frequência do Pulso': 'oximetro_frequencia_pulso',
        'Frequencia Cardíaca': 'frequencia_cardiaca',
        'Temperatura': 'temperatura'
    }

    coluna_selecionada = colunas_map[filtragem]

    # Calcular a média e o histórico para a coluna selecionada
    df_media = df.groupby('id_paciente')[coluna_selecionada].mean().reset_index()
    df_media.columns = ['id', 'media']  # Renomeando as colunas para 'id' e 'media'

    df_historico = df.groupby('id_paciente')[coluna_selecionada].apply(list).reset_index()
    df_historico.columns = ['id', 'historico']  # Renomeando as colunas para 'id' e 'historico'

    # Juntando a média e o histórico em um único DataFrame
    df_usuario = pd.merge(df_media, df_historico, on='id')

    # Estabelecendo limites para moderação visual
    if filtragem == 'Oxímetro de Oxigênio':
        limite_baixo = 90
        limite_alto = 100
        
    elif filtragem == 'Frequencia Cardíaca':
        limite_baixo = 60
        limite_alto = 100

    elif filtragem == 'Frequência do Pulso':
        limite_baixo = 60 
        limite_alto = 100

    elif filtragem == 'Temperatura':
        limite_baixo = 36.5
        limite_alto = 37.5

    # Função para definir o nível
    def definir_nivel(media, limite_baixo, limite_alto):
        if media < limite_baixo: return "alerta", "#8093F1"
        elif limite_baixo <= media <= limite_alto: return "ok", "#F7AEF8"
        else: return "média", "#B388EB"

    # Aplicando a função de nível à média
    df_usuario['nivel'], _ = zip(*df_usuario['media'].apply(lambda media: definir_nivel(media, limite_baixo, limite_alto)))


    # Função de estilização para aplicar cores à coluna 'nivel'
    def aplicar_cores(val):
        color = {
            "ok": "#F7AEF8",
            "média": "#B388EB",
            "alerta": "#8093F1"
        }
        return f'background-color: {color.get(val, "#FFFFFF")}'

    df_usuario = df_usuario.style.applymap(aplicar_cores, subset=['nivel'])

    # Exibindo os dados no Streamlit com gráfico de histórico
    st.dataframe(
        df_usuario,
        column_config={
            "id": "ID da Paciente",
            "media": f"Média de {filtragem}",
            "historico": st.column_config.LineChartColumn(f"Histórico de {filtragem}"),
            "nivel": "Nível"
        },
        hide_index=True,
    )

#Home()

col1, col2, col3 = st.columns([3, 0.05, 1])

with col1:
    st.markdown("<h3 style='font-size:60px;'>Dashboard de Monitoramento</h3>", unsafe_allow_html=True)
    
    # Gráfico de Barras
    with st.container():
        grupo_dados = df.groupby(by=[colunaX]).size().reset_index(name='Contagem')
        fig_bar = px.bar(grupo_dados, x=colunaX, y='Contagem', title=f'Contagem de Registros por {colunaX.capitalize()}')
        fig_bar.update_layout(height=400, width=700)  # Ajustando tamanho
        st.plotly_chart(fig_bar, use_container_width=True)
        

    # Gráfico Linear
    with st.container():
        grupo_dados2 = df.groupby(by=[colunaX])[colunaY].mean().reset_index(name=colunaY)
        fig_line = px.line(grupo_dados2, x=colunaX, y=colunaY, title=f"{colunaX.capitalize()} vs {colunaY.capitalize()}")
        fig_line.update_layout(height=400, width=700)  # Ajustando tamanho
        st.plotly_chart(fig_line, use_container_width=True)
    
    with st.container():

        try:
            grupo_dados_X = df_selecionado.groupby(by=[colunaX]).size().reset_index(name='Contagem')
            grupo_dados_Y = df_selecionado.groupby(by=[colunaY]).size().reset_index(name='Contagem')

            fig_valores = go.Figure()

            fig_valores.add_trace(go.Scatter(
                x=grupo_dados_X[colunaX],       # Se pa o X é .count quantidade
                y=grupo_dados_X['Contagem'],       # Y fica com .size, ou seja tamanho
                fill='tozeroy',
                mode='none',
                name=f"Área de {colunaX.capitalize()}"
            ))

            # Adicionando a segunda trace (dados do eixo Y)
            fig_valores.add_trace(go.Scatter(
                x=grupo_dados_Y[colunaY],
                y=grupo_dados_Y['Contagem'],
                fill='tonexty',
                mode='none',
                name=f"Área de {colunaY.capitalize()}"
            ))

            # Estética
            fig_valores.update_layout(
                title=f'Gráfico de Área: {colunaX.capitalize()} vs {colunaY.capitalize()}',
                xaxis_title=colunaX.capitalize(),
                yaxis_title='Contagem',
                template='plotly_white',
                height=400,
                width=700  # Ajuste do tamanho
            )

            st.plotly_chart(fig_valores, use_container_width=True, key="grafico_area")

        except Exception as e:
            st.error(f"Erro ao criar gráfico de linhas: {e}")    
        
# Espaçamento entre colunas
with col2:
    st.markdown("<div style='padding: 0 10px;'></div>", unsafe_allow_html=True)
        
        
with col3:
    
    oximetro_saturacao_oxigenio = conexao("SELECT AVG (oximetro_saturacao_oxigenio) FROM tb_dados")
    oximetro_frequencia_pulso = conexao("SELECT AVG (oximetro_frequencia_pulso) FROM tb_dados")
    frequencia_cardiaca = conexao("SELECT AVG (frequencia_cardiaca) FROM tb_dados")
                    
    oximetro_saturacao_valor = oximetro_saturacao_oxigenio.iloc[0, 0] if not oximetro_saturacao_oxigenio.empty else 0
    oximetro_frequencia_valor = oximetro_frequencia_pulso.iloc[0, 0] if not oximetro_frequencia_pulso.empty else 0
    frequencia_cardiaca_valor = frequencia_cardiaca.iloc[0, 0] if not frequencia_cardiaca.empty else 0
    

    st.write("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)
           
        
    # Gráfico de Medidor para Frequência Cardíaca
    with st.container():

    # Velocímetro
     fig_velocimetro = go.Figure(go.Indicator(
        mode="gauge+number",
        value= frequencia_cardiaca_valor,  # Pode substituir pelo valor que deseja monitorar
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

    fig_velocimetro.update_layout(width=300, height=300)
    st.plotly_chart(fig_velocimetro, use_container_width=True)
    
    with st.container(): 
                
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
                        title="Indicadores de Saúde em Escala de 1 a 5"
                    )
                    
        fig_valores3.update_traces(fill = "toself", line_color = "#0083b8")
                    
        fig_valores3.update_layout(
                        width=400,
                        height=400,
                        polar=dict(
                        angularaxis=dict(tickfont=dict(size=12)),
                        radialaxis=dict(tickfont=dict(size=14, color='black'))))

                    
        st.plotly_chart(fig_valores3, use_container_width=True)
        
if st.button("Atualizar dados"):
    df = conexao(query)