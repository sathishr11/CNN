import mlflow.pyfunc
import streamlit as st
from PIL import Image
import numpy as np
import os



model_name = "DogCatClassifier"
stage = "Production"

os.environ["MLFLOW_TRACKING_URI"] = st.secrets["MLFLOW_TRACKING_URI"]
os.environ["MLFLOW_TRACKING_USERNAME"] = st.secrets["MLFLOW_TRACKING_USERNAME"]
os.environ["MLFLOW_TRACKING_PASSWORD"] = st.secrets["MLFLOW_TRACKING_PASSWORD"]
mlflow.set_registry_uri(os.environ["MLFLOW_TRACKING_URI"])
model_mlflow = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{stage}"
)


st.title('DOG vs CAT image classification')
st.write(
    """Upload image of a cat or dog.
        The image you upload will be fed
        through the Deep Neural Network in real-time
        and the output will be displayed to the screen"""
)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    image = Image.open(uploaded_file)
    img = image.resize((224,224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0) # [batch_size, row, col, channel]
    result = model_mlflow.predict(img_array) # [[0.99, 0.01], [0.99, 0.01]]

    argmax_index = np.argmax(result, axis=1) # [0, 0]
    st.title("Here is the image you've uploaded")
    if argmax_index[0] == 0:
        st.image(image, caption="The model has predicted it as cat")
    else:
        st.image(image, caption='The model has predicted it as dog')