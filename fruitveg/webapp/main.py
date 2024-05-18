import streamlit as st
import tensorflow as tf
import numpy as np
import urllib.parse
import requests
import os
import secrets
from bs4 import BeautifulSoup

def extract_csrf_token(response_cookies):
    for cookie in response_cookies:
        if cookie.name == "csrftoken":
            return cookie.value
    return None

def generate_random_token(length=32):
    # Generate random bytes
    random_bytes = os.urandom(length)

    # Encode bytes to URL-safe base64
    token = random_bytes.hex()  # Convert to hexadecimal string first
    return token

# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_model.h5")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64, 64))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of max element

# Sidebar
def main():
    st.set_page_config(page_title="Redirecting...", page_icon=":arrow_right:", layout="wide")

    st.sidebar.title("Dashboard")
    app_mode = st.sidebar.selectbox("Select Page", ["Prediction"])
    st.sidebar.image(r"C:\Users\Hp\Downloads\logo1.jpg", width=100)
    st.sidebar.title("Food Predictor")
    st.sidebar.markdown("---")

    # Prediction Page
    if app_mode == "Prediction":
        st.header("Model Prediction")
        image_path = "home_img.jpg"
        st.image(image_path)

        test_image = st.file_uploader("Choose an Image:")
        if st.button("Show Image"):
            st.image(test_image, width=4, use_column_width=True)

        # Predict button
        if st.button("Predict"):
            st.write("Our Prediction")
            result_index = model_prediction(test_image)

            # Reading Labels
            with open("labels.txt") as f:
                content = f.readlines()
            label = [i[:-1] for i in content]
            prediction_result = label[result_index]

            st.success("Model is Predicting it's a {}".format(prediction_result))

            # Pass prediction result back to Django app
            django_url = "http://localhost:8000/update_search_bar/"  # Change URL accordingly
            django_response = requests.get("http://localhost:8000")  # Assuming Django web app is running on localhost
            csrf_token = extract_csrf_token(django_response.cookies)
            headers = {"X-CSRFToken": csrf_token} if csrf_token else {}

            response = requests.get(django_url + "?prediction=" + prediction_result)

            if response.status_code == 200:
                st.write("Prediction result sent back to Django web app successfully!")
                
                st.write(f"[Redirect to Django Web App](http://localhost:8000/?pd={prediction_result})")
                st.stop()  # Stop the Streamlit app to allow the redirect
     
            else:
                 st.error("Failed to send prediction result to Django web app.")
                
if __name__ == "__main__":
     main()