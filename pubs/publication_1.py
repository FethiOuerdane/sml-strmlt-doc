import glob
import streamlit as st
import wget
from PIL import Image
import torch
import cv2
import os
import time
from ultralytics import YOLO  # Import YOLOv8
import base64

# st.set_page_config(layout="wide")

cfg_model_path = 'models/best_roboflow_pretraind.pt'  # Default path to a YOLOv8 model
model = None
confidence = .25


from PIL import Image
import numpy as np

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
                return  # Stop execution and trigger the rerun logic
            else:
                st.error("Incorrect password")
        st.stop()


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def image_input(data_src):
    img_file = None
    if data_src == 'Sample data':
        # get all sample images
        img_path = glob.glob('data/sample_images/*')
        img_slider = st.slider("Select a test image.", min_value=1, max_value=len(img_path), step=1)
        img_file = img_path[img_slider - 1]
    else:
        img_bytes = st.sidebar.file_uploader("Upload an image", type=['png', 'jpeg', 'jpg'])
        if img_bytes:
            img_file = "data/uploaded_data/upload." + img_bytes.name.split('.')[-1]
            Image.open(img_bytes).save(img_file)

    if img_file:
        col1, col2 = st.columns(2)
        with col1:
            st.image(img_file, caption="Model prediction", use_container_width=True)

        with col2:
            img = infer_image(img_file,size=640)  # Pass the image to inference
            st.image(img, caption="Model prediction", use_container_width=True)



def infer_frame(frame, size=640):
    model.conf = st.session_state.confidence
    
    # Perform inference with the model
    results = model(frame, imgsz=size) if size else model(frame)
    result = results[0]

    # Get the bounding boxes
    confidence_threshold = st.session_state.confidence
    boxes = [box for box in result.boxes if box.conf[0].item() >= confidence_threshold]
    selected_classes = model.classes if hasattr(model, 'classes') else list(model.names.keys())

    for box in boxes:
        cls = int(box.cls[0].item())
        if cls not in selected_classes:
            continue  # Skip this box if not in selected classes
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        cls = int(box.cls[0].item())
        label = model.names[cls] if hasattr(model, 'names') else str(cls)

        # Draw box and label on the frame
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    return frame


def infer_image(img_file, size=640):
    # model.conf = st.session_state.confidence
    
    # Check if img_file is a path or image (in case of uploaded image bytes)
    # if isinstance(img_file, str):  # If it's a path, load the image
    #     img = Image.open(img_file)
    # else:  # If it's a byte stream, load the image
    #     img = Image.open(img_file)
    
    # # Convert to RGB if the image has 4 channels (RGBA)
    # if img.mode == 'RGBA':
    #     img = img.convert('RGB')
    
    # Convert to numpy array (if it's a PIL image)
    # img = np.array(img)
    img = cv2.imread(img_file)
    # Perform inference with the model
    # results = model(img, imgsz=size) if size else model(img)
    results = model(img, imgsz=640)[0]  # Get first result

    # Draw results on the image
    annotated_frame = results.plot()
    # Access the first element in results (since it's a list with one object per image/frame)
    # result = results[0]  # This is the detection result for the image
    
    # # Get the bounding boxes (you can also get class labels, confidence, etc.)
    # confidence_threshold = st.session_state.confidence
    # selected_classes = model.classes if hasattr(model, 'classes') else list(model.names.keys())
    # boxes = [box for box in result.boxes if box.conf[0].item() >= confidence_threshold]  # Bounding boxes
    # print(f"Detected {len(boxes)} objects.")
    
    # # Optionally, you can print the first bounding box for debugging
    # if len(boxes) > 0:
    #     print(f"First bounding box: {boxes[0]}")

    # Create a copy of the image to draw the boxes on
    img_with_boxes = annotated_frame.copy()
    
    # Draw bounding boxes (this assumes you have a function to draw boxes, e.g., using OpenCV)
    # for box in boxes:
    #     cls = int(box.cls[0].item())
    #     if cls not in selected_classes:
    #         continue  # Skip this box if not in selected classes
    #     x1, y1, x2, y2 = box.xyxy[0].tolist()  # Extract coordinates (xyxy format)
    #     # You can draw the boxes using OpenCV, or you can render them in another way
    #     cv2.rectangle(img_with_boxes, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Convert to PIL image for Streamlit display
    img_with_boxes_pil = Image.fromarray(img_with_boxes)
    return img_with_boxes_pil
