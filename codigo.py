import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Acidentes PRF",
    page_icon="🚓",
    layout="wide"
)

# IDs dos arquivos no Google Drive
file_ids = {
    2013: "1tmO9ObhSVL-T-1SYfwmVWUy1ty7eSvfC",
    2014: "1hWRjCjsfrFUQmng-nnEdFLEVkH7G1eFo",
    2015: "1Zj4pMKTgs7gbkoPsFZOXf0I6NIlyW-Xm",
    2016: "1tkaZ_f1h9BXV_wyMQBT9Q5MVFjiZB6u6",
    2017: "1xdoSICx6jxQyaYu60hLknXInpzTfijmj",
    2018: "1ySuJBVH2QXXidkPSGJRWgHn765WtW3_g",
    2019: "1qNwih1aNhHcPpMjvWxLvBcciUehz2cTM",
    2020: "1yxyhH2LyBKEAb_XBqaGEzIA1rY1aU1IP",
    2021: "1Xje5rMD7hrlRO8rWSWoWaCco3E6RHWyA",
    2022: "1V5eV7wBI1lMUd2lFnYV7XRBR46A0TLMZ",
    2023: "1nOOQVKrCwLWrl9M2hyEcbanCS8ngO10t"
}

# Função para carregar os dados diretamente do Google Drive
@st.cache_data
def load_data(years):
    dfs = []
    for year in years:
        file_id = file_ids[year]
        url = f'https://drive.google.com/uc?id={file_id}'
        df = pd.read_csv(url, encoding='latin-1', delimiter=';')
        df['ano'] = year
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

@st.cache_data
def load_population_data():
    return pd.read_csv('cidades.csv', encoding='latin-1', delimiter=',')

@st.cache_data
def load_vehicle_fleet_data():
    return pd.read_csv('frota_munic_modelo_dezembro_2023.csv', encoding='latin-1', delimiter=',')

# Carregando dados dos acidentes de 2013 a 2023
years = list(range(2013, 2024))
df = load_data(years)

# Carregar os dados de população e frota de automóveis
pop_data = load_population_data()
fleet_data = load_vehicle_fleet_data()

