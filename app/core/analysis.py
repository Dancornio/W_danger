import pandas as pd


def build_kpis(df: pd.DataFrame) -> dict[str, int | float | str]:
	total_vitimas = int(df["QT_VITIMAS"].sum())
	municipios_afetados = int(df["MUNICIPIO"].nunique())
	periodos = max(int(df[["ANO", "MES"]].drop_duplicates().shape[0]), 1)
	media_mensal = float(total_vitimas / periodos)

	natureza_lider = "-"
	if not df.empty:
		natureza_lider = (
			df.groupby("GR_NATUREZA", as_index=False)["QT_VITIMAS"]
			.sum()
			.sort_values("QT_VITIMAS", ascending=False)
			.iloc[0]["GR_NATUREZA"]
		)

	return {
		"total_vitimas": total_vitimas,
		"municipios_afetados": municipios_afetados,
		"media_mensal": media_mensal,
		"natureza_lider": natureza_lider,
	}


def monthly_series(df: pd.DataFrame) -> pd.DataFrame:
	out = (
		df.groupby("PERIODO", as_index=False)["QT_VITIMAS"]
		.sum()
		.sort_values("PERIODO")
	)
	out["ROTULO"] = out["PERIODO"].dt.strftime("%b/%Y")
	return out


def by_region(df: pd.DataFrame) -> pd.DataFrame:
	return (
		df.groupby("REGIAO", as_index=False)["QT_VITIMAS"]
		.sum()
		.sort_values("QT_VITIMAS", ascending=False)
	)


def by_nature(df: pd.DataFrame, top_n: int = 6) -> pd.DataFrame:
	return (
		df.groupby("GR_NATUREZA", as_index=False)["QT_VITIMAS"]
		.sum()
		.sort_values("QT_VITIMAS", ascending=False)
		.head(top_n)
	)


def top_municipalities(df: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
	return (
		df.groupby("MUNICIPIO", as_index=False)["QT_VITIMAS"]
		.sum()
		.sort_values("QT_VITIMAS", ascending=False)
		.head(top_n)
	)
