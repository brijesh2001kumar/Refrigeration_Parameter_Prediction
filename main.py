# Deep learning libraries (Tensorflow Framework)
from tensorflow.keras.models import load_model
import joblib
import numpy as np
# Libraries required for deployment (Done using Streamlit)
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoHTMLAttributes



cop,ec,gc=0,0,0




# st.write('Caution : For first-time usage, App can take some time to load (ps : for Downloading the Model)')
# # Making the Function decorator to memoize(cache) function execution of loading the model
@st.cache(allow_output_mutation=True)
def load_data_cached(location1,location2):
    # return(load_model(location1,compile=False))
#     # returning the model loaded using the tf.keras.load_model function
    return([load_model(location1, compile=False),joblib.load(location2)])

location1 = 'Model.h5'
location2='scaler.save'
model,scaler = load_data_cached(location1,location2)
    
# model=load_data_cached(location1,location2)

#settimng up background image for app
st.markdown(
   f'''
   <style>
   .stApp {{
             background: url("https://img.freepik.com/premium-photo/abstract-communication-technology-network-concept_34629-641.jpg?w=1380");
             background-size: cover
         }}
   </style>
   ''',
   unsafe_allow_html=True)

#creating containers for different sections of app
header = st.container()
input=st.form(key='form')
output=st.container()
model_intro = st.container()
model_details = st.container()
references = st.container()


with header:
    st.title('Performance Predicton for single-stage trancritical vapour compression refrigeration system for CO2')
    st.markdown("""---""")
    col1,col2=st.columns(2)
    col1.write('This app predicts various performance metrics namely:- \n\nCOP, evaporator capacity and Gas cooler capacity\n\ngiven:-\n\nevaporator exit temperature,gas cooler outlet temperature, gas cooler pressure, superheat temperature in suction line and compressor efficiency\n\n for non-ideal single stage Transcritical CO2 refrigeration system.')
    col2.image('cycle.png')
    st.markdown("""---""")
    

with input:
    st.markdown("<h3 style='text-align: center; color: white;'>PREDICT HERE</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: white;'>INPUT PARAMETERS</h5>", unsafe_allow_html=True)
    
    input_col1, input_col2 = st.columns(2)
    t1 = input_col1.number_input('Enter Evaporator exit temperature (in celcius)',min_value=0,max_value=25)
    t3 = input_col1.number_input('Enter Gas Cooler exit temperature (in celcius)',min_value=30,max_value=55)
    p3 = input_col2.number_input('Enter Gas Cooler pressure (in bar)',min_value=80,max_value=295)
    e = input_col2.number_input('Enter compressor efficiency')
    tsh = st.slider('Enter suction line superheat temperature (in celcius)',min_value=0,max_value=10,value=0,step=1)
    
    submit_button = input.form_submit_button(label='Submit')


with output:
    st.write('***')
    st.markdown("<h5 style='text-align: center; color: white;'>Predicted Metrics</h5>", unsafe_allow_html=True)
    output_col1,output_col2,output_col3=st.columns(3)
    
    if submit_button:
        X_test=scaler.transform([[t1,t3,p3,e,tsh]])
        # st.write(model.predict(X_test)[0][0])
        [cop,ec,gc]=model.predict(X_test)[0]
        output_col1,output_col2,output_col3=st.columns(3)
        output_col1.metric("Gas Cooler Capacity(per TR)", str(round(gc,3))+'kJ/kg')
        output_col2.metric("Evaporator Capacity(per TR)", str(round(ec,3))+'kJ/kg')
        output_col3.metric("COP", str(round(cop,3)))
    else:
        output_col1,output_col2,output_col3=st.columns(3)
        st.write('***')
        output_col3.metric("COP", "-")
        output_col1.metric("Evaporator Capacity(per TR)", "-",)
        output_col2.metric("Gas Cooler Capacity(per TR)", "-",)


