# 🏥 **ArogyaVahini - AI-Powered Healthcare Assistant**

ArogyaVahini is an AI-driven healthcare platform designed to provide **diagnostics, emergency medical assistance, prescription analysis, wellness tracking, and environmental health monitoring**. It integrates cutting-edge technologies, including **GenAI (Gemini Pro 1.5 API), Computer Vision, NLP, and Deep Learning**, to enhance accessibility, affordability, and efficiency in healthcare.

---

## 🚀 **Key Features**

### 🩺 **Medical Diagnosis**
- **General Doctor Chatbot 🤖** – AI-powered chatbot for medical guidance & symptom analysis.
- **Report Analyst 📄** – Scans & interprets medical reports, suggesting relevant tests.
- **Skin Disease Detection & Remedies 📸** – AI-based analysis with **Ayurvedic & homeopathic** treatments.
- **Tumor Detection 🧠** – Identifies **brain & lung tumors** from MRI/X-ray scans.
- **Pneumonia Detection 🫁** – Detects pneumonia using chest X-ray images.
- **Retina, Scalp & Tongue Disease Detection 👀** – AI-based detection with **explanations & Ayurvedic remedies**.
- **Viral Disease Prediction 🦠** – AI predicts viral infections based on **symptom inputs**.

### 📝 **Prescription & Medicine Assistance**
- **Prescription Price Comparison 💊** – OCR extracts medicine names & compares prices.
- **Alternative Medicine Finder 🌿** – Suggests **Ayurvedic & homeopathic** substitutes.
- **PlantsUp 🌿** – Recognizes plants & provides their **medicinal benefits**.

### 🚨 **Emergency & Medical Assistance**
- **Medilocker 🆘** – **Face recognition-based** medical record access during emergencies.
- **Ambulance Scheduling & Tracking 🚑** – Real-time ambulance booking & tracking.
- **MedFinder 🏥** – Finds **hospitals, clinics, and pharmacies** nearby using Google Maps API.

### 🧠 **Wellness & Mental Health**
- **Diet Planner 🥗** – AI-driven **personalized meal recommendations**.
- **MindfulMe 🧠** – AI-based **sentiment analysis for mental health** insights.
- **OMmind 🧘** – Guided meditation for stress relief.
- **Yoga Assistant 🏋‍♀** – AI-powered yoga posture detection & correction.

### 🏛 **Government Healthcare Accessibility**
- **Government Scheme Finder 📜** – Matches users with **health-related government schemes**.

### 🌎 **Environmental Risk Monitoring**
- **AQI Monitoring 💨** – Real-time **air quality index (AQI)** tracking & alerts.
- **Flood Risk Assessment 🌊** – Predicts flood risks using **satellite & geospatial data**.

### 🌍 **Community Health & Awareness**
- **Community Health Insights 🏥** – AI-powered **public health monitoring** & awareness forums.

---

## 🛠 **Tech Stack**

### **🔹 AI & Machine Learning**
- **Gemini Pro 1.5 API** – Used for **GenAI-based chatbot, report analysis & diagnosis**.
- **Computer Vision** – **YOLO, OpenCV, TensorFlow, PyTorch** for image-based disease detection.
- **Deep Learning** – Used for **tumor detection, pneumonia classification, and symptom analysis**.
- **ML Algorithms** – Decision Trees, CNNs, Transformers for predictive analytics.

### **🔹 Backend & API Development**
- **FastAPI / Flask** – Lightweight backend for AI model integration.
- **MongoDB** – NoSQL database for **user medical records & analytics**.
- **Google Maps API** – For **hospital & ambulance location tracking**.
- **Twilio API** – For **emergency SMS & notifications**.

### **🔹 Frontend & UI/UX**
- **React.js / Next.js** – **Modern, responsive frontend framework**.
- **Tailwind CSS** – For clean and intuitive UI design.

### **🔹 DevOps & Deployment**
- **Docker** – For containerized deployment.
- **NGINX** – Load balancing & security.
- **GitHub Actions** – Automated testing & CI/CD.

---

## 🏗 **How to Set Up Locally**

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/arogya-vahini.git
   cd arogya-vahini
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
3. **Run backend**
   ```bash
   uvicorn app:main --reload
   ```
4. **Run frontend**
   ```bash
   cd frontend
   npm run dev
   ```

---

## 📌 **Future Enhancements**
- ✅ Real-time AI-based **video consultation**.
- ✅ Expanded **GenAI capabilities** using **Gemini Pro 1.5 API**.
- ✅ Blockchain-based **secure health records**.

🚀 **ArogyaVahini is your all-in-one AI-powered healthcare assistant!** 🌿💊🏥
