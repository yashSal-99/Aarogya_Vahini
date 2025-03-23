from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import uvicorn
import base64
from io import BytesIO
from typing import Optional

# Configure API
app = FastAPI(title="Medical Report Analyzer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google API Configuration
GOOGLE_API_KEY = "AIzaSyBVHW5j8LPFtOPfnCzlyYExIsuDvNCEC7s"  # In production, use environment variables
genai.configure(api_key=GOOGLE_API_KEY)

# Model Configuration
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System Prompt
SYSTEM_PROMPT = """
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

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=GENERATION_CONFIG,
    safety_settings=SAFETY_SETTINGS
)

@app.get("/")
def read_root():
    return {"message": "Medical Report Analyzer API is running"}

@app.post("/analyze-report")
async def analyze_report(file: UploadFile = File(...)):
    """
    Analyze a medical report image using Google's Gemini model
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check file type
    valid_mime_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in valid_mime_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Must be one of: {', '.join(valid_mime_types)}"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        mime_type = file.content_type
        
        # Create image part for Gemini
        image_part = {"mime_type": mime_type, "data": file_content}
        prompt_parts = [image_part, SYSTEM_PROMPT]
        
        # Generate analysis
        response = model.generate_content(prompt_parts)
        
        # Return analysis
        base64_image = base64.b64encode(file_content).decode('utf-8')
        return {
            "analysis": response.text,
            "image": f"data:{mime_type};base64,{base64_image}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing report: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8042)