# Filtrar as colunas relevantes e renomear para consistência
pop_data = pop_data[['UF', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
pop_data.columns = ['UF', 'Município', 'População']

fleet_data = fleet_data[['UF', 'MUNICIPIO', 'TOTAL']]
fleet_data.columns = ['UF', 'Município', 'Total Veículos']

# Padronizar os nomes dos municípios para capslock
df['municipio'] = df['municipio'].str.upper()
pop_data['Município'] = pop_data['Município'].str.upper()
fleet_data['Município'] = fleet_data['Município'].str.upper()

# Mesclar os dados de acidentes com os dados de população e frota
df = df.merge(pop_data, left_on=['uf', 'municipio'], right_on=['UF', 'Município'], how='left')
df = df.merge(fleet_data, left_on=['uf', 'municipio'], right_on=['UF', 'Município'], how='left')

# Preencher valores ausentes
df['População'].fillna(0, inplace=True)
df['Total Veículos'].fillna(0, inplace=True)

# Barra lateral
st.sidebar.header("Configurações")
page = st.sidebar.selectbox("Escolha a Página", ["Visão Geral", "Filtros e Dados", "Análise 2023"])

def show_overview():
    # Visão geral 
    st.header("Visão Geral do Projeto")
    st.write("Bem-vindo ao projeto de Visualização de dados da base de dados da PRF. Este projeto gira em torno da análise e apresentação "
             "de dados de acidentes, localização, motivos e categorias. O conjunto de dados contém várias colunas fornecendo insights "
             "sobre os acidentes e informações relacionadas.")
    
    # Como Funciona
    st.header("Como Funciona")
    st.write("O projeto utiliza um conjunto de dados com informações sobre acidentes nas rodovias federais. Aqui está uma breve visão "
             "geral dos principais componentes:")
    
    st.markdown("- *Conjunto de Dados*: O conjunto de dados consiste em registros de acidentes, cada um contendo informações como data, "
                "local, motivo, tipo e mais.")
    
    # Objetivo do Projeto
    st.header("Objetivo do Projeto")
    st.write("O principal objetivo deste projeto é obter insights pela análise dos dados e gráficos criados. Isso inclui entender "
             "o que os dados estão nos dizendo, identificar e explorar padrões dos acidentes, "
             "prevendo e criando estratégias para melhorar a segurança nas estradas.")
    
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
    # Seleção do ano e estado na barra lateral
    ano_selecionado = st.sidebar.selectbox('Selecione o Ano', options=years, key='year_select')
    estados = ["Todos"] + list(df['uf'].unique())
    UF = st.sidebar.selectbox('Selecione o UF', options=estados, key='filters_data_uf')
    
    # Filtrar os dados pelo ano e estado selecionados
    df_ano = df[df['ano'] == ano_selecionado]
    if UF != "Todos":
        df_ano = df_ano[df_ano['uf'] == UF]

    st.header('Gráficos')

    # Gráfico de quantidade de acidentes por município
    contagem_acidentes_por_municipio = df_ano['municipio'].value_counts().reset_index()
    contagem_acidentes_por_municipio.columns = ['Município', 'Quantidade de Acidentes']
    fig1 = px.bar(contagem_acidentes_por_municipio, x='Município', y='Quantidade de Acidentes',
                  title='Quantidade de Acidentes por Município')
    st.plotly_chart(fig1)

    # Gráfico de quantidade de mortos por município
    soma_mortos_por_municipio = df_ano.groupby('municipio')['mortos'].sum().reset_index()
    soma_mortos_por_municipio.columns = ['Município', 'Quantidade de Mortos']
    fig2 = px.line(soma_mortos_por_municipio, x='Município', y='Quantidade de Mortos',
                   title='Quantidade de Mortos por Município')
    st.plotly_chart(fig2)

    # Novo gráfico: Acidentes por 1000 habitantes
    df_ano['Acidentes por 1000 Habitantes'] = (df_ano['municipio'].map(df_ano['municipio'].value_counts()) / df_ano['População']) * 1000
    acidentes_por_habitante = df_ano[['municipio', 'Acidentes por 1000 Habitantes']].drop_duplicates()
    fig3 = px.bar(acidentes_por_habitante, x='municipio', y='Acidentes por 1000 Habitantes',
                  title='Acidentes por 1000 Habitantes')
    st.plotly_chart(fig3)

    # Novo gráfico: Acidentes por 1000 veículos
    df_ano['Acidentes por 1000 Veículos'] = (df_ano['municipio'].map(df_ano['municipio'].value_counts()) / df_ano['Total Veículos']) * 1000
    acidentes_por_veiculo = df_ano[['municipio', 'Acidentes por 1000 Veículos']].drop_duplicates()
    fig4 = px.bar(acidentes_por_veiculo, x='municipio', y='Acidentes por 1000 Veículos',
                  title='Acidentes por 1000 Veículos')
    st.plotly_chart(fig4)

    # Gráfico de acidentes e casualidades ao longo do tempo
    df_ano['data_inversa'] = pd.to_datetime(df_ano['data_inversa'])
    accidents_count = df_ano.groupby('data_inversa').size().reset_index(name='Número de Acidentes')
    fig5 = px.scatter(accidents_count, x='data_inversa', y='Número de Acidentes',
                      title='Número de Acidentes ao Longo do Tempo')
    st.plotly_chart(fig5)

    df_ano['year_month'] = df_ano['data_inversa'].dt.to_period('M')

    # Agrupar os dados por mês e somar os valores
    monthly_casualties = df_ano.groupby('year_month').agg({
        'mortos': 'sum', 
        'feridos_leves': 'sum', 
        'feridos_graves': 'sum', 
        'ilesos': 'sum'
    }).reset_index()
    
    # Converter o período para string para fins de plotagem
    monthly_casualties['year_month'] = monthly_casualties['year_month'].astype(str)
    
    # Criar o gráfico de barras empilhadas
    fig6 = px.bar(
        monthly_casualties, 
        x='year_month', 
        y=['mortos', 'feridos_leves', 'feridos_graves', 'ilesos'],
        title='Número de Casualidades por Mês',
        labels={'value': 'Total de Casualidades', 'year_month': 'Mês'},
        color_discrete_sequence=['#FF0000', '#0000FF', '#FFA500', '#00FF00'] # Ajuste as cores conforme necessário
    )
    
    fig6.update_layout(barmode='stack')
    st.plotly_chart(fig6)

    # Gráfico de número de acidentes por hora do dia
    df_ano['hora'] = pd.to_datetime(df_ano['horario']).dt.hour
    accidents_by_hour = df_ano.groupby('hora').size().reset_index(name='Número de Acidentes')
    fig7 = px.bar(accidents_by_hour, x='hora', y='Número de Acidentes',
                  title='Número de Acidentes por Hora do Dia')
    st.plotly_chart(fig7)

    # Mapa coroplético de acidentes por estado
    acidentes_por_estado = df.groupby(['uf', 'ano']).size().reset_index(name='Quantidade de Acidentes')
    df_ano_estado = acidentes_por_estado[acidentes_por_estado['ano'] == ano_selecionado]
    
    fig8 = px.choropleth(df_ano_estado, 
                        geojson='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson',
                        locations='uf', 
                        featureidkey='properties.sigla', 
                        color='Quantidade de Acidentes',
                        hover_name='uf',
                        title=f'Quantidade de Acidentes por Estado em {ano_selecionado}',
                        color_continuous_scale='Reds'
    )
    
    fig8.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig8)

if page == "Visão Geral":
    show_overview()
elif page == "Filtros e Dados":
    show_filters_data()
elif page == "Análise 2023":
    show_analysis_2023()
