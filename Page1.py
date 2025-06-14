import streamlit as st

# Page 1 layout
def page1():
    # st.title("Recent Work in IRC SML")
   
    
    # Example: simple input and display
 # -----------------------------
    # Main Content: Publications Overview
    # -----------------------------

# st.set_page_config(page_title="Publications", layout="wide")

# Define a list of publications
    publications = [
        {
            "id": "publication_1",
            "title": "Data Fusion for Visual Navigation: Robust Robot Trajectory from Stereo-VIO-GPS",
            "authors": "Wissem Dilmi, Sami El Ferik, Fethi Ouerdane, Mustapha K. Khaldi, Abdul-Wahid A. Saif",
            "abstract": "This study addresses deploying deep learning-based object detection on UAVs and ground robots for real-time logistics applications, including a comparative analysis of YOLOv5 and YOLOv8.",
            "link": "https://www.mdpi.com/1424-8220/25/8/2572",
            "image": "data/images/poster_stereo.png"
        },
    
        {
        "id": "publication_3",
        "title": "Technical Aspects of Deploying UAV and Ground Robots for Intelligent Logistics Using YOLO on Embedded Systems",
        "authors": "Wissem Dilmi, Sami El Ferik, Fethi Ouerdane, Mustapha K. Khaldi, Abdul-Wahid A. Saif",
        "abstract": "Automation of logistics enhances efficiency, reduces costs, and minimizes human error. Image processing—particularly vision-based AI—enables real-time tracking, object recognition, and intelligent decision-making, thereby improving supply chain resilience. This study addresses the challenge of deploying deep learning-based object detection on resource-constrained embedded platforms, such as NVIDIA Jetson devices on UAVs and ground robots, for real-time logistics applications. Specifically, we provide a comprehensive comparative analysis of YOLOv5 and YOLOv8, evaluating their performance in terms of inference speed, accuracy, and dataset-specific metrics using both the Common Objects in Context (COCO) dataset and a novel, custom logistics dataset tailored for aerial and ground-based logistics scenarios. A key contribution is the development of a user-friendly graphical user interface (GUI) for selective object visualization, enabling dynamic interaction and real-time filtering of detection results—significantly enhancing practical usability. Furthermore, we investigate and compare deployment strategies in both Python 3.9 and C# (ML. NET v3 and .NET Framework 7) environments, highlighting their respective impacts on performance and scalability. This research offers valuable insights and practical guidelines for optimizing real-time object detection deployment on embedded platforms in UAV- and ground robot-based logistics, with a focus on efficient resource utilization and enhanced operational effectiveness.",
        "link": "https://www.mdpi.com/1424-8220/25/8/2572",
        "image": "data/images/sensors_tech_dilmi.png"
         },
         {
        "id": "publication_4",
        "title": "Variations in EEG Signals Across Different Brain Regions during Motor Imagery and Execution Tasks",
        "authors": "Maged S. Al-Quraishi, Syed Saad Azhar Ali, Haitham H. Saleh, Mahmoud S. Abouomar",
        "abstract": "Electroencephalography techniques used in Brain computer interface to control external devices. Different BCI applications based on EEG were reported such as controlling the robotic arm, computer courser or gaming. Motor execution and motor imagery are both used as EEG input control signals to control the peripheral devices. However, some applications are required to control the peripheral devices using thoughts (motor imagery) only. In this case, differentiation between actual and imagery action is crucial. In this work, the investigation of the changes of the power spectrum of the EEG bands including alpha and beta bands in the different brain regions. The public dataset recorded from 60 subjects in different movements task were used. Th Alpha (8-12 Hz) and Beta (13-30 Hz) were extracted from the recorded EEG signals. After the preprocessing, the power spectrum was calculated for each band in four brain regions including central sulcus, motor cortex, sensorimotor cortex. The results reveal that significant differences were found in the area in the alpha and beta bands in the motor cortex and sensorimotor cortex. while in the central sulcus the differences were insignificant. The results of this study are still preliminary and more investigation using different EEG quantities and features are required. Additionally, this study needs to be validated with another dataset. © 2024 The Authors. Published by ELSEVIER B.V.",
        "link": "https://www.scopus.com/inward/record.uri?eid=2-s2.0-105001492739&doi=10.1016%2fj.trpro.2025.03.099&partnerID=40&md5=69d397e830b539416651ab4145e2cfbf",
        "image": "data/images/eeg_motor_imagery.png"
    } ,
    {
            "id": "publication_2",
            "title": "VISUAL SERVOING TECHNIQUES FOR SPECULAR REFLECTION MITIGATION IN UAV-BASED METER INSPECTION",
            "authors": "Alice Johnson, Bob Smith, Carol White",
            "abstract": "This paper explores how AI-driven real-time object detection can improve logistics efficiency and automation across various industries, focusing on practical deployment on embedded systems.",
            "link": "https://www.example.com/paper2",
            "image": "data/images/poster_reflection.png"
        },
        {
        "id": "publication_4",
        "title": "Stereo Visual Matching for UAV Navigation: Multi-Channel Disparity Map-Based Trajectory Estimation",
        "authors": "Wissem Dilmi, Sami El-Ferik, Abdul-Wahid A. Saif",
        "abstract": "Stereo vision and matching constitute a deeply researched sector within computer vision, particularly in the domains of robot and drone navigation, augmented reality, and automotive applications. Stereo matching performs more effectively in scenarios without radiometric variations compared to those with such variations present. This study delves into stereo matching techniques and proposes novel frameworks aimed at enhancing precise localization and velocity measurement of UAVs within defined boundaries. The primary focus lies on refining the accuracy of the resulting disparagement map, achieved through three key phases: pre-processing, stereo matching, and post-processing. Initially, input images undergo pre-processing using NMHE to mitigate radiometric variations. Subsequently, various features are extracted from both images during the second phase. Finally, the disparagement map undergoes post-processing to eliminate minor artifacts. Experimental findings demonstrate that the proposed modifications have significantly enhanced the performance of state-of-the-art local stereo matching algorithms and bolstered their resilience against radiometric changes.",
        "link": "https://doi.org/10.1109/SSD64182.2025.10989917",
        "image": "data/images/uav_stereo_matching.png"
    }

        # Add more...
    ]


    st.title("📚 Recent Research Work")
    st.write("A List of Recent Academic research projects and publications.")
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

            # if st.button(f"📖 Read More: {pub['id']}", key=pub["id"]):
            #     st.session_state.page = pub["id"]

        st.markdown("---")
