import streamlit as st
from matplotlib import image
import pandas as pd
import plotly.express as px
import os

st.snow()
file_d=os.path.dirname(os.path.abspath(__file__))

parent_d=os.path.join(file_d,os.pardir)

dir_of_in=os.path.join(parent_d,"resources")

im_path=os.path.join(dir_of_in,"titanic.jpg")
data_path=os.path.join(dir_of_in,"test.csv")

st.title("Dashboard - Titanic Data")

img=image.imread(im_path)
st.image(img)

df = pd.read_csv(data_path)

species=st.selection("select the gender:",df['species'].unique())
col1,col2=st.columns(2)

fig_1=px.histogram(df[df["gender"]==species],x="Sex")
c0l1.plotly_chart(fig_1,use_container_width=true)


fig_1=px.box(df[df["gender"]==species],x="Sex")
c0l2.plotly_chart(fig_1,use_container_width=true)

