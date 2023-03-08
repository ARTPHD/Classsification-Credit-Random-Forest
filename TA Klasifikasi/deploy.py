#Import Libraries

import pandas as pd
import streamlit as st 
from pickle import load
import sklearn
from PIL import Image

#Title of web page
st.title("Welcome To Prediction Collection")

#Image on webpage
img = Image.open("sms.jpg")
st.image(img)
                  

#Title for sidebar
st.title('User Input Parameters')
nom = st.text_input('Account number')

    ## Full Name
fn = st.text_input('Full Name')

ca     = {'Percaya': 'Percaya', 'Tidak': 'Tidak Percaya', 'Normal': 'Normal'}
pa     = {'Mampu': 'Mampu', 'Tidak': 'Tidak Mampu', 'Sedang': 'Sedang'}
pi     = {'Banyak': 'Banyak', 'Tidak': 'Tidak Kuat', 'Sedang': 'Sedang'}
cn     = {'Baik': 'Baik', 'Tidak': 'Tidak Baik', 'Normal': 'Normal'}
cl     = {'Kuat': 'Kuat', 'Rendah': 'Rendah', 'Sedang': 'Sedang'}


#Input variables               
def user_input_features():

    chr  = st.selectbox("Character", options=ca.keys(), format_func=(lambda x: '{}'.format(ca.get(x)) ))
    cpa  = st.selectbox("Capacity",options=pa.keys(), format_func=(lambda x: '{}'.format(pa.get(x)) ))
    cpi  = st.selectbox("Capital",options=pi.keys(), format_func=(lambda x: '{}'.format(pi.get(x)) ))
    cdt  = st.selectbox("Condition",options=cn.keys(), format_func=(lambda x: '{}'.format(cn.get(x)) ))
    clt  = st.selectbox('Collateral', options=cl.keys(), format_func=(lambda x: '{}'.format(cl.get(x)) ))
    
    
    new = {'Character': chr,
           'Capacity': cpa, 
           'Capital': cpi, 
           'Condition': cdt,
           'Collateral': clt}
           
    features = pd.DataFrame(new, index=[0])
    return features
                  
#Running the function
df = user_input_features()
st.write('You have chosen following inputs: ')
st.write(df)

#Loading the model
model = load(open('kredit1.pkl', 'rb'))


#Predicting the model

result = model.predict(df)

if st.button('Predict'):
    #st.snow()
    st.header('Hasil Prediksi :')
    if result[0]=="Approved":
        st.success(
            "" + fn +" || "
            "Account number: "+nom +' || '
            "Selamat Anda Layak Mendapatkan Pinjaman")
        good = Image.open("ap.png")
        st.image(good)
        
        
        
    else:
        st.error(
            "Hello: " + fn +" || "
            "Account number: "+nom +' || '
            'Mohon Maaf Anda Belum Dapat Mengambil Pinjaman')
        bad  = Image.open("rj.png")
        st.image(bad)
        
if __name__=='__user_input_features__':
    user_input_features()
