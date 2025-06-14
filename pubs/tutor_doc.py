import streamlit as st

# Sample data dictionary (replace or load from JSON/YAML/DB)
TOOLS = {
    "Streamlit": {
        "description": "Streamlit is an open-source Python library for creating web apps for data science and ML.",
        "tutorial": [
            "Install Streamlit using `pip install streamlit`.",
            "Create a new Python file `app.py`.",
            "Add Streamlit code: `st.write('Hello World')`.",
            "Run the app: `streamlit run app.py`."
        ],
        "code": [
            "import streamlit as st",
            "st.title('My First Streamlit App')",
            "st.write('Welcome to the tutorial!')"
        ],
        "resources": {
            "Official Docs": "https://docs.streamlit.io/",
            "GitHub Repo": "https://github.com/streamlit/streamlit",
            "YouTube Intro": "https://www.youtube.com/watch?v=JwSS70SZdyM"
        }
    },
    "Docker": {
        "description": "Docker is a tool designed to make it easier to create, deploy, and run applications using containers.",
        "tutorial": [
            "Install Docker Desktop.",
            "Create a `Dockerfile` in your project directory.",
            "Build the Docker image: `docker build -t myapp .`.",
            "Run the container: `docker run myapp`."
        ],
        "code": [
            "# Dockerfile",
            "FROM python:3.10",
            "COPY . /app",
            "WORKDIR /app",
            "RUN pip install -r requirements.txt",
            "CMD ['python', 'app.py']"
        ],
        "resources": {
            "Official Docs": "https://docs.docker.com/",
            "Docker Hub": "https://hub.docker.com/",
            "Tutorial Video": "https://www.youtube.com/watch?v=3c-iBn73dDE"
        }
    }
}

# --- Streamlit App UI ---
st.title("📚 Docs & Tutorials Platform")

# Sidebar selector
selected_tool = st.sidebar.selectbox("Choose a Tool/Product:", list(TOOLS.keys()))

# Load selected tool data
tool_data = TOOLS[selected_tool]

st.subheader(f"🔧 {selected_tool}")
st.markdown(tool_data["description"])

# Tabs for content
tab1, tab2, tab3 = st.tabs(["📝 Tutorial", "💻 Code", "🔗 Resources"])

with tab1:
    st.markdown("### Step-by-Step Tutorial")
    for i, step in enumerate(tool_data["tutorial"], start=1):
        st.markdown(f"**Step {i}:** {step}")

with tab2:
    st.markdown("### Code Snippets")
    for line in tool_data["code"]:
        st.code(line, language="python")

with tab3:
    st.markdown("### Resources & Links")
    for name, link in tool_data["resources"].items():
        st.markdown(f"[{name}]({link})")

