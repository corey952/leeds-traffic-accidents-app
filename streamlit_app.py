import streamlit as st
import pandas as pd

st.title("Leeds Traffic Accidents")
st.write(
    "Accidents"
)

data =  pd.read_csv("Traffic%20accidents_2019_Leeds.csv")
#st.write(df)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Accidents Throughout 2019")
    st.line_chart(data.set_index('Accident Date')[''])

with col2:
    st.subheader("Total of Each Type Within 2019")
    st.bar_chart(data.set_index('Accident Date')[''])