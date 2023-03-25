import streamlit as st
import pandas as pd

df = pd.read_csv('data/epma_standards.csv')
elements = df.columns[10:129].tolist()

colel1_1, colel1_2 = st.columns([1,3])
with colel1_1:
    st.session_state.el1 = st.selectbox('Element', elements, index=8)
with colel1_2:
    st.session_state.el1_range = st.slider('sel', .0, 100.0, (0., 100.))

fil = (df[st.session_state.el1] > st.session_state.el1_range[0]) & (df[st.session_state.el1] < st.session_state.el1_range[1])
st.dataframe(df[fil])

with st.expander('full table'):
    st.dataframe(df)