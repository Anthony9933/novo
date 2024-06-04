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
@st.cache
def load_data(years):
    dfs = []
    for year in years:
        file_id = file_ids[year]
        url = f'https://drive.google.com/uc?id={file_id}'
        df = pd.read_csv(url, encoding='latin-1', delimiter=';')
        df['ano'] = year
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

#carregando dados dos acidentes de 2013 a 2023
years = list(range(2013, 2024))
df = load_data(years)

#barra lateral
st.sidebar.header("Configurações")
page = st.sidebar.selectbox("Escolha a Página", ["Visão Geral", "Filtros e Dados", "Análise 2023"])

def show_overview():
    # visão geral 
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
    #st.header("Filtros e Dados")


    # Seleção do ano e estado na barra lateral
    ano_selecionado = st.sidebar.selectbox('Selecione o Ano', options=years, key='year_select')
    estados = ["Todos"] + list(df['uf'].unique())
    UF = st.sidebar.selectbox('Selecione o UF', options=estados, key='filters_data_uf')
    
    # Filtrar os dados pelo ano e estado selecionados
    df_ano = df[df['ano'] == ano_selecionado]
    if UF != "Todos":
        df_ano = df_ano[df_ano['uf'] == UF]
    # Exibir o dataframe filtrado
    #st.subheader('Dados Filtrados')
    #st.dataframe(df_ano)

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

    # Gráfico de acidentes e casualidades ao longo do tempo
    df_ano['data_inversa'] = pd.to_datetime(df_ano['data_inversa'])

    accidents_count = df_ano.groupby('data_inversa').size().reset_index(name='Número de Acidentes')
    fig3 = px.scatter(accidents_count, x='data_inversa', y='Número de Acidentes',
                      title='Número de Acidentes ao Longo do Tempo')
    st.plotly_chart(fig3)

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
    df_ano['hora'] = pd.to_datetime(df_ano['horario']).dt.hour
    accidents_by_hour = df_ano.groupby('hora').size().reset_index(name='Número de Acidentes')
    fig5 = px.bar(accidents_by_hour, x='hora', y='Número de Acidentes',
                  title='Número de Acidentes por Hora do Dia')
    st.plotly_chart(fig5)

    # Mapa coroplético de acidentes por estado
    acidentes_por_estado = df.groupby(['uf', 'ano']).size().reset_index(name='Quantidade de Acidentes')
    df_ano_estado = acidentes_por_estado[acidentes_por_estado['ano'] == ano_selecionado]
    
    fig6 = px.choropleth(df_ano_estado, 
                        geojson='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson',
                        locations='uf', 
                        featureidkey='properties.sigla', 
                        color='Quantidade de Acidentes',
                        hover_name='uf',
                        title='Quantidade de Acidentes por Estado em {ano_selecionado}',
                        color_continuous_scale='Reds'
    )
    
    fig6.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig6)


# Funções para carregar as novas bases de dados
@st.cache_data
def load_population_data():
    try:
        population_data = pd.read_csv('cidades.csv', encoding='latin-1')
        return population_data
    except Exception as e:
        return None

@st.cache_data
def load_vehicle_data():
    try:
        vehicle_data = pd.read_csv('frota_munic_modelo_dezembro_2023.csv', encoding='latin-1')
        return vehicle_data
    except Exception as e:
        return None

# Carregar os dados adicionais
population_df = load_population_data()
vehicle_df = load_vehicle_data()

# Verificar se os dados foram carregados corretamente
if population_df is not None:
    st.write("Population DataFrame:", population_df.head())
else:
    st.write("Failed to load population data.")

if vehicle_df is not None:
    st.write("Vehicle DataFrame:", vehicle_df.head())
else:
    st.write("Failed to load vehicle data.")

# Adicionar a nova página ao menu lateral e a lógica para mostrar a análise de 2023
def show_2023_analysis():
    st.header("Análise de 2023")
    # Funções para carregar as novas bases de dados
@st.cache_data
def load_population_data():
    try:
        population_data = pd.read_csv('cidades.csv', encoding='latin-1')
        return population_data
    except Exception as e:
        return None

@st.cache_data
def load_vehicle_data():
    try:
        vehicle_data = pd.read_csv('frota_munic_modelo_dezembro_2023.csv', encoding='latin-1')
        return vehicle_data
    except Exception as e:
        return None

# Carregar os dados adicionais
population_df = load_population_data()
vehicle_df = load_vehicle_data()

# Verificar se os dados foram carregados corretamente
if population_df is not None:
    st.write("Population DataFrame:", population_df.head())
else:
    st.write("Failed to load population data.")

if vehicle_df is not None:
    st.write("Vehicle DataFrame:", vehicle_df.head())
