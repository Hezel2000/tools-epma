import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Upload an excel file with a 'targt' and a 'source' sheet in it")
if uploaded_file is not None:
    target = pd.read_excel(uploaded_file, 'target')
    source = pd.read_excel(uploaded_file, 'source')
    merged = pd.merge(target, source, how='outer')
    st.dataframe(merged)

