import mlflow.pyfunc
import streamlit as st
from PIL import Image
import numpy as np
import os
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/mail2sathish11/CNN.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"]="mail2sathish11"
os.environ["MLFLOW_TRACKING_PASSWORD"]=""


model_name = "VGGmodel16"
stage = "Production"

mlflow.set_registry_uri(os.environ["MLFLOW_TRACKING_URI"])
model_mlflow = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{stage}"
)

# img = Image.open("./artifacts/data_ingestion/PetImages/Dog/5.jpg")
# img = img.resize((224,224))
# img_array = np.array(img)
# img_array = np.expand_dims(img_array, axis=0)
# img_array.shape

# print(model_mlflow.predict(img_array))

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:

    image = Image.open(uploaded_file)
    img = image.resize((224,224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0) # [batch_size, row, col, channel]
    result = model_mlflow.predict(img_array) # [[0.99, 0.01], [0.99, 0.01]]

    argmax_index = np.argmax(result, axis=1) # [0, 0]
    if argmax_index[0] == 0:
        st.image(image, caption="predicted: cat")
    else:
        st.image(image, caption='predicted: dog')