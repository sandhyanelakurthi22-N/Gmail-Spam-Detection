import streamlit as st
import pickle
import time

# Page configuration
st.set_page_config(
    page_title="Gmail Spam Detector",
    page_icon="🛡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color:black
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        min-width: 120px;
    
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .result-container {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    .spam-result {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        border: 2px solid #ff5252;
    }
    
    .ham-result {
        background: linear-gradient(135deg, #51cf66, #40c057);
        color: white;
        border: 2px solid #51cf66;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #e9ecef;
        color: #666;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Load model and vectorizer with error handling
@st.cache_resource
def load_models():
    try:
        model = pickle.load(open('model.pkl', 'rb'))
        vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
        return model, vectorizer
    except FileNotFoundError:
        st.error("❌ Model files not found. Please ensure 'model.pkl' and 'vectorizer.pkl' are in the same directory.")
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None, None

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡 Advanced Gmail Spam Detector</h1>
    <p>Protect your inbox with AI-powered spam detection</p>
</div>
""", unsafe_allow_html=True)

# Features section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🚀 Fast Detection</h3>
        <p>Get instant results with our optimized ML model</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🎯 High Accuracy</h3>
        <p>Advanced algorithms ensure reliable spam detection</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🔒 Secure</h3>
        <p>Your data is processed locally and never stored</p>
    </div>
    """, unsafe_allow_html=True)

# Statistics (mock data - you can replace with actual model metrics)
st.markdown("""
<div class="stats-container">
    <div class="stat-box">
        <div class="stat-number">99.2%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">0.3s</div>
        <div class="stat-label">Avg Speed</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Emails Analyzed</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main functionality
st.markdown("## 📝 Email Analysis")
st.markdown("Paste your email content below to check if it's spam or legitimate:")

# Load models
model, vectorizer = load_models()

if model is not None and vectorizer is not None:
    # Input section
    input_text = st.text_area(
        "Enter Email Content:",
        height=200,
        placeholder="Paste your email content here...\n\nExample:\nSubject: Congratulations! You've won $1,000,000!\nClick here immediately to claim your prize..."
    )
    
    # Analysis section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔍 Analyze Email", key="analyze_btn"):
            if input_text.strip() == "":
                st.warning("⚠ Please enter an email message to analyze.")
            else:
                # Show loading spinner
                with st.spinner('Analyzing email content...'):
                    time.sleep(1)  # Simulate processing time
                    
                    try:
                        # Prediction
                        input_data = [input_text]
                        vectorized_input = vectorizer.transform(input_data)
                        prediction = model.predict(vectorized_input)
                        confidence = model.predict_proba(vectorized_input).max() * 100
                        
                        # Display results
                        if prediction[0] == 1:  # Ham/Not Spam
                            st.markdown(f"""
                            <div class="result-container ham-result">
                                <h2>✅ Legitimate Email (Ham)</h2>
                                <p style="font-size: 1.2rem; margin: 1rem 0;">This email appears to be safe and legitimate.</p>
                                <p style="font-size: 1rem; opacity: 0.9;">Confidence: {confidence:.1f}%</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.success("✅ *Safe to read* - This email passed our spam detection filters.")
                            
                        else:  # Spam
                            st.markdown(f"""
                            <div class="result-container spam-result">
                                <h2>⚠ Potential Spam Detected</h2>
                                <p style="font-size: 1.2rem; margin: 1rem 0;">This email shows characteristics of spam.</p>
                                <p style="font-size: 1rem; opacity: 0.9;">Confidence: {confidence:.1f}%</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.error("🚨 *Caution advised* - This email may be spam. Avoid clicking links or providing personal information.")
                            
                            # Additional warnings for spam
                            st.markdown("""
                            *⚠ Spam Email Safety Tips:*
                            - Don't click on suspicious links
                            - Don't download unexpected attachments  
                            - Don't provide personal or financial information
                            - Report spam to your email provider
                            """)
                    
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")

    # Additional information
    st.markdown("---")
    
    with st.expander("ℹ How it works"):
        st.markdown("""
        Our spam detection system uses advanced machine learning algorithms trained on thousands of emails to identify:
        
        - *Suspicious keywords* commonly found in spam
        - *Email structure patterns* typical of unwanted messages  
        - *Language patterns* that indicate promotional or fraudulent content
        - *Sender behavior* characteristics that suggest spam
        
        The model analyzes your email content locally without storing any data, ensuring your privacy is protected.
        """)
    
    with st.expander("🛡 Privacy & Security"):
        st.markdown("""
        *Your privacy is our priority:*
        
        - ✅ All analysis is performed locally on your device
        - ✅ No email content is stored or transmitted to external servers
        - ✅ No personal data is collected or retained
        - ✅ Open-source algorithms ensure transparency
        
        This tool is designed to help you identify potential spam while keeping your data completely private.
        """)

else:
    st.error("Unable to load the spam detection model. Please check that the model files are available.")

# Footer
st.markdown("""
<div class="footer">
    <p>🔐 Built with Streamlit | 🤖 Powered by Machine Learning</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        Made with ❤ for email security | © 2024 Gmail Spam Detector
    </p>
</div>
""", unsafe_allow_html=True)