import streamlit as st 

st.set_page_config(
    page_title="Violeta Analytics",
    page_icon="assets/violeta_logo.png",
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
            header[data-testid="stHeader"] {
                background: transparent !important;
                border-bottom: 0 !important;
            }
            [data-testid="stToolbar"] {
                background: transparent !important;
            }
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
                padding: 0.3rem;
            }
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
                border-radius: 8px;
                color: #433267;
            }
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
                background: #ddccff;
                color: #433267;
            }
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
                background: linear-gradient(90deg, #ac9ce6 0%, #6f52d9 100%);
                color: #ffffff;
                font-weight: 700;
            }
            .block-container {
                padding-top: 1.2rem;
                padding-bottom: 1.2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
)

pg = st.navigation(
    
    [
        
        st.Page(
            "pages/dashboard.py",
            title="Violeta Analytics",
            icon=":material/dashboard:",
            default=True,
        ),
        st.Page("pages/about.py", title="Sobre", icon=":material/info:"),
    ],
)
pg.run()

with st.sidebar:
    st.markdown(
        ":material/code: [streamlit-echarts](https://github.com/andfanilo/streamlit-echarts)"
    )
    st.caption("Made in :streamlit: by [Ammon](https://www.linkedin.com/in/omoura/)")

