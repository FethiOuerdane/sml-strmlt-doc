import streamlit as st
import json
# Page 1 layout
def page1():
    # st.title("Recent Work in IRC SML")
   
    
    # Example: simple input and display
 # -----------------------------
    # Main Content: Publications Overview
    # -----------------------------

# st.set_page_config(page_title="Publications", layout="wide")

# Define a list of publications
    

    st.title("📚 Recent Research Work")
    st.write("A List of Recent Academic research projects and publications.")
    with open('data/publications.json', 'r', encoding='utf-8') as f:
        publications = json.load(f)
        for pub in publications:
            col1, col2 = st.columns([1, 3])

            # Left column: image
            with col1:
                st.image(pub["image"], use_container_width=True)

            # Right column: details
            with col2:
                st.markdown(f"### {pub['title']}")
                st.markdown(f"**Authors:** {pub['authors']}")
                st.markdown(f"**Abstract:** {pub['abstract']}")
                st.markdown(f"🔗 [Read Full Paper]({pub['link']})")

            
            st.markdown("---")
