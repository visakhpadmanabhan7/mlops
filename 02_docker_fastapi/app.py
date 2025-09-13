from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model at startup
model = joblib.load("model.pkl")

# Define input schema
class InputData(BaseModel):
    features: list[float]

# Create FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "ML model is running 🚀"}

@app.post("/predict")
def predict(data: InputData):
    X = np.array([data.features])
    pred = model.predict(X)
    return {"prediction": int(pred[0])}