if 'play_video' not in st.session_state:
    st.session_state.play_video = False

def video_input(data_src):
    vid_file = None
    if data_src == 'Sample data':
        vid_file = "data/sample_videos/sample3.mp4"
    else:
        vid_bytes = st.sidebar.file_uploader("Upload a video", type=['mp4', 'mpv', 'avi'])
        if vid_bytes:
            vid_file = "data/uploaded_data/upload." + vid_bytes.name.split('.')[-1]
            with open(vid_file, 'wb') as out:
                out.write(vid_bytes.read())

    if vid_file:
        cap = cv2.VideoCapture(vid_file)
        custom_size = st.sidebar.checkbox("Custom frame size")
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if custom_size:
            width = st.sidebar.number_input("Width", min_value=120, step=20, value=width)
            height = st.sidebar.number_input("Height", min_value=120, step=20, value=height)

        fps = 0
        st1, st2, st3 = st.columns(3)
        with st1:
            st.markdown("## Height")
            st1_text = st.markdown(f"{height}")
        with st2:
            st.markdown("## Width")
            st2_text = st.markdown(f"{width}")
        with st3:
            st.markdown("## FPS")
            st3_text = st.markdown(f"{fps}")

        st.markdown("---")
        output = st.empty()
        prev_time = 0
        curr_time = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                st.write("Can't read frame, stream ended? Exiting ....")
                break
            # frame = cv2.resize(frame, (640, 640))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output_img = infer_frame(frame,size=640)
            output.image(output_img)
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            st1_text.markdown(f"**{height}**")
            st2_text.markdown(f"**{width}**")
            st3_text.markdown(f"**{fps:.2f}**")

        cap.release()


@st.cache_resource  # Cache the model loading function
def load_model(path, device):
    model = YOLO(path)  # Load YOLOv8 model
    model.to(device)
    print("model to ", device)
    return model


@st.cache_resource  # Cache the model download function
def download_model(url):
    model_file = wget.download(url, out="models")
    return model_file


def get_user_model():
    model_src = st.sidebar.radio("Model source", ["file upload", "url"])
    model_file = None
    if model_src == "file upload":
        model_bytes = st.sidebar.file_uploader("Upload a model file", type=['pt'])
        if model_bytes:
            model_file = "models/uploaded_" + model_bytes.name
            with open(model_file, 'wb') as out:
                out.write(model_bytes.read())
    else:
        url = st.sidebar.text_input("model url")
        if url:
            model_file_ = download_model(url)
            if model_file_.split(".")[-1] == "pt":
                model_file = model_file_

    return model_file
# def main():
#     # global variables
#     global model, confidence, cfg_model_path

#     st.title("Smart Mobility and Logistics Dashboard")
#     st.sidebar.title("Settings")

#     # 🌐 External Links
#     if st.button("Learn more about the center"):
#         url = "https://www.example.com"  # Replace with real link
#         st.markdown(f'<a href="{url}" target="_blank">Click here to go to the Smart Mobility Dashboard</a>', unsafe_allow_html=True)

#     if st.button("Check Other Projects"):
#         url = "https://www.example.com"  # Replace with real link
#         st.markdown(f'<a href="{url}" target="_blank">Click here to go to the Smart Mobility Dashboard</a>', unsafe_allow_html=True)

#     # 📄 Published Work - Sidebar Section
#     st.sidebar.markdown("---")
#     st.sidebar.subheader("📄 Published Work")
#     st.sidebar.markdown("""
#     **Title**: *Deep Learning-based Object Detection for Smart Logistics*  
#     **Authors**: A. Researcher, B. Scientist, C. Developer  
#     **Conference**: IEEE Smart Mobility Conf. 2025  
#     🔗 [View Paper](https://your-paper-link.com)
#     """)

#     # 📄 Published Work - Expandable Main Section
#     with st.expander("📄 View Published Research"):
#         st.markdown("""
#         ### Deep Learning-based Object Detection for Smart Logistics  
#         **Authors**: A. Researcher, B. Scientist, C. Developer  
#         **Published in**: IEEE Smart Mobility Conference 2025  
#         🔗 [Read Full Paper](https://your-paper-link.com)  

#         > This dashboard was developed as part of the experimental validation discussed in Section 4 of the paper.
#         """)

