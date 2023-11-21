import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.link_button('Epicenter','http://geoplatform.de')

st.session_state.el = 'Fe'
st.session_state.scale = 'linear'
st.session_state.unit_mag = 'eV'

df = pd.read_csv('data/electron binding energies.csv')
elements = df.columns[2:].tolist()

def abc(el, scale, unit_mag, shell):
    if unit_mag == 'eV':
        um_mult = -1
        disp_unit = 'eV'
    else:
        um_mult = -.001
        disp_unit = 'keV'
    df1 = df[['shell', 'x_pos', el,]]
    df1.loc[:, el]=um_mult * df1.loc[:, el]
    df1.dropna()
    energyLevels = [x for x in df1[el]]
    fig, ax = plt.subplots(figsize=(2,4))
    _=[ax.axhline(y=i, xmin=.1, xmax=1, linestyle='--') for i in energyLevels]
    ax.set_ylim(1.1*min(energyLevels), .9*max(energyLevels))    
    ax.set_ylabel('Energy ('+disp_unit+')')
    ax.set_yscale('linear')
    if scale == 'log':
        ax.set_yscale('symlog')
    else:
        ax.set_yscale('linear')
    l = []
    for ind in df1.index:
        l.append([df1['shell'][ind], df1['x_pos'][ind], df1[el][ind]])
    if shell == 'orbital':
        _=[ax.text(i[1], i[2], i[0], fontsize=7) for i in l]
    else:
        _=[ax.text(i[1], i[2], round(i[2], 2), fontsize=7) for i in l]
    ax.set_xticks([])
    ax.spines[['bottom', 'top', 'right']].set_visible(False)
    return fig


col1, col2 = st.columns([1, 4])

with col1:
    st.session_state.el = st.selectbox('Element', elements, index=25)
    st.session_state.scale = st.radio('Scale', ['linear', 'log'])
    st.session_state.unit_mag = st.radio('Unit', ['eV', 'keV'], index=1)
    st.session_state.shell = st.radio('Shell info', ['orbital', 'energy'], index=0)

with col2:
    st.pyplot(abc(st.session_state.el, st.session_state.scale, st.session_state.unit_mag, st.session_state.shell))
