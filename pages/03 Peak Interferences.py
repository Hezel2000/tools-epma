import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Text

st.header('Checking for Peak Interferences')

st.session_state.df = pd.read_csv('data/transition_energies.csv')
elements = sorted(set(st.session_state.df['El'].values))

tab1, tab2 = st.tabs(['visual', 'numeric'])

with tab1:
    def sel_el(selEl): 
        el = st.session_state.df[(st.session_state.df['El'] == selEl)]
        x = el['Energy (keV)'].values
        y = el['I'].values
        label = el['Line'].values
        return x, y, label

    col1, col2 = st.columns([1, 5])

    with col1:
        st.session_state.el1 = st.selectbox('Element 1', elements, index = 75)
        st.session_state.el2 = st.selectbox('Element 2', elements, index = 44)

    with col2:
        x1, y1, label1 = sel_el(st.session_state.el1)
        x2, y2, label2 = sel_el(st.session_state.el2)
        label_source1 = ColumnDataSource(dict(x=x1, y=y1, text = label1))
        label_source2 = ColumnDataSource(dict(x=x2, y=y2, text = label2))
        glyph1 = Text(x="x", y="y", text="text", text_color="blue")
        glyph2 = Text(x="x", y="y", text="text", text_color="green")

        p = figure(x_axis_label = 'Energy (keV)', y_axis_label = 'Intensity (normalised to 100)')

        p.segment(x1, 0, x1, y1, color="blue", line_width=3, legend_label = st.session_state.el1)
        p.segment(x2, 0, x2, y2, color="green", line_width=3, legend_label = st.session_state.el2)
        p.add_glyph(label_source1, glyph1)
        p.add_glyph(label_source2, glyph2)

        st.bokeh_chart(p)

with tab2:
    const_h = 6.62607004 * 10**(-34)
    const_c = 299792458
    const_eVtoJoule = 1.602176634 * 10**(-19)
    #d-distance of the analystor-crystals in nm
    st.session_state.crystalID = {
    'TAP': 25.757,
    'PET': 8.742,
    'LIF': 4.0267,
    'LDE1': 60,
    'LDE2': 98,
    'LDE4': 40,
    'STE': 100.4
    }
    mmRange = [60, 260]

    col1, col2 = st.columns([1,4])
    with col1:
        st.session_state.el = st.selectbox('Element', elements, index = 44)
    with col2:
        st.session_state.analysor_crystal = st.multiselect('Analyser Crystal', st.session_state.crystalID)
    
    el = st.session_state.df[(st.session_state.df['El'] == st.session_state.el)]
    energies = el['Energy (keV)']
    line_labels = el['Line']
    
    # convert energies into wavelengths in SI units (-> m) & in nm  # convert wavelengths from m to nm
    waveLengths = ((const_h * const_c / (1000 * const_eVtoJoule * energies)) * 10**9).rename('lambda (nm)')

    st.session_state.df2 = pd.concat([line_labels, energies, waveLengths], axis=1)

    specConst1_4 = 2800   # Spec 1-4
    specConst5 = 2000   # Spec 5

    for i in st.session_state.analysor_crystal:
        mm = waveLengths * specConst1_4/st.session_state.crystalID[i]
        mm.mask(mm < mmRange[0], '', inplace=True)
        mm.mask(mm > mmRange[1], '', inplace=True)
        st.session_state.df2[i] = mm

    st.dataframe(st.session_state.df2.round(2))