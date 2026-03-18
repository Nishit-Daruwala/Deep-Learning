from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Load model
model = tf.keras.models.load_model("model.h5")

class_names = ['buildings','forest','glacier','mountain','sea','street']

def preprocess_image(image):
    image = image.resize((150,150))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    processed = preprocess_image(image)
    prediction = model.predict(processed)
    
    confidence = float(np.max(prediction))
    predicted_class = class_names[np.argmax(prediction)]
    
    # Threshold (you can tune this)
    THRESHOLD = 0.7
    
    if confidence < THRESHOLD:
        return {
            "prediction": "I don't know",
            "confidence": confidence
        }
    
    return {
        "prediction": predicted_class,
        "confidence": confidence
    }