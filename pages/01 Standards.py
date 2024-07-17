import streamlit as st
import pandas as pd
from PIL import Image

st.sidebar.link_button('Epicenter','http://geoplatform.de')

st.session_state.df = pd.read_csv('data/epma_standards.csv')
elements = st.session_state.df.columns[10:129].tolist()
unsorted_mineral_names = st.session_state.df['Mineral'].unique()
mineral_names = pd.Series(unsorted_mineral_names).sort_values()

tab1, tab2, tab3, tab4 = st.tabs(['Elements', 'Minerals', 'Holder', 'Entire table'])

with tab1:
    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        st.session_state.el1 = st.selectbox('Select Element', elements, index=8)
    with col2:
        built_in_only_el = st.checkbox('built in only', value = True, key = 'built_in_1')
    with col3:
        st.session_state.el1_range = st.slider('wt\%-range', .0, 100.0, (0., 100.))
    
    df1 = st.session_state.df
    df1.insert(2, st.session_state.el1+' ', st.session_state.df[st.session_state.el1])
    if built_in_only_el:
        fil = (df1[st.session_state.el1] > st.session_state.el1_range[0]) & (df1[st.session_state.el1] < st.session_state.el1_range[1]) & (df1['Built in'] == 'yes')
        st.dataframe(df1[fil].drop('ID',axis=1))
    else:
        fil = (df1[st.session_state.el1] > st.session_state.el1_range[0]) & (df1[st.session_state.el1] < st.session_state.el1_range[1])
        st.dataframe(df1[fil].drop('ID',axis=1))

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.mineral = st.selectbox('Select Mineral', mineral_names, key = 'built_in_2')
    with col2:
        built_in_only_min = st.checkbox('built in only', value = True)

    if built_in_only_min:
        fil = (st.session_state.df['Mineral'] == st.session_state.mineral) & (st.session_state.df['Built in'] == 'yes')
        st.dataframe(st.session_state.df[fil])
    else:
        fil = st.session_state.df['Mineral'] == st.session_state.mineral
        st.dataframe(st.session_state.df[fil])

with tab3:
    st.session_state.std_name = st.selectbox('Select Standard', ['Block 3', 'NBS Metals', 'Astimex', '3R', 'Current Standard Holder', 'Amphibole', 'Block 4', 'NIST NBS Glasses'], index=4
                                             )
    image = Image.open('data/std_images/' + st.session_state.std_name + '.png')
    st.image(image, caption=st.session_state.std_name)

with tab4:
    st.dataframe(st.session_state.df)