import streamlit as st
import base64
import base64
import os
# Utility: Convert image to base64 for embedding
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
def pdf_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Folder containing your PDFs
PDF_FOLDER = "concept_reviews"
DOC_PDF_FOLDER = "data/product_docs"
# Utility to convert filename to pretty title
def prettify_filename(filename):
    name = filename.replace(".pdf", "")  # remove extension
    parts = name.split("_")[2:]  # remove numeric prefix like 00001_
    title = " ".join(word.capitalize() for word in parts)
    return title
def main_docs():
    # Set wide layout and page config
    # st.set_page_config(layout="wide", page_title="Project Documentation", page_icon="📘")
    st.title("Smart Mobility and Logistics — Lab Documentations")
    # Header with logo and title
    # logo_path = "data/ircsml.png"  # Change to your logo path
    # logo_base64 = get_base64_image(logo_path)
    st.image("data/images/lab.jpg")
    # st.image("data/images/guide_tabs.png")
    with st.expander("🧠 Information Tip", expanded=True):
        st.image("data/images/guide_tabs.png")
    # st.subheader("🎯 Objectives")
    # st.markdown(""" 
    # - Develop a robust, real-time object detection system
    # - Deploy models on resource-constrained embedded systems (e.g., Jetson Nano)
    # - Evaluate YOLOv5 vs YOLOv8 for real-world logistics scenarios
    # """)

    # ---------------- Project Features ---------------- #
    # st.subheader("🧰 Features Overview")
    # cols = st.columns(3)

    # features = [
    #     ("🚁 UAV & Ground Robot Integration", "Real-time deployment on aerial and mobile units."),
    #     ("🎯 YOLOv8 Inference", "Supports live inference and dynamic class selection."),
    #     ("🖥️ Embedded Optimization", "Tested on Jetson Nano for edge processing."),
    # ]

    # for col, (title, desc) in zip(cols, features):
    #     col.markdown(f"### {title}")
    #     col.markdown(desc)

    # Inject CSS to style tabs
 
    tabd, tabdd = st.tabs(["📘 Lab Products Docs", "📖 General Concept Reviews (PDF)"])

    with tabd:
        st.subheader("🛠️ Select a Quanser Product")
        
        products = {
            "QBot Platform": {
                "description": "QBot Plateform is an autonomous ground robot designed for teaching and research.",
                "doc_folder_name":"Qbot_Platform",
                "image_path":"QBotPlatform.jpg",
                "resource_link":"https://youtu.be/w5RFFDtPaKM",
                "tutorial": [
                    "Power on the QBot 2e and ensure WiFi connection.",
                    "Open QUARC Simulink model in MATLAB.",
                    "Deploy the model to QBot using QUARC > Build & Run."
                ],
                "code": [
                    "model_name = 'qbot2e_navigation'",
                    "quarc_run(model_name)"
                ],
                "links":{
                "Download Files related to ": "https://drive.google.com/drive/folders/1S3b5eHAwRx1ZKIQ3EWYmu3Vnj3J5-sLO?usp=sharing",
                # "GitHub": "https://github.com",
                # "OpenAI": "https://www.openai.com"
            },
                "resources": {
                    "Product Page": "https://www.quanser.com/products/qbot-2e/",
                    "QUARC Docs": "https://www.quanser.com/products/quarc-real-time-control-software/"
                }
            },
            "QDrone 2": {
                "description": "QDrone is a quadrotor for research in aerial robotics and control.",
                "doc_folder_name":"Qdrone2",
                "image_path":"qdrone2.jpg",
                "resource_link":"https://youtu.be/lxrts2ohqok",
                "tutorial": [
                    "Connect to QDrone via WiFi.",
                    "Open the QDrone flight control model.",
                    "Deploy from Simulink using QUARC.",
                    "Ensure flight safety protocols."
                ],
                "code": [
                    "model_name = 'qdrone_flight_control'",
                    "quarc_run(model_name)"
                ],
                "links":{
                "Download Files related to ": "https://drive.google.com/drive/folders/1VKgANHKBBXdbtkxYbj7AKo6BC-NcNKAn?usp=sharing",
                # "GitHub": "https://github.com",
                # "OpenAI": "https://www.openai.com"
            },
                "resources": {
                    "Product Page": "https://www.quanser.com/products/qdrone-2/",
                    "Flight Control Example": "https://www.quanser.com/products/qdrone-2/#example"
                }
            }
        }

        # Dropdown to select product
        selected_product = st.selectbox("Choose a Quanser Product:", list(products.keys()))
        product_data = products[selected_product]
        st.image(os.path.join("data/images/", product_data["image_path"]),width=320)
        st.markdown(f"### 🔍 {selected_product}")
        st.markdown(product_data["description"])

        # ---------------- Product Tabs ---------------- #
        tab1, tab2, tab3 = st.tabs(["📘 Tutorial", "💻 Code and Files", "🔗 Resources and Training"])
       
        with tab1:
           
        
            st.markdown(f"#### {selected_product} General Information")
            fld = os.path.join(DOC_PDF_FOLDER,product_data["doc_folder_name"])
            print(fld)
            pdf_files = [f for f in os.listdir(fld) if f.endswith(".pdf")]
            
            # Create a mapping from pretty name to filename
            pretty_to_file = {
                prettify_filename(f): f for f in pdf_files
            }
            print(pretty_to_file)
            # Dropdown for user to pick a PDF
            selected_title = st.selectbox("📚 Select a Product related topic to review PDF:", sorted(pretty_to_file.keys()))

            # Get the corresponding file path
            selected_file = pretty_to_file[selected_title]
            pdf_path = os.path.join(fld, selected_file)

            # Display the selected PDF
            st.markdown(f"### 📄 {selected_title}")

            pdf_base64 = pdf_to_base64(pdf_path)

            st.markdown(
                f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="1100" type="application/pdf"></iframe>',
                unsafe_allow_html=True
            )

            # for i, step in enumerate(product_data["tutorial"], start=1):
            #     st.markdown(f"**Step {i}:** {step}")

        with tab2:
            st.markdown("#### MATLAB / Simulink Code files")
            # for line in product_data["code"]:
            #     st.code(line, language="matlab")
            
            # Example links and labels
            links = product_data["links"]
            # {
            #     "Download Files related to ": "https://drive.google.com/drive/folders/1VKgANHKBBXdbtkxYbj7AKo6BC-NcNKAn?usp=sharing",
            #     # "GitHub": "https://github.com",
            #     # "OpenAI": "https://www.openai.com"
            # }

            # Loop to create buttons that look like links
            for label, url in links.items():
                st.markdown(f"""
                    <a href="{url}" target="_blank">
                        <button style="margin: 5px;">{label}{selected_product}</button>
                    </a>
                """, unsafe_allow_html=True)    

        with tab3:
            st.markdown("#### External Links & Documentation")
            st.video( product_data["resource_link"])
            for name, link in product_data["resources"].items():
                st.markdown(f"- [{name}]({link})")
            # ---------------- Footer ---------------- #
            st.markdown("---")
            st.markdown("© 2025 Smart Mobility Research Group | Contact: `selferik@kfupm.edu.sa`", unsafe_allow_html=True)

    with tabdd:
        st.markdown("#### Concept Reviews: Select from List")
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
        # for line in product_data["code"]:
        #     st.code(line, language="matlab")
    
    
    # ---------------- Architecture ---------------- #
    # with st.expander("🧠 System Architecture Diagram", expanded=False):
    #     st.image("data/sample_images/packages.png", caption="System Design and Flow")  # Replace with your diagram
        
   # ---------------- Quanser Product Selection ---------------- #
    

# Run the app
if __name__ == "__main__":
    main_docs()
