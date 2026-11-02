
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

# Create FastAPI application
app = FastAPI(title="Iris Flower Prediction API")

# Load the trained ML model
model = joblib.load("iris_model.pkl")

# Define the four inputs expected from the user
class IrisInput(BaseModel):
    sepal_length: float = Field(gt=0, description="Sepal length in cm")
    sepal_width: float = Field(gt=0, description="Sepal width in cm")
    petal_length: float = Field(gt=0, description="Petal length in cm")
    petal_width: float = Field(gt=0, description="Petal width in cm")


# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Iris Flower Prediction API"}

@app.get("/health")
@app.head("/health")
def health_check():
    return{"message":"Healthy"}

# Prediction endpoint
@app.post("/predict")
def predict_flower(data: IrisInput):

    # Arrange input values in the correct order
    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    # Predict the flower class
    prediction = int(model.predict(input_data)[0])

    # Convert class number to flower name
    flower_names = ["setosa", "versicolor", "virginica"]
    flower_name = flower_names[prediction]

    # Return prediction as JSON
    return {
        "flower_name": flower_name,
        "class_number": prediction
    }
