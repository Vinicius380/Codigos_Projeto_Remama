    with grafico4: #Gráfico de radar        
        
        try:
            
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
            
            grupo_dados4 = pd.DataFrame({
            'Métrica': ['Saturação do Oxigenio', 'Oximetro Pulso', 'Frequência Cardíaca'],
            'Valor': [peso_oximetro_saturacao, peso_oximetro_pulso, peso_frequencia_cardiaca]})
                    
            grupo_dados3 = pd.DataFrame(dict(
            Métrica = ['Saturação do Oxigenio', 'Oximetro Pulso', 'Frequência Cardíaca'],
            Valor = [peso_oximetro_saturacao, peso_oximetro_pulso, peso_frequencia_cardiaca]))

            # Gráfico de radar
            fig_valores4 = px.line_polar(
                grupo_dados3,
                r = grupo_dados3["Valor"],  
                theta = grupo_dados3["Métrica"], 
                line_close=True,
                title="Gráfico de Radar para Dados de Saúde"
            )
            
            fig_valores4.update_traces(fill = "toself")


        except Exception as e:
            st.error(f"Erro ao criar gráfico de radar: {e}")
            
        st.plotly_chart(fig_valores4, use_container_width=True)