import streamlit as st
import datetime
import pandas as pd
import mlflow
import mlflow.pyfunc
import os

with st.form("my_form"):
    st.write("Enter the details")
    region = st.selectbox(
    'Region',
    ('Bejaia Region Dataset ', 'Sidi-Bel Abbes Region Dataset'))

    st.write('You selected:', region)

    d = st.date_input(
        "Enter the date",
        datetime.date(2012, 6, 1),
        min_value=(datetime.date(2012, 6, 1)),
        max_value=(datetime.date(2012, 9, 30))
    )
    st.write('Selected date is:', d.day, d.month, d.year)
    temp_slider_val = st.slider("Temperature", min_value=22, max_value=42)
    rh_slider_val = st.slider("RH", min_value=21, max_value=90)
    ws_slider_val = st.slider("WS", min_value=6, max_value=29)
    rain_slider_val = st.slider("Rain", min_value=0.0, max_value=16.8)
    ffmc_slider_val = st.slider("FFMC", min_value=28.6, max_value=96.0)
    dmc_slider_val = st.slider("DMC", min_value=0.7, max_value=65.9)
    dc_slider_val = st.slider("DC", min_value=6.9, max_value=220.4)
    isi_slider_val = st.slider("ISI", min_value=0, max_value=19)
    bui_slider_val = st.slider("BUI", min_value=1.1, max_value=68.0)
    fwi_slider_val = st.slider("FWI", min_value=0.0, max_value=31.1)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

    if submitted:

        st.write(
            pd.DataFrame(
                {
                    "Region": region, "day": d.day, "month": d.month, "year": d.year,
                    "Temperature": temp_slider_val, "RH": rh_slider_val, "Ws": ws_slider_val, 
                    "Rain": rain_slider_val, "FFMC": ffmc_slider_val, "DMC": dmc_slider_val,
                    "DC": dc_slider_val, "ISI": isi_slider_val, "BUI": bui_slider_val,
                    "FWI": fwi_slider_val
                }, index=[0]
            )
        )


mlflow.set_registry_uri(os.environ["MLFLOW_TRACKING_URI"])

# model_mlflow = mlflow.pyfunc.load_model(
#     model_uri=f"models:/{model_name}/{stage}"
# )

logged_model = 'runs:/d295c0a1eea441218b1c1058baa19455/Fire_classification1'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
data = (pd.DataFrame(
                {
                    "Region": region, "day": d.day, "month": d.month, "year": d.year,
                    "Temperature": temp_slider_val, "RH": rh_slider_val, "Ws": ws_slider_val, 
                    "Rain": rain_slider_val, "FFMC": ffmc_slider_val, "DMC": dmc_slider_val,
                    "DC": dc_slider_val, "ISI": isi_slider_val, "BUI": bui_slider_val,
                    "FWI": fwi_slider_val
                }, index=[0]
            )
    )

data["Region"].replace({'Bejaia Region Dataset ':0,'Sidi-Bel Abbes Region Dataset':1}, inplace=True)

if loaded_model.predict(data) == 0:
    st.write('Prediction is: Not fire')
else:
    st.write('Prediction is: Fire')