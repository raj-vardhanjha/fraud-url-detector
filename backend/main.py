from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from backend.feature_extractor import extract_features

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Fraud URL Detector API is running"}

model = joblib.load("backend/model.pkl")

class URLInput(BaseModel):
    url: str

@app.post("/predict/")
def predict_url(data: URLInput):

    url = data.url
    features = extract_features(url)

    prediction = model.predict([features])[0]

    if prediction == 1:
        result = "phishing"
    else:
        result = "legitimate"

    return {"prediction": result}
