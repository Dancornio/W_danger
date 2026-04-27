from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import plotly.graph_objects as go


st.markdown(
	"""
    <style>
	</style>
	""",
	
    unsafe_allow_html=True,
)

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "estupros-ipea.csv"


@st.cache_data(show_spinner=False)
def load_estupros_data(csv_path: Path = DATA_PATH) -> pd.DataFrame:
	df = pd.read_csv(csv_path, sep=";", encoding="utf-8")

	df = df.rename(
		columns={
			"cod": "cod",
			"nome": "estado",
			"período": "ano",
			"valor": "casos",
		}
	)

	df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
	df["casos"] = pd.to_numeric(df["casos"], errors="coerce")
	df = df.dropna(subset=["estado", "ano", "casos"]).copy()
	df["ano"] = df["ano"].astype(int)
	df["casos"] = df["casos"].astype(int)

	return df


def format_int(value: int) -> str:
	return f"{value:,}".replace(",", ".")


def format_pct(value: float) -> str:
	return f"{value:.2f}%".replace(".", ",")


def sort_table(df: pd.DataFrame, by: str | list[str], ascending: bool = True) -> pd.DataFrame:
	keys = [by] if isinstance(by, str) else by
	records = df.to_dict("records")

	# Stable multi-key sort without relying on pandas sort_values type overloads.
	for key in reversed(keys):
		records = sorted(records, key=lambda row: row[key], reverse=not ascending)

	return pd.DataFrame.from_records(records)


def build_metrics(df: pd.DataFrame) -> dict[str, str]:
	ano_min = int(df["ano"].min())
	ano_max = int(df["ano"].max())

	total_periodo = int(df["casos"].sum())

	total_por_ano = sort_table(
		df.groupby("ano", as_index=False).agg(casos=("casos", "sum")),
		by="ano",
	)
	total_inicio = int(total_por_ano.loc[total_por_ano["ano"] == ano_min, "casos"].iloc[0])
	total_fim = int(total_por_ano.loc[total_por_ano["ano"] == ano_max, "casos"].iloc[0])
	anos = ano_max - ano_min
	cagr = (((total_fim / total_inicio) ** (1 / anos)) - 1) * 100 if anos > 0 else 0.0

	ranking_estados = sort_table(
		df.groupby("estado", as_index=False).agg(casos=("casos", "sum")),
		by="casos",
		ascending=False,
	)
	top_estado = ranking_estados.iloc[0]
	top_share = (top_estado["casos"] / total_periodo) * 100

	return {
		"intervalo": f"{ano_min} - {ano_max}",
		"total_periodo": format_int(total_periodo),
		"cagr": format_pct(cagr),
		"top_estado": f"{top_estado['estado']} ({format_int(int(top_estado['casos']))})",
		"top_share": format_pct(top_share),
	}


st.title(":material/home: Home")
st.subheader("Indicadores e insights - Estupros (IPEA)")
st.caption(f"Fonte: {DATA_PATH.name}")

if not DATA_PATH.exists():
	st.error(f"Arquivo nao encontrado em: {DATA_PATH}")
	st.stop()

