import streamlit as st
import google.generativeai as genai
#from google_api_key import google_report_key
google_report_key ="AIzaSyBVHW5j8LPFtOPfnCzlyYExIsuDvNCEC7s"

genai.configure(api_key=google_report_key)

# Model Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System Prompt for Medical Report Analysis
system_prompt = """
You are an expert medical assistant trained to analyze medical reports. Your job is to:
1. Extract and interpret key medical terms, values, and findings.
2. Provide insights into the patient's condition based on the extracted data.
3. Suggest further medical tests, possible diagnoses, or lifestyle recommendations.
4. Always include a disclaimer: "Consult a doctor before making any medical decisions."

Provide the analysis under these headings:
- **Findings Summary**
- **Possible Health Implications**
- **Recommended Next Steps**
- **Disclaimer**
"""

# Load Model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit UI
st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺", layout="wide")
st.title("Medical Report Analyzer 🏥🩺")
st.subheader("Upload a medical report (PDF/Image) to get AI-powered insights")

uploaded_file = st.file_uploader("Upload Medical Report", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    st.image(uploaded_file, width=300, caption='Uploaded Report')
    submit = st.button("Analyze Report")
    
    if submit:
        file_data = uploaded_file.getvalue()
        
        image_parts = [{"mime_type": "image/jpg", "data": file_data}]
        prompt_parts = [image_parts[0], system_prompt]
        
        response = model.generate_content(prompt_parts)
        
        if response:
            st.subheader("📝 AI-Generated Report Analysis")
            st.markdown(response.text)
