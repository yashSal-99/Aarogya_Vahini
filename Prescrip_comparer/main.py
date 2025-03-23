import easyocr
import re

# Initialize EasyOCR reader (English)
reader = easyocr.Reader(['en'])

# Load and Process Prescription Image
image_path = "C:\\yash\\Machine_Learning\\MediLocker\\Prescrip_comparer\\4.jpg"  # Update with your image path
results = reader.readtext(image_path)

# Extract Text
extracted_text = "\n".join([text for _, text, _ in results])
print("Extracted Text from Prescription:\n", extracted_text)

# List of common medicine keywords
medicine_keywords = [
    "Dolo", "Paracetamol", "Crocin", "Augmentin", "Amoxicillin", "Clavulanic Acid",
    "Cetirizine", "Azithromycin", "Omeprazole", "Metformin", "Atorvastatin"
]

# Extract medicine names (filter words that match medicine keywords)
def extract_medicine_names(text):
    words = re.findall(r'\b\w+\b', text)  # Extract all words
    medicines = [word for word in words if word in medicine_keywords]
    return medicines

medicine_list = extract_medicine_names(extracted_text)
print("\nIdentified Medicines:", medicine_list)

# Mock Database for Medicine Prices

medicine_prices = {
    "Dolo": {"PharmEasy": 25.66, "1mg": 32, "Netmeds": 30.38},
    "Paracetamol": {"PharmEasy": 16.43, "1mg": 19.13, "Netmeds": 19},
    "Crocin": {"PharmEasy":29 , "1mg": 33, "Netmeds": 30},
    "Augmentin": {"PharmEasy": 155, "1mg": 193, "Netmeds": 204},
    "Amoxicillin": {"PharmEasy": 155, "1mg": 204, "Netmeds": 204},
    "Clavulanic Acid": {"PharmEasy": 155, "1mg": 193, "Netmeds": 204},
    "Cetirizine ": {"PharmEasy": 14.0, "1mg": 15.0, "Netmeds": 13.5},
    "Azithromycin": {"PharmEasy": 85.0, "1mg": 90.0, "Netmeds": 88.0},
    "Omeprazole": {"PharmEasy": 12.0, "1mg": 11.5, "Netmeds": 12.5},
    "Metformin ": {"PharmEasy": 9.0, "1mg": 8.5, "Netmeds": 9.5},
    "Atorvastatin ": {"PharmEasy": 15.0, "1mg": 14.5, "Netmeds": 15.5},
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

# Fetch Prices
print("\n📌 Price Comparison:")
for med in medicine_list:
    prices = medicine_prices.get(med, {"PharmEasy": "Not Found", "1mg": "Not Found", "Netmeds": "Not Found"})
    print(f"\n🔹 {med}:")
    print(f"  🛒 PharmEasy Price: ₹{prices['PharmEasy']}")
    print(f"  🛒 1mg Price: ₹{prices['1mg']}")
    print(f"  🛒 Netmeds Price: ₹{prices['Netmeds']}")
    
    # Find the platform with the lowest price
    min_platform = min(prices, key=prices.get)
    print(f"  🔗 Best Price Link: https://{min_platform.lower()}.com/search/all?name={med}")

# Suggest Generic Alternatives
print("\n📌 Generic Alternatives:")
for med in medicine_list:
    alternatives = generic_alternatives.get(med, ["No Generic Found"])
    print(f"🔹 {med}: {', '.join(alternatives)}")