df = load_estupros_data(DATA_PATH)
metrics = build_metrics(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Periodo", metrics["intervalo"])
col2.metric("Total no periodo", metrics["total_periodo"])
col3.metric("Crescimento medio anual", metrics["cagr"])
col4.metric("Estado com maior volume", metrics["top_estado"], delta=f"{metrics['top_share']} do total")

st.divider()

anual = sort_table(df.groupby("ano", as_index=False).agg(casos=("casos", "sum")), by="ano")
anual["variacao_%"] = anual["casos"].pct_change() * 100

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
	fig_tendencia = px.line(
		anual,
		x="ano",
		y="casos",
		markers=True,
		title="Evolucao anual de casos (Brasil)",
		labels={"ano": "Ano", "casos": "Numero de casos"},
		color_discrete_sequence=["#6f52d9"],
	)
	fig_tendencia.update_traces(line=dict(width=3), marker=dict(size=7))
	fig_tendencia.update_layout(margin=dict(l=8, r=8, t=56, b=8))
	st.plotly_chart(fig_tendencia, width='content')

with chart_col2:
	fig_yoy = px.bar(
		anual.dropna(subset=["variacao_%"]),
		x="ano",
		y="variacao_%",
		title="Variacao percentual ano a ano (YoY)",
		labels={"ano": "Ano", "variacao_%": "Variacao %"},
		color="variacao_%",
		color_continuous_scale="Purp",
	)
	fig_yoy.update_layout(margin=dict(l=8, r=8, t=56, b=8), coloraxis_showscale=False)
	st.plotly_chart(fig_yoy, width='content')

st.divider()

top_n = st.slider("Top estados no ranking", min_value=5, max_value=15, value=10, step=1)

ranking = (
	sort_table(
		df.groupby("estado", as_index=False).agg(casos=("casos", "sum")),
		by="casos",
		ascending=False,
	).head(top_n)
)

fig_ranking = px.bar(
	ranking.sort_values("casos"),
	x="casos",
	y="estado",
	orientation="h",
	title=f"Ranking de estados por volume acumulado (Top {top_n})",
	labels={"casos": "Numero de casos (2011-2016)", "estado": "Estado"},
	color="casos",
	color_continuous_scale="Purp",
)
fig_ranking.update_layout(margin=dict(l=8, r=8, t=56, b=8), coloraxis_showscale=False)
st.plotly_chart(fig_ranking, width='stretch')

st.divider()

top5_estados = (
	sort_table(
		df.groupby("estado", as_index=False).agg(casos=("casos", "sum")),
		by="casos",
		ascending=False,
	).head(5)["estado"].tolist()
)
estados_disponiveis = sorted(df["estado"].unique().tolist())

estados_sel = st.multiselect(
	"Selecione estados para comparar a evolucao anual",
	options=estados_disponiveis,
	default=top5_estados,
)

if estados_sel:
	evolucao_estados = sort_table(
		df[df["estado"].isin(estados_sel)]
		.groupby(["ano", "estado"], as_index=False)
		.agg(casos=("casos", "sum")),
		by=["estado", "ano"],
	)

	fig_estados = px.line(
		evolucao_estados,
		x="ano",
		y="casos",
		color="estado",
		markers=True,
		title="Evolucao anual por estado",
		labels={"ano": "Ano", "casos": "Numero de casos", "estado": "Estado"},
        color_discrete_sequence=["#6f52d9", "#d95f02", "#1b9e77", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#fdbf6f", "#ff7f00"],
	)
	fig_estados.update_layout(margin=dict(l=8, r=8, t=56, b=8), legend_title_text="Estado")
	st.plotly_chart(fig_estados, width='stretch')
else:
	st.info("Selecione ao menos um estado para exibir o grafico de evolucao.")


st.subheader("Mapa de casos por estado")
ano_mapa = st.select_slider(
	"Ano para o mapa",
	options=sorted(df["ano"].unique().tolist()),
	value=int(df["ano"].max()),
)

mapa_df = (
	df[df["ano"] == ano_mapa]
	.groupby("estado", as_index=False)
	.agg(casos=("casos", "sum"))
)

url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
brasil_geojson = requests.get(url_geojson, timeout=30).json()

fig = go.Figure(
	data=go.Choropleth(
		locations=mapa_df["estado"],
		z=mapa_df["casos"],
		geojson=brasil_geojson,
		featureidkey="properties.sigla",
		colorscale="Purples",
		text=mapa_df["estado"],
		hovertemplate="<b>%{text}</b><br>Casos: %{z:,}<extra></extra>",
		colorbar=dict(title=f"Casos ({ano_mapa})"),
	)
)

fig.update_layout(
	title=f"Casos de estupro por estado - {ano_mapa}",
	geo=dict(
		scope="south america",
		projection_type="mercator",
		showland=True,
		landcolor="rgb(243, 243, 243)",
	),
	margin=dict(l=8, r=8, t=56, b=8),
	height=650,
)

st.plotly_chart(fig, width='stretch')



st.caption(
	"Observacao: os valores sao absolutos e podem refletir variacoes de registro/notificacao ao longo do tempo."
)
