import os
from sre_parse import Verbose
from dotenv import load_dotenv, find_dotenv


from pathlib import Path

# dotenv_path = Path('path/to/.env')
# dotenv_path = Path(__file__).parents[1]
# print(__file__)
# print(dotenv_path)
# print(Path(os.path.join(dotenv_path,'.env')))
# load_dotenv(dotenv_path)
# load_dotenv(Path(os.path.join(dotenv_path,'.env')))
# load_dotenv(find_dotenv('.env'))
load_dotenv()
# os.environ['PROJECT_ID']
# os.environ.get('PROJECT_ID')
print(os.getenv('ACCESS_TOKEN'))
import streamlit as st

st.title('DOG vs CAT image classification')
st.subheader('Upload an image of either dog or cat')
uploaded_file = st.file_uploader("Choose a file")
data_load_state = st.text('Waiting for image...')
if uploaded_file is not None:
    data_load_state.text('Image uploaded. If you wish to upload again use browse files')
