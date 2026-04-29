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

    selected_categoria = st.selectbox(
        "Selecione a categoria para análise:",
        options=[
            "Feminicídio",
            "Violência Doméstica",
        ]
    )

    selected_estado = st.multiselect(
        "Selecione os estados para análise:",
        options=["BA", "MG", "DF"],
    )

