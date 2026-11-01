
import streamlit as st
import requests
import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/predict"
)
# Page configuration
st.set_page_config(
    page_title="Iris Flower Predictor",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 Iris Flower Prediction")
st.write("Enter the flower measurements to predict its species.")

st.divider()

# Input fields
st.subheader("Flower Measurements (cm)")

sepal_length = st.number_input(
    "Sepal Length",
    min_value=0.1,
    value=5.1,
    step=0.1
)

sepal_width = st.number_input(
    "Sepal Width",
    min_value=0.1,
    value=3.5,
    step=0.1
)

petal_length = st.number_input(
    "Petal Length",
    min_value=0.1,
    value=1.4,
    step=0.1
)

petal_width = st.number_input(
    "Petal Width",
    min_value=0.1,
    value=0.2,
    step=0.1
)

st.divider()

# Prediction button
if st.button("Predict Flower 🌼", use_container_width=True):

    # Prepare input for FastAPI
    input_data = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }


    try:
        with st.spinner("Predicting flower species..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=10
            )

        # Check whether the API returned success
        response.raise_for_status()
        result = response.json()

        # Display prediction
        st.success("Prediction completed!")

        st.subheader("Predicted Flower")
        st.title(f"🌸 {result['flower_name'].title()}")

        st.write(
            f"**Class Number:** {result['class_number']}"
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Please start the backend server first."
        )

    except requests.exceptions.Timeout:
        st.error("The prediction request timed out.")

    except requests.exceptions.RequestException as error:
        st.error(f"API request failed: {error}")

    except (ValueError, KeyError):
        st.error("Received an invalid response from the API.")
