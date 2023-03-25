import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Text
from bokeh.util.compiler import TypeScript

st.header('Checking for Peak Interferences')

tab1, tab2 = st.tabs(['visual', 'numeric'])

with tab1:
    def sel_el(selEl): 
        el = df[(df['El'] == selEl)]
        x = el['Energy (keV)'].values
        y = el['I'].values
        label = el['Line'].values
        return x, y, label

    df = pd.read_csv('data/transition_energies.csv')
    elements = sorted(set(df['El'].values))

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
    st.write('coming')


