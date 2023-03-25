import streamlit as st
import pandas as pd
from PIL import Image

st.sidebar.markdown(f'''<a href='http://geoplatform.de'><button style="background-color:LightBlue;">Back to DataPro</button></a>''',unsafe_allow_html=True)

st.session_state.df = pd.read_csv('data/epma_standards.csv')
elements = st.session_state.df.columns[10:129].tolist()

tab1, tab2 = st.tabs(['Elements', 'Images'])

with tab1:
    colel1_1, colel1_2 = st.columns([1,3])
    with colel1_1:
        st.session_state.el1 = st.selectbox('Select Element', elements, index=8)
    with colel1_2:
        st.session_state.el1_range = st.slider('sel', .0, 100.0, (0., 100.))
    
    df1 = st.session_state.df
    df1.insert(2, st.session_state.el1+' ', st.session_state.df[st.session_state.el1])
    fil = (df1[st.session_state.el1] > st.session_state.el1_range[0]) & (df1[st.session_state.el1] < st.session_state.el1_range[1])
    st.dataframe(df1[fil].drop('ID',axis=1))

    with st.expander('The entire standards table'):
        st.dataframe(st.session_state.df)
    
with tab2:
    st.session_state.std_name = st.selectbox('Select Standard', ['Block 3', 'NBS Metals', 'Astimex', '3R', 'Current Standard Holder', 'Block 4', 'NIST NBS Glasses'], index=4
                                             )
    image = Image.open('data/std_images/' + st.session_state.std_name + '.png')
    st.image(image, caption=st.session_state.std_name)