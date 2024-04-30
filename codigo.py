import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly as pt
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
    st.dataframe(df)
    #df['dia_semana'] = pd.to_datetime(df['dia_semana']).dt.name

    Dia = st.sidebar.selectbox('Selecione o Dia', options=df['dia_semana'].unique())
    early_access = st.sidebar.checkbox('Apenas Early Access')
    recommendation = st.sidebar.checkbox('Apenas Recomendados')

    filtered_df = df[df['dia_semama'] == dia_semana]


    uf = st.sidebar.selectbox('Selecione um Estado', options=df['title'].unique())
    uf_df = filtered_df[filtered_df['title'] == uf]

    st.write(uf_df)


    st.header('Gráficos')

    # Média de acidentes por Uf
    id_uf = df.groupby('title')['id'].mean()
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(id_uf.index, id_uf.values)
    plt.xticks(rotation=90)
    plt.title('Média de acidentes por Estado')
    plt.xlabel('Uf')
    plt.ylabel('Média de acidentes')
    st.pyplot(fig)

    # Quantidade de acidentes
    id_counts = df.groupby('title')['id'].sum()
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(id_counts.index, id_counts.values)
    plt.xticks(rotation=90)
    plt.title('Quantidade de acidentes por Estado')
    plt.xlabel('uf')
    plt.ylabel('id_counts')
    st.pyplot(fig)


# Página de Visão Geral
if page == "Visão Geral":
    show_overview()

# Página de Filtros e Dados
elif page == "Filtros e Dados":
    show_filters_data()