#     # Upload model
#     model_src = st.sidebar.radio("Select YOLOv8 weight file", ["Use our demo model 5s", "Use your own model"])
#     if model_src == "Use your own model":
#         user_model_path = get_user_model()
#         if user_model_path:
#             cfg_model_path = user_model_path

#         st.sidebar.text(cfg_model_path.split("/")[-1])
#         st.sidebar.markdown("---")

#     if not os.path.isfile(cfg_model_path):
#         st.warning("Model file not available!!!, please add it to the 'models' folder.", icon="⚠️")
#     else:
#         if torch.cuda.is_available():
#             device_option = st.sidebar.radio("Select Device", ['cpu', 'cuda'], disabled=False, index=0)
#         else:
#             device_option = st.sidebar.radio("Select Device", ['cpu', 'cuda'], disabled=True, index=0)

#         model = load_model(cfg_model_path, device_option)

#         confidence = st.sidebar.slider('Confidence', min_value=0.1, max_value=1.0, value=.45)

#         if st.sidebar.checkbox("Custom Classes"):
#             model_names = list(model.names.values())
#             assigned_class = st.sidebar.multiselect("Select Classes", model_names, default=[model_names[0]])
#             classes = [name for name in assigned_class if name in model.names.values()]
#             model.classes = [list(model.names.values()).index(class_name) for class_name in classes]
#         else:
#             model.classes = list(model.names.keys())

#         st.sidebar.markdown("---")

#         input_option = st.sidebar.radio("Select input type: ", ['image', 'video'])
#         data_src = st.sidebar.radio("Select input source: ", ['Sample data', 'Upload your own data'])

#         if input_option == 'image':
#             image_input(data_src)
#         else:
#             video_input(data_src)


# if __name__ == "__main__":
#     try:
#         main()
#     except SystemExit:
#         pass


def main_page3():
    # global variables
    global model, confidence, cfg_model_path
 # Initialize session state values if not already present
    if "video_frame" not in st.session_state:
        st.session_state.video_frame = 0
    if "play_video" not in st.session_state:
        st.session_state.play_video = False
    # st.title("Object Recognition Dashboard")
    image_path = "data/uav.png"
    image_base64 = get_base64_of_bin_file(image_path)
    image_html = f'<img src="data:image/png;base64,{image_base64}" width="50" style="margin-right:10px;">'

    # st.markdown(
    #     f"""
    #     <div style="display: flex; align-items: center;">
    #         {image_html}
    #         <h1 style="margin: 0;">Smart Mobility and Logistics Dashboard V0.2</h1>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    # st.title("Smart Mobility and Logistics Dashboard V0.3")
    # st.sidebar.image("data/ircsml.png", width=300)
    st.sidebar.title("Settings")
    # Add a button that redirects to a URL when clicked
    # if st.button("Learn more about the center"):
    #     url = "https://www.example.com"  # Replace this URL with the relevant one
    #     st.markdown(f'<a href="{url}" target="_blank">Click here to go to the Smart Mobility Dashboard</a>', unsafe_allow_html=True)
    # Add a button that redirects to a URL when clicked
    # if st.button("Check Other Projects"):
    #     url = "https://www.example.com"  # Replace this URL with the relevant one
    #     st.markdown(f'<a href="{url}" target="_blank">Click here to go to the Smart Mobility Dashboard</a>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.subheader("📄 Published Work")
    st.sidebar.markdown("""
    **Title**: *Technical Aspects of Deploying UAV and Ground Robots for Intelligent Logistics Using YOLO on Embedded Systems
*  
    **Authors**: Wissem Dilmi,Sami El Ferik ,Fethi Ouerdane ,Mustapha K. Khaldi  andAbdul-Wahid A. Saif
    **Conference**: MDPI Sensors. 2025  
    🔗 [View Paper](https://www.mdpi.com/1424-8220/25/8/2572)
    """)
    #  st.sidebar.image("data/uav.png", caption="Published Work", use_column_width=True)

  # -----------------------------
    # 📄 Expandable Paper Info (Main)
    # -----------------------------
    with st.expander("📄 View Published Research", expanded=True):
        st.markdown("""
        <div style="background-color: #1a1a2e	; padding: 15px; border-radius: 10px;">
            <h4 style="color:#e0e7ff">Technical Aspects of Deploying UAV and Ground Robots for Intelligent Logistics Using YOLO on Embedded Systems</h4>
            <p><b>Authors:</b> Wissem Dilmi,Sami El Ferik ,Fethi Ouerdane ,Mustapha K. Khaldi  andAbdul-Wahid A. Saif </p>
            <p><b>Published in:</b> <i>MDPI Sensors 2025 </i></p>
            <p>📖 <a href="https://www.mdpi.com/1424-8220/25/8/2572" target="_blank">Read Full Paper</a></p>
                    <p><h4 style="color:#e0e7ff">Abstract:</h4>
Automation of logistics enhances efficiency, reduces costs, and minimizes human error. Image processing—particularly vision-based AI—enables real-time tracking, object recognition, 
                            and intelligent decision-making, thereby improving supply chain resilience.
                             This study addresses the challenge of deploying deep learning-based object detection 
                            on resource-constrained embedded platforms, such as NVIDIA Jetson devices on UAVs and ground robots,
                             for real-time logistics applications. Specifically, we provide a comprehensive comparative analysis of YOLOv5 and YOLOv8,
                             evaluating their performance in terms of inference speed, accuracy, and dataset-specific metrics using both the
                             Common Objects in Context (COCO) dataset and a novel, custom logistics dataset tailored for aerial and ground-based
                             logistics scenarios. A key contribution is the development of a user-friendly graphical user interface (GUI) 
                            for selective object visualization, enabling dynamic interaction and real-time filtering of detection results—significantly
                             enhancing practical usability. Furthermore, we investigate and compare deployment strategies in both Python 3.9 and C# 
                    (ML. NET v3 and .NET Framework 7) environments, highlighting their respective impacts on performance and scalability. This research offers
                     valuable insights and practical guidelines for optimizing real-time object detection deployment on embedded platforms in UAV- 
                    and ground robot-based logistics, with a focus on efficient resource utilization and enhanced operational effectiveness</p>
        </div>
        """, unsafe_allow_html=True)


