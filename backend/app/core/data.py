import pandas as pd
import streamlit as st


def carrega_dataset(url):
    try:
        food_consumption = pd.read_csv(url)
        return food_consumption
    except Exception:
        st.error(f"Erro ao carregar dados {Exception}")
        return None
