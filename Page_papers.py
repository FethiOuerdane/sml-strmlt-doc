import streamlit as st
import streamlit.components.v1 as components
import base64
import os
# Page 2 layout
def pdf_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Folder containing your PDFs
PDF_FOLDER = "published_papers"
# Utility to convert filename to pretty title
def prettify_filename(filename):
    name = filename.replace(".pdf", "")  # remove extension
    parts = name.split("_")[2:]  # remove numeric prefix like 00001_
    title = " ".join(word.capitalize() for word in parts)
    return title

def page_paper():
    st.title("Published Papers on IRC SML")
    # st.write("This is the second page with some charts.")
    
    # Example: Plot a simple chart using random data
    # import numpy as np
    # import matplotlib.pyplot as plt
    # pdf_file = "concept_reviews/00001_concept_review_geometric_lateral_control.pdf"
    # st.markdown(f'<a href="{pdf_file}" target="_blank">Open {pdf_file}</a>', unsafe_allow_html=True)
    # pdf_base64 = pdf_to_base64("concept_reviews/00001_concept_review_geometric_lateral_control.pdf")

    # df_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="800" height="1000" type="application/pdf"></iframe>'

    # st.markdown(df_display, unsafe_allow_html=True)
    # x = np.linspace(0, 10, 100)
    # y = np.sin(x)
    
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # st.pyplot(fig)
    # Get all PDFs in the folder
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    # Create a mapping from pretty name to filename
    pretty_to_file = {
        prettify_filename(f): f for f in pdf_files
    }

    # Dropdown for user to pick a PDF
    selected_title = st.selectbox("📚 Select a Concept Review PDF:", sorted(pretty_to_file.keys()))

    # Get the corresponding file path
    selected_file = pretty_to_file[selected_title]
    pdf_path = os.path.join(PDF_FOLDER, selected_file)

    # Display the selected PDF
    st.markdown(f"### 📄 {selected_title}")

    pdf_base64 = pdf_to_base64(pdf_path)

    st.markdown(
        f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="1100" type="application/pdf"></iframe>',
        unsafe_allow_html=True
    )
