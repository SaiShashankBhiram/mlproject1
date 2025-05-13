import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

app = FastAPI()

# Load trained model
model_path = "artifacts/model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Define feature lists
numerical_columns = ["reading_score", "writing_score"]  # Adjust based on training columns
categorical_columns = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]

# Define same preprocessing pipeline
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehotencoder", OneHotEncoder(handle_unknown="ignore")),
    ("scaler", StandardScaler(with_mean=False)),
])

preprocessor = ColumnTransformer([
    ("num_pipeline", num_pipeline, numerical_columns),
    ("cat_pipeline", cat_pipeline, categorical_columns),
])

@app.post("/predict/")
def predict(data: dict):
    try:
        # Convert input JSON to DataFrame
        df = pd.DataFrame([data])

        # Apply preprocessing
        processed_data = preprocessor.transform(df)

        # Make prediction
        prediction = model.predict(processed_data)
        
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))