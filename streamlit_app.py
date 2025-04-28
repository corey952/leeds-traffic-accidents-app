import streamlit as st
import pandas as pd

st.title("Leeds Traffic Accidents")
st.write(
    "Accidents"
)

df =  pd.read_csv("Traffic%20accidents_2019_Leeds.csv")
st.write(df)