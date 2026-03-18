import streamlit as st
import requests
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Land Type Classifier for Autonomous Systems",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling
st.markdown("""
    <style>
        /* Main background and text */
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Hide Streamlit footer and header */
        footer {visibility: hidden;}
        
        /* Title styling */
        .title-container {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        
        .title-container h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            color: rgba(255,255,255,0.9);
            margin-top: 0.5rem;
            font-size: 1.1rem;
        }
        
        /* Upload section */
        .upload-container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 2px dashed #667eea;
            text-align: center;
        }
        
        /* Image preview */
        .image-container {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Prediction result */
        .prediction-container {
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            color: white;
            text-align: center;
            margin-top: 1rem;
        }
        
        .prediction-label {
            font-size: 0.9rem;
            font-weight: bold;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .prediction-text {
            font-size: 2rem;
            font-weight: bold;
            margin-top: 0.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 32px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
        }
        
        /* Info boxes */
        .info-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .info-text {
            margin: 0;
            font-size: 0.95rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="title-container">
        <h1>🖼️ Land Type Classifier for Autonomous Systems</h1>
        <p class="subtitle">AI-Powered Scene Recognition</p>
    </div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📤 Upload Your Image")
    st.markdown("""
    <div class="info-box">
        <p class="info-text">✓ Supports JPG, PNG, JPEG formats<br>✓ Max file size: 200MB<br>✓ Quick AI predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )

with col2:
    if uploaded_file is not None:
        st.markdown("### 👁️ Image Preview")
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        try:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True, output_format="auto")
        except:
            st.error("Error loading image")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("### 👁️ No Image Selected")
        st.info("👈 Upload an image to get started!")

# Prediction section
if uploaded_file is not None:
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        predict_button = st.button("🚀 Classify Image", use_container_width=True)
    
    if predict_button:
        with st.spinner("🔄 Analyzing image... This may take a moment"):
            try:
                # Send to FastAPI
                files = {"file": uploaded_file.getvalue()}
                response = requests.post("http://127.0.0.1:8000/predict/", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get('prediction', 'Unknown')
                    confidence = result.get('confidence', 'N/A')
                    
                    # Display result
                    st.markdown(f"""
                        <div class="prediction-container">
                            <p class="prediction-label">Classification Result</p>
                            <p class="prediction-text">{prediction}</p>
                            <p style="margin-top: 1rem; font-size: 1.1rem; opacity: 0.95;">Confidence: {confidence}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Success celebration
                    st.balloons()
                else:
                    st.error("❌ Error: Could not classify image. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Make sure the FastAPI server is running on http://127.0.0.1:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: gray; padding: 1rem;">
        <p>🚀 Powered by Deep Learning | TensorFlow & FastAPI</p>
    </div>
""", unsafe_allow_html=True)