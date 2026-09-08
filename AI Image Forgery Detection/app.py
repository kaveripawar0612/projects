import streamlit as st
import cv2, numpy as np
from PIL import Image

st.set_page_config(page_title='AI Image Forgery Detection',page_icon='🔎',layout='wide')
st.title('🔎 AI Image Forgery Detection')
st.caption('Forensic analysis baseline — not a definitive authenticity verdict')
file=st.file_uploader('Upload an image',type=['png','jpg','jpeg','webp'])
if file:
    pil=Image.open(file).convert('RGB'); arr=np.array(pil); gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    ela=cv2.detailEnhance(arr,sigma_s=10,sigma_r=.15)
    c1,c2=st.columns(2)
    with c1: st.image(pil,caption='Input image',use_container_width=True)
    with c2: st.image(ela,caption='Forensic enhancement view',use_container_width=True)
    st.subheader('Image signals')
    a,b,c=st.columns(3)
    a.metric('Resolution',f'{arr.shape[1]} × {arr.shape[0]}')
    b.metric('Mean intensity',f'{gray.mean():.1f}')
    c.metric('Edge density',f'{(cv2.Canny(gray,50,150)>0).mean()*100:.2f}%')
    st.info('These signals can help inspection but do not prove that an image is genuine or manipulated. Use a trained, validated forensic model for classification.')
