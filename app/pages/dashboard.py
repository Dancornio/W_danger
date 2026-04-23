import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="dashboard painel", layout="wide")
st.title(":material/analytics: Violeta Analytics")
st.markdown(
    "Explore os dados de feminicídio e violência doméstica nos estados do Brasil utilizando os filtros disponíveis. \n"
    "\n Interaja com os gráficos para obter " f"**insights** " "sobre os dados."
)

with st.sidebar:
    st.title(":material/filter_alt: Filters")


