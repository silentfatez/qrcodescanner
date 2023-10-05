import streamlit as st
import pyrebase
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

current_date_and_time = datetime.now()


config = {
  "apiKey": st.secrets['apiKey'],
  "authDomain": st.secrets['authDomain'],
  "databaseURL": st.secrets['databaseURL'],
  "storageBucket": st.secrets['storageBucket']
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
st.write(current_date_and_time)




st.write("""
# Login Form
Key in your unique code below
""")
h=st.experimental_get_query_params()
st.write()
st.write('Warning do not submit if you are not staff. Only the staff can sign in guests. Failure to heed warnings will be barred from entering the event.')
try: 
    with st.form(key='my_form'):
        validation_code = st.text_input('Code to enter', value=h['qrcode'][0], key="type_input")
        submit_button = st.form_submit_button(label='Submit')
except:
    with st.form(key='my_form2'):
        validation_code = st.text_input('Code to enter', key="type_input")
        submit_button = st.form_submit_button(label='Submit')

if submit_button:
    
    data = database.child("qr_code_codes").get()
    datadict = data.val() 
    result=datadict.get(validation_code,'not avail')
    if result==True:
        st.write('Sucess')
        st.balloons()
        datadict.update({validation_code:False})
        database.child("qr_code_codes").update(datadict)

    elif result=='not avail':
        st.error('Failure', icon='🚨')
    else:
        st.warning('Already Entered', icon="⚠️")




