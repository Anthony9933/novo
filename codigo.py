import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
# Sidebar (Menu Lateral)
page = st.sidebar.selectbox("Escolha a Página", ["Visão Geral", "Filtros e Dados"])

def show_overview():
    
    # Visão Geral do Projeto
    st.header("Visão Geral do Projeto")
    st.write("Bem-vindo ao projeto de Visualização de dados da loja Moda Antiga! Este projeto gira em torno da análise e apresentação "
             "de dados do estoque e de vendas de produtos da loja Moda Antiga. O conjunto de dados contém várias colunas fornecendo insights "
             "sobre os produtos e informações relativas a vendas, incluindo data, produtos mais vendidos, melhores e piores meses de venda.")
    
    
    # Como Funciona
    st.header("Como Funciona")
    st.write("O projeto utiliza um conjunto de dados com informações sobre as vendas e o estoque da loja. Aqui está uma breve visão "
             "geral dos principais componentes:")
    
    st.markdown("- **Conjunto de Dados**: O conjunto de dados consiste em avaliações, cada uma contendo informações como data "
                "vendas, produtos, lucro e mais.")
    st.markdown("- **Explicação das Colunas**: As colunas do conjunto de dados fornecem detalhes sobre vendas, produtos, "
                "estoque e insights.")
    
    # Objetivo do Projeto
    st.header("Objetivo do Projeto")
    st.write("O principal objetivo deste projeto é obter insights pela análise dos dados e gráficos criados. Isso inclui entender "
             "o que os dados estão nos dizendo, identificar e explorar padrões dos compradores "
             "prevendo e criando estratégias para aumentar as vendas.")
    
    # Como Utilizar
    st.header("Como Utilizar")
    st.write("Para explorar o projeto, você pode navegar por diferentes seções usando a barra lateral. As principais seções incluem:")
    st.markdown("- **Visualização do Conjunto de Dados**: Oferece uma visão rápida dos dados disponíveis.")
    st.markdown("- **Descrição das Colunas**: Explica o significado de cada coluna no conjunto de dados.")
    st.markdown("- **Estatísticas Resumidas**: Apresenta informações estatísticas sobre o conjunto de dados.")
    
    st.header("Conclusão")
    st.write("Sinta-se à vontade para analisar o conjunto de dados, obter insights e tirar conclusões significativas a partir "
             "dos dados apresentados. Para análises específicas ou dúvidas, novos recursos podem ser incorporados com base nos "
             "objetivos do seu projeto.")

    st.write("Aproveite a exploração do projeto!")

def show_filters_data():
    st.header("Filtros e Dados")
    df = pd.read_csv('datatran2023.csv', encoding='latin-1', delimiter=';')
    st.header('Gráficos')
    UF = st.sidebar.selectbox('Selecione o Estado', options=df['uf'].unique())
    st.dataframe(df)
    # Filtrando o dataframe para apenas linhas do UF escolhido
    df_uf = df[df['uf'] == UF]

    # Contando o número de acidentes por município
    contagem_acidentes_por_municipio = df_uf['municipio'].value_counts().reset_index()

    # Renomeando as colunas para melhor entendimento
    contagem_acidentes_por_municipio.columns = ['Município', 'Quantidade de Acidentes']

    soma_mortos_por_municipio = df_uf.groupby('municipio')['mortos'].sum().reset_index()

    # Juntando os dois dataframes
    df_final = pd.merge(contagem_acidentes_por_municipio, soma_mortos_por_municipio, on='municipio')

    # Renomeando as colunas para melhor entendimento
    df_final.columns = ['Município', 'Quantidade de Acidentes', 'Quantidade de Mortos']

    # Criando o gráfico
    fig = px.histogram(df_final, x='Município', y=['Quantidade de Acidentes', 'Quantidade de Mortos'],
                       barmode='group', title='Quantidade de Acidentes e Mortos por Município')
    fig.show()

    st.write(df_final)
        #st.dataframe(df)
    
        #Dia = st.sidebar.selectbox('Selecione o Dia', options=df['dia_semana'].unique())
    
        #filtered_df = df[df['dia_semana'] == Dia]
    
        #contagem_id_por_uf = filtered_df.groupby('uf')['id'].nunique().reset_index()
    
        # Criando o gráfico
        #fig = px.bar(contagem_id_por_uf, x='uf', y='id', labels={'id':'Quantidade de IDs', 'uf':'UF'},
                     #title='Quantidade de IDs por UF')
        #fig.show()
    
        #st.write(contagem_id_por_uf)
    
        #st.header('Gráficos')

# Página de Visão Geral
if page == "Visão Geral":
    show_overview()

# Página de Filtros e Dados
elif page == "Filtros e Dados":
    show_filters_data()
