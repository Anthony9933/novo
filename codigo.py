import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Sidebar (Menu Lateral)
page = st.sidebar.selectbox("Escolha a Página", ["Visão Geral", "Filtros e Dados"])

def show_overview():
    
    # Visão Geral do Projeto
    st.header("Visão Geral do Projeto")
    st.write("Bem-vindo ao projeto de Avaliações de Jogos no Steam! Este projeto gira em torno da análise e apresentação "
             "de avaliações de jogos na plataforma Steam. O conjunto de dados contém várias colunas fornecendo insights "
             "sobre as avaliações dos usuários, incluindo data de postagem, reações engraçadas, reações úteis, horas jogadas, "
             "status de acesso antecipado, recomendações e a própria análise escrita.")
    
    # Como Funciona
    st.header("Como Funciona")
    st.write("O projeto utiliza um conjunto de dados com informações sobre avaliações de jogos. Aqui está uma breve visão "
             "geral dos principais componentes:")
    
    st.markdown("- **Conjunto de Dados**: O conjunto de dados consiste em avaliações, cada uma contendo informações como data "
                "de postagem, reações do jogador, horas jogadas e mais.")
    st.markdown("- **Explicação das Colunas**: As colunas do conjunto de dados fornecem detalhes sobre quando a avaliação foi "
                "postada, reações do jogador, horas de jogo, status de acesso antecipado, recomendações do jogador e a própria análise escrita.")
    
    # Objetivo do Projeto
    st.header("Objetivo do Projeto")
    st.write("O principal objetivo deste projeto é obter insights das avaliações de jogos no Steam. Isso inclui entender "
             "os sentimentos dos jogadores, identificar jogos populares e explorar padrões nas recomendações dos jogadores "
             "durante períodos de acesso antecipado.")
    
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

    st.write("Aproveite a exploração do projeto de Avaliações de Jogos no Steam!")

def show_filters_data():
    st.header("Filtros e Dados")
    df = pd.read_csv('datatran2023.csv')
    st.dataframe(df)
    df['dia_semana'] = pd.to_datetime(df['dia_semana']).dt.name

    dia_semana = st.sidebar.selectbox('Selecione o Dia', options=df['dia_semana'].unique())
    early_access = st.sidebar.checkbox('Apenas Early Access')
    recommendation = st.sidebar.checkbox('Apenas Recomendados')

    filtered_df = df[df['dia_semama'] == dia_semana]
    if early_access:
        filtered_df = filtered_df[filtered_df['is_early_access_review'] == True]
    if recommendation:
        filtered_df = filtered_df[filtered_df['recommendation'] == "Recommended"]

    uf = st.sidebar.selectbox('Selecione um Estado', options=df['title'].unique())
    uf_df = filtered_df[filtered_df['title'] == uf]

    st.write(uf_df)


    st.header('Gráficos')

    # Média de acidentes por Uf
    id_uf = df.groupby('title')['id'].mean()
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(id_uf.index, id_uf.values)
    plt.xticks(rotation=90)
    plt.title('Média de acidentes por uf')
    plt.xlabel('Uf')
    plt.ylabel('Média de acidentes')
    st.pyplot(fig)

    # Quantidade de acidentes
    id_counts = df.groupby('title')['id'].sum()
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(id_counts.index, id_counts.values)
    plt.xticks(rotation=90)
    plt.title('Quantidade de acidentes por UF')
    plt.xlabel('UF')
    plt.ylabel('Quantidade de acidentes')
    st.pyplot(fig)


# Página de Visão Geral
if page == "Visão Geral":
    show_overview()

# Página de Filtros e Dados
elif page == "Filtros e Dados":
    show_filters_data()
