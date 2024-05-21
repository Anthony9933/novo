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
    
    st.markdown("- *Conjunto de Dados*: O conjunto de dados consiste em avaliações, cada uma contendo informações como data "
                "local, motivo, tipo e mais.")
    st.markdown("- *Explicação das Colunas*: As colunas do conjunto de dados fornecem detalhes sobre vendas, produtos, "
                "estoque e insights.")
    
    # Objetivo do Projeto
    st.header("Objetivo do Projeto")
    st.write("O principal objetivo deste projeto é obter insights pela análise dos dados e gráficos criados. Isso inclui entender "
             "o que os dados estão nos dizendo, identificar e explorar padrões dos compradores "
             "prevendo e criando estratégias para aumentar as vendas.")
    
    # Como Utilizar
    st.header("Como Utilizar")
    st.write("Para explorar o projeto, você pode navegar por diferentes seções usando a barra lateral. As principais seções incluem:")
    st.markdown("- *Visualização do Conjunto de Dados*: Oferece uma visão rápida dos dados disponíveis.")
    st.markdown("- *Descrição das Colunas*: Explica o significado de cada coluna no conjunto de dados.")
    st.markdown("- *Estatísticas Resumidas*: Apresenta informações estatísticas sobre o conjunto de dados.")
    
    st.header("Conclusão")
    st.write("Sinta-se à vontade para analisar o conjunto de dados, obter insights e tirar conclusões significativas a partir "
             "dos dados apresentados. Para análises específicas ou dúvidas, novos recursos podem ser incorporados com base nos "
             "objetivos do seu projeto.")

    st.write("Aproveite a exploração do projeto!")

def show_filters_data():
    st.header("Filtros e Dados")
    df = pd.read_csv('datatran2023.csv', encoding='latin-1', delimiter=';')

    # Adicionar um seletor de estado na barra lateral
    estados = ["Todos"] + list(df['uf'].unique())
    UF = st.sidebar.selectbox('Selecione o UF', options=estados, key='filters_data_uf')

    # Filtrar o dataframe pelo estado selecionado
    if UF == "Todos":
        df_uf = df
    else:
        df_uf = df[df['uf'] == UF]

    # Exibir o dataframe filtrado
    st.subheader('Dados Filtrados')
    st.dataframe(df_uf)

    st.header('Gráficos')

    # Gráfico de quantidade de acidentes por município
    contagem_acidentes_por_municipio = df_uf['municipio'].value_counts().reset_index()
    contagem_acidentes_por_municipio.columns = ['Município', 'Quantidade de Acidentes']
    fig1 = px.bar(contagem_acidentes_por_municipio, x='Município', y='Quantidade de Acidentes',
                  title='Quantidade de Acidentes por Município')
    st.plotly_chart(fig1)

    # Gráfico de quantidade de mortos por município
    soma_mortos_por_municipio = df_uf.groupby('municipio')['mortos'].sum().reset_index()
    soma_mortos_por_municipio.columns = ['Município', 'Quantidade de Mortos']
    fig2 = px.line(soma_mortos_por_municipio, x='Município', y='Quantidade de Mortos',
                   title='Quantidade de Mortos por Município')
    st.plotly_chart(fig2)

    # Gráfico de acidentes e casualidades ao longo do tempo
    df_uf['data_inversa'] = pd.to_datetime(df_uf['data_inversa'])

    accidents_count = df_uf.groupby('data_inversa').size().reset_index(name='Número de Acidentes')
    fig3 = px.scatter(accidents_count, x='data_inversa', y='Número de Acidentes',
                   title='Número de Acidentes ao Longo do Tempo')
    st.plotly_chart(fig3)

    #casualties = df_uf.groupby('data_inversa').agg({'mortos': 'sum', 'feridos_leves': 'sum', 'feridos_graves': 'sum', 'ilesos': 'sum'}).reset_index()
    #fig4 = px.line(casualties, x='data_inversa', y='mortos', title='Número de Mortos ao Longo do Tempo')
    #fig4.add_scatter(x=casualties['data_inversa'], y=casualties['feridos_leves'], mode='lines', name='Feridos Leves')
    #fig4.add_scatter(x=casualties['data_inversa'], y=casualties['feridos_graves'], mode='lines', name='Feridos Graves')
    #fig4.add_scatter(x=casualties['data_inversa'], y=casualties['ilesos'], mode='lines', name='Ilesos')
    #st.plotly_chart(fig4)

    df_uf['year_month'] = df_uf['data_inversa'].dt.to_period('M')

    # Agrupar os dados por mês e somar os valores
    monthly_casualties = df_uf.groupby('year_month').agg({
        'mortos': 'sum', 
        'feridos_leves': 'sum', 
        'feridos_graves': 'sum', 
        'ilesos': 'sum'
    }).reset_index()
    
    # Converter o período para string para fins de plotagem
    monthly_casualties['year_month'] = monthly_casualties['year_month'].astype(str)
    
    # Criar o gráfico de barras empilhadas
    fig = px.bar(
        monthly_casualties, 
        x='year_month', 
        y=['mortos', 'feridos_leves', 'feridos_graves', 'ilesos'],
        title='Número de Casualidades por Mês',
        labels={'value': 'Total de Casualidades', 'year_month': 'Mês'},
        color_discrete_sequence=['#FF0000', '#0000FF', '#FFA500', '#00FF00'] # Ajuste as cores conforme necessário
    )
    
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig)

    # Gráfico de número de acidentes por hora do dia
    df_uf['hora'] = pd.to_datetime(df_uf['horario']).dt.hour
    accidents_by_hour = df_uf.groupby('hora').size().reset_index(name='Número de Acidentes')
    fig5 = px.bar(accidents_by_hour, x='hora', y='Número de Acidentes',
                  title='Número de Acidentes por Hora do Dia')
    st.plotly_chart(fig5)


    # Extrair o ano da coluna 'data_inversa'
    df['ano'] = pd.to_datetime(df['data_inversa']).dt.year
    
    # Agrupar por UF e ano para obter a soma de acidentes por estado e ano
    acidentes_por_estado = df.groupby(['uf', 'ano']).size().reset_index(name='Quantidade de Acidentes')
    
    # Selecionar um ano específico ou mostrar a soma total
    anos = sorted(acidentes_por_estado['ano'].unique())
    ano_selecionado = st.sidebar.selectbox('Selecione o Ano', options=anos, key='year_select')
    
    # Filtrar o DataFrame pelo ano selecionado
    df_ano = acidentes_por_estado[acidentes_por_estado['ano'] == ano_selecionado]
    
    # Criar o mapa coroplético
    fig6 = px.choropleth(df_ano, 
                        geojson='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson',
                        locations='uf', 
                        featureidkey='properties.sigla', 
                        color='Quantidade de Acidentes',
                        hover_name='uf',
                        title=f'Quantidade de Acidentes por Estado em {ano_selecionado}')
    
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig6)



# Página de Visão Geral
if page == "Visão Geral":
    show_overview()

# Página de Filtros e Dados
elif page == "Filtros e Dados":
    show_filters_data()


    
# Página de Filtros de acidentes
#elif page == "Gráficos de Acidentes e Casualidades ao Longo do Tempo":
    #show_graphs()

#elif page == "Número de Acidentes por Hora do Dia":
    #show_accidents_by_hour()
