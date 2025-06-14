import streamlit as st

# Home page layout
def home_page():
    st.image("data/ircsml.png", width=300)
    st.title("Welcome to the Home Page!")
    st.write("The research in mobility and logistics using digital technology and adding intelligence, autonomy, and decision is a strategic research and development promoted by the Kingdom Vision 2030, in this regard, future mobility is seeing a tremendous worldwide interest. Many industrial and research institutions are trying to get the lead in the development of the related technology and establish themselves as main players in the innovation market. SML research focuses on the three main pillars-Smart and Sustainable Technologies, Mobility Modes and Clean Energy, Logistics and Transportation Studies")
    st.write("You can navigate to the other pages using the menu in the sidebar.")
    st.sidebar.title("Center Information")
    st.sidebar.markdown("### General Statistics")
    # st.sidebar.markdown(""" 
    #     - **Total Projects**: 15  
    #     - **Active Researchers**: 20  
    #     - **Published Papers**: 10  
    #     - **Collaborations**: 5  
    # """)
    st.sidebar.markdown("### Research Themes")
    st.sidebar.markdown(""" 
        - **Cognitive City and Urban Analytics**  
        - **Advanced Mobility and Logistics Solutions**  
        - **Human-centric Sustainable Systems**  
        - **Intelligent Logistics and Supply Chain Automation**
    """)