import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
page_config = {
    "page_title": "My Streamlit App",
    "page_icon": ":guardsman:",
    "layout": "wide",
}
st.set_page_config(**page_config)

# Page selection
page = st.sidebar.selectbox("Select a page", ["Apresentação", "Gráficos"])

# Apresentação page
if page == "Apresentação":
    st.title("Apresentação")
    st.write("Welcome to the Streamlit app! This page contains information about the app and its features.")

# Gráficos page
if page == "Gráficos":
    st.title("Gráficos")

    # Load CSV file
    df = pd.read_csv("datatran2023.csv")

    # Generate bar chart
    chart = px.bar(df, x="id", y="dia_semana", title="My Bar Chart")

    # Display chart
    st.plotly_chart(chart)
