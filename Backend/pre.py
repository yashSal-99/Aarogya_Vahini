from fastapi import FastAPI, File, UploadFile, HTTPException
import easyocr
import re
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (replace "*" with your frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize EasyOCR reader (English)
reader = easyocr.Reader(['en'])

# List of common medicine keywords
medicine_keywords = [
    "Dolo", "Paracetamol", "Crocin", "Augmentin", "Amoxicillin", "Clavulanic Acid",
    "Cetirizine", "Azithromycin", "Omeprazole", "Metformin", "Atorvastatin"
]

# Updated Mock Database for Medicine Prices with numeric values
medicine_prices = {
    "Dolo": {"PharmEasy": 25.66, "1mg": 32, "Netmeds": 30.38},
    "Paracetamol": {"PharmEasy": 16.43, "1mg": 19.13, "Netmeds": 19},
    "Crocin": {"PharmEasy": 29, "1mg": 33, "Netmeds": 30},
    "Augmentin": {"PharmEasy": 155, "1mg": 193, "Netmeds": 204},
    "Amoxicillin": {"PharmEasy": 155, "1mg": 204, "Netmeds": 204},
    "Clavulanic Acid": {"PharmEasy": 155, "1mg": 193, "Netmeds": 204},
    "Cetirizine": {"PharmEasy": 14.0, "1mg": 15.0, "Netmeds": 13.5},
    "Azithromycin": {"PharmEasy": 85.0, "1mg": 90.0, "Netmeds": 88.0},
    "Omeprazole": {"PharmEasy": 12.0, "1mg": 11.5, "Netmeds": 12.5},
    "Metformin": {"PharmEasy": 9.0, "1mg": 8.5, "Netmeds": 9.5},
    "Atorvastatin": {"PharmEasy": 15.0, "1mg": 14.5, "Netmeds": 15.5},
}

# Mock Database for Generic Alternatives
generic_alternatives = {
    "Dolo": ["Paracetamol"],
    "Paracetamol": ["Acetaminophen"],
    "Crocin": ["Paracetamol"],
    "Augmentin": ["Amoxicillin + Clavulanic Acid"],
    "Amoxicillin": ["Penicillin"],
    "Clavulanic Acid": ["No Generic Found"],
    "Cetirizine": ["Levocetirizine"],
    "Azithromycin": ["Erythromycin"],
    "Omeprazole": ["Pantoprazole"],
    "Metformin": ["No Generic Found"],
    "Atorvastatin": ["Rosuvastatin"],
}

# Extract medicine names
def extract_medicine_names(text: str) -> List[str]:
    words = re.findall(r'\b\w+\b', text)  # Extract all words
    medicines = [word for word in words if word in medicine_keywords]
    return medicines

@app.post("/upload-prescription/")
async def upload_prescription(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Save the uploaded file temporarily to process with EasyOCR
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Process image with EasyOCR
        results = reader.readtext(temp_file_path)

        # Extract text
        extracted_text = "\n".join([text for _, text, _ in results])

        # Extract medicine names
        medicine_list = extract_medicine_names(extracted_text)

        # Prepare response data
        price_comparison = {}
        best_price_links = {}
        
        for med in medicine_list:
            prices = medicine_prices.get(med, {"PharmEasy": "Not Found", "1mg": "Not Found", "Netmeds": "Not Found"})
            
            # Format prices with ₹ symbol for display
            formatted_prices = {
                platform: f"₹{price}" if isinstance(price, (int, float)) else price 
                for platform, price in prices.items()
            }
            
            price_comparison[med] = formatted_prices
            
            # Find the platform with the lowest price
            if all(isinstance(price, (int, float)) for price in prices.values()):
                min_platform = min(prices, key=prices.get)
                best_price_links[med] = f"https://{min_platform.lower()}.com/search/all?name={med}"
        
        generic_alternatives_list = {med: generic_alternatives.get(med, ["No Generic Found"]) for med in medicine_list}

        return {
            "extracted_text": extracted_text,
            "medicine_list": medicine_list,
            "price_comparison": price_comparison,
            "best_price_links": best_price_links,
            "generic_alternatives": generic_alternatives_list,
        }
    
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

@app.get("/")
def read_root():
    return {"message": "Welcome to Prescription Analyzer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="127.0.0.1", port=8032)