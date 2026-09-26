import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import time

# ---------------- Page Setup ----------------
st.set_page_config(page_title="PrivacyLens Prototype", page_icon="🛡️", layout="wide")

# ---------------- Custom Styling ----------------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #e0f7fa, #f1f8e9);
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        color: #1565c0;
        text-shadow: 1px 1px 2px #90caf9;
    }
    .stButton>button {
        background-color: #1565c0;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: 600;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("PrivacyLens Prototype 🛡️")
st.write("Upload an image — faces will be blurred automatically, and you’ll get privacy insights.")

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Options")
show_score = st.sidebar.checkbox("Show Privacy Risk Score", value=True)
enable_download = st.sidebar.checkbox("Enable Download Safe Copy", value=True)
show_faces = st.sidebar.checkbox("Show Face Count", value=True)
show_tips = st.sidebar.checkbox("Show Privacy Tips", value=True)

# ---------------- Upload Section ----------------
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    # Display original image
    col1, col2 = st.columns(2)
    col1.image(image, caption="Original Image", use_container_width=True)

    # Progress bar
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # Convert to OpenCV format
    img_cv = np.array(image)

    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Blur detected faces
    for (x, y, w, h) in faces:
        roi = img_cv[y:y+h, x:x+w]
        roi_blur = cv2.GaussianBlur(roi, (51, 51), 30)
        img_cv[y:y+h, x:x+w] = roi_blur

    # Display blurred image
    col2.image(img_cv, caption="Blurred Image", use_container_width=True)

    # ---------------- Extra Features ----------------
    if show_faces:
        st.info(f"🔍 Faces detected and blurred: {len(faces)}")

    if show_score:
        score = min(len(faces) * 20, 100)
        st.metric("Privacy Risk Score", f"{score}/100")

    if enable_download:
        buf = io.BytesIO()
        Image.fromarray(img_cv).save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="📥 Download Safe Copy",
            data=byte_im,
            file_name="safe_image.png",
            mime="image/png"
        )

    if show_tips:
        st.subheader("💡 Privacy Tips")
        st.markdown("""
        - Avoid sharing images with visible ID cards or documents.  
        - Blur faces of others before posting publicly.  
        - Remove location metadata from photos before uploading.  
        - Use PrivacyLens for quick protection!
        """)

    st.success("✅ Prototype upgraded! Faces blurred, score calculated, and download ready.")


