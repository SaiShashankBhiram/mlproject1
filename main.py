from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import numpy as np

app = FastAPI()

# Load trained model from saved artifacts
model_path = "artifacts/model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Load the preprocessor from saved artifacts
preprocessor_path = "artifacts/preprocessor.pkl"
with open(preprocessor_path, "rb") as file:
    preprocessor = pickle.load(file)

@app.get("/")
def home():
    return {"message": "ML Model API is Running!"}

@app.post("/predict/")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])  # Convert JSON input to DataFrame
        
        # Apply the same preprocessing pipeline used during training
        processed_data = preprocessor.transform(df)  

        # Ensure transformed input matches model expectations
        if processed_data.shape[1] != model.n_features_in_:
            raise HTTPException(status_code=400, detail=f"Model expects {model.n_features_in_} features, but received {processed_data.shape[1]}")

        prediction = model.predict(processed_data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))