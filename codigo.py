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

    df = pd.read_csv('datatran2023.csv')
    st.write(df.head())  # Verificar os primeiros dados do DataFrame

    # Geração de gráficos
    fig, ax = plt.subplots()
    ax.plot(df['dia_semana'], df['mortos'])
    plt.show()  # Mostrar o gráfico usando Matplotlib
    st.pyplot(fig)
