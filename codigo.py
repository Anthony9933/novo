
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the layout of the page
page_layout, sidebar_layout = st.beta_columns(2)

# Add the project presentation to the right side of the page
with page_layout:
    st.title("Project Presentation")
    st.write("Here is the project presentation...")
    st.write("## Section 1")
    st.write(
        """
        This is a longer section of text that spans multiple lines.
        It can include **bold text** and *italic text* as well.
        """
    )
    st.write("## Section 2")
    st.write(
        """
        <div style="background-color:lightblue; padding:20px;">
            This is a div with a light blue background and some padding.
        </div>
        """
    )

    # Add the option to open the graphs page
    if st.button("Open Graphs Page"):
        st.markdown("""
            <style>
            .css-18e3th9 {
                width: 100%;
                height: 100%;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 9999;
                background-color: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .css-18e3th9 iframe {
                border: none;
                width: 80%;
                height: 80%;
            }
            </style>
            <div class="css-18e3th9">
                <iframe src="https://github.com/username/repository/blob/main/graphs.html" frameborder="0"></iframe>
            </div>
        """)

# Add the sidebar to the left side of the page
with sidebar_layout:
    st.sidebar.title("Sidebar")
    if st.sidebar.button("Open Presentation Page"):
        st.experimental_rerun()

# Generate the graphs using a CSV file from a GitHub repository
df = pd.read_csv('datatran2023.csv')
df.plot(kind='bar')
plt.title('Bar Chart')
plt.xlabel('dia_semana')
plt.ylabel('id')
plt.show()
