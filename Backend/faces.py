import cv2
import os
import time
import datetime
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Serve static files from the "face_data" directory
app.mount("/face_data", StaticFiles(directory="face_data"), name="face_data")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the datasets directory exists
output_dir = 'face_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def clear_output_dir():
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                logging.error(f"Error removing existing file: {filename} ({e})")
        logging.info(f"Existing data in '{output_dir}' cleared.")

def get_face_data():
    # Initialize video capture
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise Exception("Could not open webcam. Please ensure it is connected and accessible.")
    logging.info("Camera initialized successfully.")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise Exception("Could not load Haar Cascade classifier.")
    logging.info("Haar Cascade classifier loaded successfully.")

    count = 0
    max_images = 10
    times = 0
    logging.info("Ensure good lighting and look directly into the camera...")

    start_time = time.time()
    interval = 5

    while True:
        ret, frame = video.read()
        if not ret:
            logging.error("Failed to grab frame")
            break
        logging.info("Frame captured successfully.")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        logging.info(f"Detected {len(faces)} faces in the current frame.")

        current_time = time.time()

        if current_time - start_time >= interval:
            for (x, y, w, h) in faces:
                if count >= max_images:
                    break

                count += 1
                face_roi = frame[y:y+h, x:x+w]
                resized_face = cv2.resize(face_roi, (300, 300))
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = f"face_data/Face{timestamp}{count}.jpg"
                cv2.imwrite(filename, resized_face)
                logging.info(f"Saved face image: {filename}")

            start_time = current_time
            times += 1

        # Display the frame using OpenCV (for debugging)
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

        if count >= max_images or times >= 3:
            break

    # Release the camera and close OpenCV windows
    video.release()
    cv2.destroyAllWindows()
    logging.info(f"Dataset Collection Done. {count} images saved.")

@app.get("/start-face-detection")
def start_face_detection():
    try:
        clear_output_dir()
        get_face_data()
        
        # Get the list of captured images
        image_files = [f for f in os.listdir(output_dir) if f.endswith('.jpg')]
        image_urls = [f"http://localhost:8044/face_data/{f}" for f in image_files]
        
        return {
            "message": "Face detection and dataset collection completed.",
            "image_urls": image_urls,
        }
    except Exception as e:
        logging.error(f"Error in face detection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8044)