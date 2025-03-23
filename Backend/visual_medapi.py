from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pathlib import Path

# Configure Google Generative AI
genai.configure(api_key="AIzaSyCLywgeI9WCXCpkHy76fbYahZMxSh9LU7M")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompts = [
    """
    You are a domain expert in medical image analysis. You are tasked with 
    examining medical images for a renowned hospital.
    Your expertise will help in identifying or 
    discovering any anomalies, diseases, conditions or
    any health issues that might be present in the image.
    You are a Ayurvedic doctor and you have expertise in AYUSH (ayurveda, yoga, unani, siddha and homeopathy).
    
    Your key responsibilites:
    1. Detailed Analysis : Scrutinize and thoroughly examine each image, 
    focusing on finding any abnormalities.
    2. Analysis Report : Document all the findings and 
    clearly articulate them in a structured format.
    3. Recommendations : Basis the analysis, suggest remedies, 
    tests or treatments as applicable.
    4. Treatments : If applicable, lay out detailed treatments 
    which can help in faster recovery.
    5. Ayurvedic Remedic: If applicable, suggest Ayurvedic remedies.
    
    Important Notes to remember:
    1. Scope of response : Only respond if the image pertains to 
    human health issues.
    2. Clarity of image : In case the image is unclear, 
    note that certain aspects are 
    'Unable to be correctly determined based on the uploaded image'
    3. Disclaimer : Accompany your analysis with the disclaimer: 
    "Consult with a Doctor before making any decisions."
    4. Your insights are invaluable in guiding clinical decisions. 
    Please proceed with the analysis, adhering to the 
    structured approach outlined above.
    
    Please provide the final response with these 4 headings : 
    Detailed Analysis, Analysis Report, Recommendations and Treatments
    """
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_data = await file.read()

        # Prepare the image and prompt
        image_parts = [{"mime_type": file.content_type, "data": image_data}]
        prompt_parts = [image_parts[0], system_prompts[0]]

        # Generate response
        response = model.generate_content(prompt_parts)
        return {"analysis": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8041)