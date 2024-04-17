import streamlit as st
import plotly.express as px

# Page configuration
page_config = {
    "page_title": "My Streamlit App",
    "page_icon": ":guardsman:",
    "layout": "wide",
}
st.set_page_config(**page_config)

# Page selection
page = st.sidebar.selectbox("Select a page", ["Apresentation", "Gráficos"])

# Apresentation page
if page == "Apresentation":
    st.title("Apresentation")
    st.write("Welcome to the Streamlit app! This page contains information about the app and its features.")

# Gráficos page
if page == "Gráficos":
    st.title("Gráficos")

    # Load CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        # Generate bar chart
        chart = px.bar(data, x="column_name", y="value_column", title="My Bar Chart")

        # Display chart
        st.plotly_chart(chart)
