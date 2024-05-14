import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
# Sidebar (Menu Lateral)
page = st.sidebar.selectbox("Escolha a Página", ["Visão Geral", "Filtros e Dados", "Gráficos de Acidentes e Casualidades ao Longo do Tempo", "Número de Acidentes por Hora do Dia"])
def show_overview():
    
    # Visão Geral do Projeto
    st.header("Visão Geral do Projeto")
    st.write("Bem-vindo ao projeto de Visualização de dados da base de dados da PRF.  Este projeto gira em torno da análise e apresentação "
             "de dados do acidentes, localização, motivos e categorias. O conjunto de dados contém várias colunas fornecendo insights "
             "sobre os produtos e informações relativas a vendas, incluindo data, produtos mais vendidos, melhores e piores meses de venda.")
    
    
    # Como Funciona
    st.header("Como Funciona")
    st.write("O projeto utiliza um conjunto de dados com informações sobre as vendas e o estoque da loja. Aqui está uma breve visão "
             "geral dos principais componentes:")
    
    st.markdown("- **Conjunto de Dados**: O conjunto de dados consiste em avaliações, cada uma contendo informações como data "
                "local, motivo, tipo e mais.")
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
    st.dataframe(df)
    UF = st.sidebar.selectbox('Selecione o UF', options=df['uf'].unique())

    # Filtrando o dataframe para apenas linhas do UF escolhido
    df_uf = df[df['uf'] == UF]

    # Contando o número de acidentes por município
    contagem_acidentes_por_municipio = df_uf['municipio'].value_counts().reset_index()

    # Renomeando as colunas para melhor entendimento
    contagem_acidentes_por_municipio.columns = ['Município', 'Quantidade de Acidentes']

    # Criando o gráfico
    fig = px.bar(contagem_acidentes_por_municipio, x='Município', y='Quantidade de Acidentes',
                 title='Quantidade de Acidentes por Município')
    st.plotly_chart(fig)


    soma_mortos_por_municipio = df_uf.groupby('municipio')['mortos'].sum().reset_index()

    # Renomeando as colunas para melhor entendimento
    soma_mortos_por_municipio.columns = ['Município', 'Quantidade de Mortos']

    # Criando o gráfico
    fig2 = px.line(soma_mortos_por_municipio, x='Município', y='Quantidade de Mortos',
                 title='Quantidade de Mortos por Município')

    st.plotly_chart(fig2)

def show_graphs():
    st.header("Gráficos de Acidentes e Casualidades ao Longo do Tempo")
    df = pd.read_csv('datatran2023.csv', encoding='latin-1', delimiter=';')

    # Convertendo a coluna 'data_inversa' para o tipo datetime
    df['data_inversa'] = pd.to_datetime(df['data_inversa'])

    # Agrupando os dados pela data e contando o número de acidentes
    accidents_count = df.groupby('data_inversa').size().reset_index(name='Número de Acidentes')

    # Criando o gráfico de linha para o número de acidentes ao longo do tempo
    fig3 = px.line(accidents_count, x='data_inversa', y='Número de Acidentes',
                  title='Número de Acidentes ao Longo do Tempo')
    st.plotly_chart(fig3)

    # Agrupando os dados pela data e somando o número de mortos, feridos leves, feridos graves e ilesos
    casualties = df.groupby('data_inversa').agg({'mortos': 'sum', 'feridos_leves': 'sum', 'feridos_graves': 'sum', 'ilesos': 'sum'}).reset_index()

    # Criando o gráfico de linha para o número de mortos, feridos leves, feridos graves e ilesos ao longo do tempo
    fig4 = px.line(casualties, x='data_inversa', y='mortos', title='Número de Mortos ao Longo do Tempo')
    fig4.add_scatter(x=casualties['data_inversa'], y=casualties['feridos_leves'], mode='lines', name='Feridos Leves')
    fig4.add_scatter(x=casualties['data_inversa'], y=casualties['feridos_graves'], mode='lines', name='Feridos Graves')
    fig4.add_scatter(x=casualties['data_inversa'], y=casualties['ilesos'], mode='lines', name='Ilesos')
    st.plotly_chart(fig4)

def show_accidents_by_hour():
    st.header("Número de Acidentes por Hora do Dia")
    df = pd.read_csv('datatran2023.csv', encoding='latin-1', delimiter=';')

    # Convertendo a coluna 'horario' para o tipo datetime e extraindo a hora
    df['hora'] = pd.to_datetime(df['horario']).dt.hour

    # Agrupando os dados pela hora e contando o número de acidentes
    accidents_count = df.groupby('hora').size().reset_index(name='Número de Acidentes')

    # Criando o gráfico de linha
    fig5 = px.bar(accidents_count, x='hora', y='Número de Acidentes',
                  title='Número de Acidentes por Hora do Dia')
    st.plotly_chart(fig5)



# Página de Visão Geral
if page == "Visão Geral":
    show_overview()

# Página de Filtros e Dados
elif page == "Filtros e Dados":
    show_filters_data()
    
# Página de Filtros de acidentes
elif page == "Gráficos de Acidentes e Casualidades ao Longo do Tempo":
    show_graphs()

elif page == "Número de Acidentes por Hora do Dia":
    show_accidents_by_hour()

