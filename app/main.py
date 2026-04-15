from pathlib import Path

import plotly.express as px
import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu


from app.core.data import load_dataset


st.set_page_config(
	page_title="Violeta Analytics",
	page_icon="\U0001f7e3",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.markdown(
	"""
	<style>
	  .stApp {
		background: radial-gradient(circle at 5% 10%, #f0ebff 0%, #f6f3ff 35%, #f8f7ff 100%);
	  }
	  section[data-testid="stSidebar"] {
		background: linear-gradient(180deg, #f1e9ff 0%, #e8dcff 100%);
		border-right: 1px solid rgba(111, 82, 217, 0.2);
	  }
	  .block-container {
		padding-top: 1.2rem;
		padding-bottom: 1.2rem;
	  }
	</style>
	""",
	unsafe_allow_html=True,
)

with st.sidebar:
	selected = option_menu(
        menu_title="Menu",
        options=["Home", "Dashboard", "Sobre", "Contato"],
        icons=["house", "bar-chart", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
		styles={
			"container": {
				"padding": "0.2rem 0.25rem",
				"background-color": "rgba(255, 255, 255, 0.45)",
				"border": "1px solid rgba(111, 82, 217, 0.28)",
				"border-radius": "12px",
			},
			"menu-title": {
				"color": "#3f2c74",
				"font-size": "1.05rem",
				"font-weight": "700",
			},
			"icon": {
				"color": "#6f52d9",
				"font-size": "1rem",
			},
			"nav-link": {
				"font-size": "0.95rem",
				"text-align": "left",
				"margin": "0.15rem 0",
				"padding": "0.5rem 0.6rem",
				"color": "#433267",
				"border-radius": "8px",
				"--hover-color": "#ddccff",
			},
			"nav-link-selected": {
				"background": "linear-gradient(90deg, #8a68f2 0%, #6f52d9 100%)",
				"color": "#ffffff",
				"font-weight": "600",
			},
        }
    )

if selected == "Sobre":
	st.title("Sobre o projeto")
	st.markdown(
		"""
		Este projeto foi desenvolvido com o propósito de aplicar técnicas de análise de dados e desenvolvimento de interfaces utilizando Python e Streamlit. 
		O objetivo é fornecer um dashboard interativo que transforma dados brutos de segurança pública em insights visuais claros. 
		A ferramenta permite a exploração detalhada de registros de mortes violentas no estado, 
		facilitando a identificação de tendências temporais, áreas de maior incidência e tipologias criminais predominantes. 
		Toda a análise é fundamentada em microdados reais e abertos, disponibilizados por fontes governamentais.
		
		O Dashboard utiliza fontes de dados reais disponibilizadas pelo governo publicamente.
		"""
	)
	st.info("Para mais informações, entre em contato: ammon@tutamail.com.")
elif selected == "Contato":
	st.title("Contato")
	st.markdown(
		"""
		Para entrar em contato, envie um e-mail para: ammon@tutamail.com
		"""
	)
elif selected == "Dashboard":
	st.title("Dashboard")
	st.caption("Fonte: mortes_violentas_estado.csv")

	csv_real = Path(__file__).resolve().parents[1] / "data" / "raw" / "mortes_violentas_estado.csv"
	df = load_dataset(csv_real)

	mensal = df.groupby("PERIODO", as_index=False)["QT_VITIMAS"].sum()
	mensal["PERIODO"] = mensal["PERIODO"].dt.strftime("%Y-%m")

	fig = px.line(
		mensal,
		x="PERIODO",
		y="QT_VITIMAS",
		markers=True,
		color_discrete_sequence=["#6f52d9"],
		labels={"PERIODO": "Periodo (ano-mes)", "QT_VITIMAS": "Vitimas"},
		title="Total mensal de vitimas no estado",
	)
	fig.update_traces(line=dict(width=3), marker=dict(size=6))
	fig.update_layout(
		margin=dict(l=8, r=8, t=56, b=8),
		plot_bgcolor="rgba(255,255,255,0.65)",
		paper_bgcolor="rgba(255,255,255,0)",
	)

	st.plotly_chart(fig, use_container_width=True)

