from pathlib import Path
import pandas as pd
import streamlit as st


MONTH_MAP = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}


def default_dataset_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "raw" / "mortes_violentas_estado.csv"


@st.cache_data(show_spinner=False)
def load_dataset(csv_path: str | Path | None = None) -> pd.DataFrame:
    path = Path(csv_path) if csv_path else default_dataset_path()
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de dados nao encontrado: {path}")

    df = pd.read_csv(path, encoding="latin-1")

    for col in ["ANO", "MES", "QT_VITIMAS"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["ANO", "MES", "QT_VITIMAS"])
    df["ANO"] = df["ANO"].astype(int)
    df["MES"] = df["MES"].astype(int).clip(1, 12)
    df["QT_VITIMAS"] = df["QT_VITIMAS"].astype(int)
    df["MES_NOME"] = df["MES"].map(MONTH_MAP)
    df["PERIODO"] = pd.to_datetime(
        {"year": df["ANO"], "month": df["MES"], "day": 1},
        errors="coerce",
    )

    return df


def filter_dataset(
    df: pd.DataFrame,
    years: list[int],
    regions: list[str],
    natures: list[str],
) -> pd.DataFrame:
    mask = df["ANO"].isin(years) & df["REGIAO"].isin(regions) & df["GR_NATUREZA"].isin(natures)
    return df.loc[mask].copy()
