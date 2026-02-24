import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Explorer - Raw Tables", layout="wide")

# Verileri Yükle
ad_df = pd.read_csv("ad_performance_table.csv")
sales_df = pd.read_csv("sales_pipeline_table.csv")
web_df = pd.read_csv("web_behavior_table.csv")
master_df = pd.read_csv("master_lead_dataframe.csv")

st.title("🗄️ Veri Kaynakları ve Ham Tablolar")
st.markdown("""
Bu sayfa, farklı sistemlerden gelen verilerin **'Normalize'** edilmeden önceki ham hallerini ve birleştirilmiş ana tabloyu içerir.
""")

tab1, tab2, tab3, tab4 = st.tabs([
    "📢 Reklam Paneli",
    "🤝 CRM (Satış)",
    "🌐 Web Davranış",
    "💎 MASTER DATAFRAME"
])

with tab1:
    st.subheader("Meta & Google Ads Ham Verisi")
    st.dataframe(ad_df.head(10), use_container_width=True)

with tab2:
    st.subheader("CRM Satış Boru Hattı")
    st.dataframe(sales_df.head(10), use_container_width=True)

with tab3:
    st.subheader("GTM / Google Analytics 4 Event Verileri")
    st.dataframe(web_df.head(10), use_container_width=True)

with tab4:
    st.subheader("Analize Hazır Birleştirilmiş Veri (Joined)")
    st.success(f"Toplam {len(master_df)} satır veri analize hazır hale getirildi.")

    # Küçük bir interaktif filtre ekleyelim
    platform_filter = st.multiselect("Platforma Göre Filtrele", options=master_df['platform'].unique(),
                                     default=master_df['platform'].unique())
    filtered_df = master_df[master_df['platform'].isin(platform_filter)]

    st.dataframe(filtered_df, use_container_width=True)