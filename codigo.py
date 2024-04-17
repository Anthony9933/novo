import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração das páginas
st.set_page_config(page_title='Meu Web App', layout='wide')

# Menu lateral para navegação
with st.sidebar:
    page = st.radio('Navegue pelas páginas:', ['Apresentação', 'Gráficos'])

# Página de Apresentação
if page == 'Apresentação':
    st.title('Apresentação do Projeto')
    st.write('Aqui você pode escrever textos que apresentarão o projeto.')
    # Exemplo de campo de texto para entrada de dados
    st.text_area('Descrição do Projeto', 'Escreva aqui sobre o projeto...')

# Página de Gráficos
elif page == 'Gráficos':
    st.title('Gráficos')
    st.write('Gráficos gerados a partir da leitura de um arquivo CSV.')
    
    file_path = '/path/to/datatran2023.csv' # Replace this with the actual path to the file
    df = pd.read_csv(file_path)

    # Geração de gráficos
    fig, ax = plt.subplots()
    ax.plot(df['dia_semana'], df['mortos'])
    st.pyplot(fig)
