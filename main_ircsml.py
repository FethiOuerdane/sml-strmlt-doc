import streamlit as st
import os
import importlib.util
st.set_page_config(page_title="Smart Mobility and Logistics Dashboard", page_icon="🚀", layout="wide")

from Home import home_page
from Page1 import page1
from Page2 import page2
# from pubs.publication_1 import main_page3
# from Page_papers import page_paper
from pubs.docs import main_docs
# def load_page(page_name):
#     # Build the file path for the publication script
#     page_path = os.path.join('pages', f'{page_name}.py')
    
#     if os.path.exists(page_path):
#         # Load the module dynamically
#         spec = importlib.util.spec_from_file_location(page_name, page_path)
#         page_module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(page_module)  # Execute the module
#     else:
#         st.error(f"Page {page_name} not found!")

def password_protect():
    PASSWORD = "ircsml"  # 🔐 Change this to your preferred password

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "rerun" not in st.session_state:
        st.session_state.rerun = False

    # Use this flag to trigger rerun logic, not the deprecated rerun method
    if st.session_state.rerun:
        st.session_state.rerun = False
        return  # This will stop further execution and effectively "rerun" the page

    if not st.session_state.authenticated:
        st.title("🔐 Login Required")
        pwd = st.text_input("Enter password", type="password")
        if st.button("Login"):
            if pwd == PASSWORD:
                st.session_state.authenticated = True
                st.session_state.rerun = True  # Set rerun flag to True after login
                st.stop()  # Stop execution and trigger the rerun logic
            else:
                st.error("Incorrect password")
        st.stop()

def main():
    st.sidebar.image("data/ircsml.png", width=300)

    # Sidebar Center Info
    if st.sidebar.button("Learn More About the Center and Administration"):
        st.sidebar.markdown("""
        ## Center Overview
        This research center focuses on advancing the fields of smart mobility and logistics by leveraging state-of-the-art AI and robotic systems. Our goal is to contribute to sustainable and efficient transportation solutions using the latest advancements in deep learning and embedded systems.
        
        ### Administration
        - **Director**: Prof. Sami Elferik 
        - **Contact**: selferik@kfupm.edu.sa
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.title("Navigation")

    # Main page selection (including Publications as a special page)
    pages = {
        "About the Center": home_page,
        "Recent Work in the Center": page1,
        # "Concept Reviews": page2,
        "Research Docs and Materials": main_docs,
        # "📖 Publications": "PUBLICATIONS"  # special flag
    }

    # Sidebar main navigation
    selection = st.sidebar.radio("Go to", list(pages.keys()), key="main_nav")

    st.sidebar.markdown("---")

    # Publications sub-pages
    # publication_pages = {
    #     "Technical Aspects of Deploying UAV and Ground Robots for Intelligent Logistics Using YOLO on Embedded Systems": main_page3,
    #     "List of Published Papers": page_paper,
    # }

    # Handle conditional rendering
    if selection != "📖 Publications":
        # Call normal page
        page = pages[selection]
        page()
    # else:
    #     # Publications-specific interface
    #     st.sidebar.header("Select a Paper")
    #     pub_selection = st.sidebar.radio("Choose publication:", list(publication_pages.keys()), key="pub_nav")
    #     selected_func = publication_pages[pub_selection]
    #     selected_func()

    st.sidebar.markdown("---")

if __name__ == "__main__":
    try:
        password_protect()  # Make sure the user is logged in
        main()  # Run the main function
    except SystemExit:
        pass
