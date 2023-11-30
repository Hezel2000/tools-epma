import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Text

st.header('Checking for Peak Interferences')

st.sidebar.link_button('Epicenter','http://geoplatform.de')

st.session_state.df = pd.read_csv('data/transition_energies.csv')
elements = sorted(set(st.session_state.df['El'].values))
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

tab1, tab2, tab3, tab4 = st.tabs(['visual', 'numeric', 'interferences', 'recipe'])

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

    col1, col2, col3 = st.columns([1,1,4])
    with col1:
        st.session_state.el = st.selectbox('Element', elements, index = 44)

    with col2:
        st.session_state.spec = st.selectbox('Spectrometer', ['S1-4', 'S5'], index = 0)
        if st.session_state.spec == 'S1-4':
            st.session_state.specConst = 2800
        else:
            st.session_state.specConst = 2000
    
    with col3:
        st.session_state.analysor_crystal = st.multiselect('Analyser Crystal', st.session_state.crystalID)
    

    el = st.session_state.df[(st.session_state.df['El'] == st.session_state.el)]
    energies = el['Energy (keV)']
    line_labels = el['Line']
    line_intensity = el['I']
    
    # convert energies into wavelengths in SI units (-> m) & in nm  # convert wavelengths from m to nm
    waveLengths = ((const_h * const_c / (1000 * const_eVtoJoule * energies)) * 10**9).rename('lambda (nm)')

    st.session_state.df2 = pd.concat([line_labels, line_intensity, energies, waveLengths], axis=1)

    for i in st.session_state.analysor_crystal:
        mm = waveLengths * st.session_state.specConst/st.session_state.crystalID[i]
        mm.mask((mm < mmRange[0]) | (mm > mmRange[1]), '', inplace=True)
        st.session_state.df2[i] = mm.apply(lambda col:pd.to_numeric(col, errors='coerce'))

    st.dataframe(st.session_state.df2.round(3))

with tab3:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.session_state.el_interference = st.selectbox('Element to check', elements, index = 44)
    with col2:
        st.session_state.el_interference_line = st.selectbox('Element line', st.session_state.df[st.session_state.df['El'] == st.session_state.el_interference]['Line'])
    with col3:
        st.session_state.interference_intervall = st.number_input('±interval', value = 100)
    with col4:
        st.session_state.interference_unit = st.selectbox('Unit', ['keV', 'mm'])
    with col5:
        st.session_state.interference_crystal = st.selectbox('analyser crystal', list(st.session_state.crystalID.keys()))
    
    fil_int_energy = (st.session_state.df['El'] == st.session_state.el_interference) & (st.session_state.df['Line'] == st.session_state.el_interference_line)
    st.session_state.interference_energy = st.session_state.df[fil_int_energy]['Energy (keV)'].values[0]
    
    fil_int = (st.session_state.df['Energy (keV)'] < st.session_state.interference_energy + .001 * st.session_state.interference_intervall) & (st.session_state.df['Energy (keV)'] > st.session_state.interference_energy - .001 * st.session_state.interference_intervall)
    st.write('Energy of '+st.session_state.el_interference+ st.session_state.el_interference_line + ': ' + str(st.session_state.interference_energy.round(3)) + ' ' + st.session_state.interference_unit)

    st.write(st.session_state.df[fil_int])#[st.session_state.df[fil_int] == st.session_state.interference_crystal])

with tab4:
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        s1_rec = st.multiselect('S1', elements)
    with col2:
        s2_rec = st.multiselect('S2', elements)
    with col3:
        s3_rec = st.multiselect('S3', elements)
    with col4:
        s4_rec = st.multiselect('S4', elements)
    with col5:
        s5_rec = st.multiselect('S5', elements)
        

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(s1_rec)
        with st.expander("See explanation"):
            st.write(s1_rec)
    
    with col2:
        st.write(s2_rec)
    
    with col3:
        st.write(s3_rec)

    with col4:
        st.write(s4_rec)
    
    with col5:
        st.write(s5_rec)