else:
    st.write("Failed to load vehicle data.")

    # Filtrar os dados de acidentes para 2023
    df_2023 = df[df['ano'] == 2023]

    # Verificar se as colunas 'municipio' e 'NOME DO MUNICÍPIO' estão presentes
    if 'municipio' not in df_2023.columns:
        st.write("A coluna 'municipio' não está presente nos dados de acidentes.")
        return

    if population_df is not None:
        if 'NOME DO MUNICÍPIO' not in population_df.columns:
            st.write("A coluna 'NOME DO MUNICÍPIO' não está presente nos dados de população.")
            return

        # Merge com a base de população
        df_merged = df_2023.merge(population_df, left_on='municipio', right_on='NOME DO MUNICÍPIO', how='left')
        st.write("Merge with population data successful.")
    else:
        st.write("População data is not available.")
        return

    # Verificar se as colunas 'municipio' e 'MUNICIPIO' estão presentes
    if vehicle_df is not None:
        if 'MUNICIPIO' not in vehicle_df.columns:
            st.write("A coluna 'MUNICIPIO' não está presente nos dados de veículos.")
            return

        # Merge com a base de veículos
        df_merged = df_merged.merge(vehicle_df, left_on='municipio', right_on='MUNICIPIO', how='left')
        st.write("Merge with vehicle data successful.")
    else:
        st.write("Vehicle data is not available.")
        return

    # Gráfico de acidentes por quantidade de habitantes
    df_merged['acidentes_por_habitante'] = df_merged.groupby('municipio')['id'].transform('count') / df_merged['POPULAÇÃO ESTIMADA']
    fig1 = px.scatter(df_merged, x='POPULAÇÃO ESTIMADA', y='acidentes_por_habitante',
                      title='Acidentes por Quantidade de Habitantes',
                      labels={'POPULAÇÃO ESTIMADA': 'População Estimada', 'acidentes_por_habitante': 'Acidentes por Habitante'})
    st.plotly_chart(fig1)

    # Gráfico de acidentes por tipo de veículo
    vehicle_types = ['AUTOMOVEL', 'CAMINHAO', 'MOTOCICLETA', 'ONIBUS', 'UTILITARIO']
    for vehicle_type in vehicle_types:
        df_merged[f'acidentes_por_{vehicle_type.lower()}'] = df_merged.groupby('municipio')['id'].transform('count') / df_merged[vehicle_type]
    
    fig2 = px.scatter_matrix(df_merged, dimensions=[f'acidentes_por_{vt.lower()}' for vt in vehicle_types],
                             title='Acidentes por Tipo de Veículo',
                             labels={f'acidentes_por_{vt.lower()}': f'Acidentes por {vt}' for vt in vehicle_types})
    st.plotly_chart(fig2)

    # Heatmap de distribuição de acidentes por dia da semana e hora
    df_merged['hora'] = pd.to_datetime(df_merged['horario']).dt.hour
    df_merged['dia_semana'] = pd.Categorical(df_merged['dia_semana'], 
                                             categories=['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo'], 
                                             ordered=True)
    heatmap_data = df_merged.groupby(['dia_semana', 'hora']).size().reset_index(name='Número de Acidentes')
    heatmap_data = heatmap_data.pivot('dia_semana', 'hora', 'Número de Acidentes')
    fig3 = px.imshow(heatmap_data, aspect='auto', title='Distribuição de Acidentes por Dia da Semana e Hora')
    st.plotly_chart(fig3)

    # Gráfico de barras empilhadas por tipo de acidente e classificação
    accident_types = df_merged.groupby(['tipo_acidente', 'classificacao_acidente']).size().reset_index(name='counts')
    fig4 = px.bar(accident_types, x='tipo_acidente', y='counts', color='classificacao_acidente',
                  title='Distribuição de Acidentes por Tipo e Classificação',
                  labels={'tipo_acidente': 'Tipo de Acidente', 'counts': 'Número de Acidentes', 'classificacao_acidente': 'Classificação'})
    st.plotly_chart(fig4)

    # Gráfico de barras empilhadas por condição meteorológica e tipo de acidente
    weather_conditions = df_merged.groupby(['condicao_metereologica', 'tipo_acidente']).size().reset_index(name='counts')
    fig5 = px.bar(weather_conditions, x='condicao_metereologica', y='counts', color='tipo_acidente',
                  title='Distribuição de Acidentes por Condição Meteorológica e Tipo de Acidente',
                  labels={'condicao_metereologica': 'Condição Meteorológica', 'counts': 'Número de Acidentes', 'tipo_acidente': 'Tipo de Acidente'})
    st.plotly_chart(fig5)

    # Gráfico de barras empilhadas por uso do solo e tipo de pista
    road_conditions = df_merged.groupby(['uso_solo', 'tipo_pista']).size().reset_index(name='counts')
    fig6 = px.bar(road_conditions, x='uso_solo', y='counts', color='tipo_pista',
                  title='Distribuição de Acidentes por Uso do Solo e Tipo de Pista',
                  labels={'uso_solo': 'Uso do Solo', 'counts': 'Número de Acidentes', 'tipo_pista': 'Tipo de Pista'})
    st.plotly_chart(fig6)

# Página de Visão Geral
if page == "Visão Geral":
    show_overview()

# Página de Filtros e Dados
elif page == "Filtros e Dados":
    show_filters_data()

# Página de Análise 2023
elif page == "Análise 2023":
    show_2023_analysis()
