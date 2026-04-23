import streamlit as st


st.set_page_config(page_title="About")
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