#     with st.expander("📄 View Published Research",expanded=True):
#         st.markdown("""
# ### Technical Aspects of Deploying UAV and Ground Robots for Intelligent Logistics Using YOLO on Embedded Systems

# **Authors**: A. Researcher, B. Scientist  
# **Published in**: MDPI Sensors 2025 

# 🔗 [Read Full Paper](https://your-paper-link.com)  

# > 🧪 This dashboard was developed as part of the experimental validation described in Section 4 of the paper.
#         """)

    # upload model
    model_src = st.sidebar.radio("Select YOLOv8 weight file", ["Use our demo model 5s", "Use your own model"])
    # URL, upload file (max 200 mb)
    if model_src == "Use your own model":
        user_model_path = get_user_model()
        if user_model_path:
            cfg_model_path = user_model_path

        st.sidebar.text(cfg_model_path.split("/")[-1])
        st.sidebar.markdown("---")

    # check if model file is available
    if not os.path.isfile(cfg_model_path):
        st.warning("Model file not available!!!, please added to the model folder.", icon="⚠️")
    else:
        # device options
        if torch.cuda.is_available():
            device_option = st.sidebar.radio("Select Device", ['cpu', 'cuda'], disabled=False, index=0)
        else:
            device_option = st.sidebar.radio("Select Device", ['cpu', 'cuda'], disabled=True, index=0)

        # load model
        model = load_model(cfg_model_path, device_option)

        # confidence slider
        if 'confidence' not in st.session_state:
            st.session_state.confidence = 0.45

        st.session_state.confidence = st.sidebar.slider('Confidence', min_value=0.1, max_value=1.0, value=st.session_state.confidence)
        confidence = st.session_state.confidence  # use this in inference

        if st.sidebar.checkbox("Custom Classes"):
            model_names = list(model.names.values())  # List of class names
            assigned_class = st.sidebar.multiselect("Select Classes", model_names, default=[model_names[0]])
            
            # Map class names to indices
            classes = [name for name in assigned_class if name in model.names.values()]
            model.classes = [list(model.names.values()).index(class_name) for class_name in classes]
        else:
            model.classes = list(model.names.keys())

        st.sidebar.markdown("---")

        # input options
        input_option = st.sidebar.radio("Select input type: ", ['image', 'video'])

        # input src option
        data_src = st.sidebar.radio("Select input source: ", ['Sample data', 'Upload your own data'])

        if input_option == 'image':
            image_input(data_src)
        else:
            video_input(data_src)


if __name__ == "__main__":
    try:
        password_protect()
        main_page3()
    except SystemExit:
        pass
