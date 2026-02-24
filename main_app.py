import streamlit as st
import pandas as pd

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Dental Clinic - Growth & Data Science Dashboard",
    page_icon="🦷",
    layout="wide"
)

# --- VERİ YÜKLEME (KPI Metrikleri İçin) ---
@st.cache_data
def get_summary_metrics():
    df = pd.read_csv("master_lead_dataframe.csv")
    total_leads = len(df)
    total_spend = df['spend_per_lead'].sum()
    avg_cpl = df['spend_per_lead'].mean()
    conversion_rate = (df['status'] == 'Won').mean() * 100
    return total_leads, total_spend, avg_cpl, conversion_rate

try:
    t_leads, t_spend, a_cpl, conv_rate = get_summary_metrics()
except:
    # Eğer henüz CSV oluşmadıysa hata vermemesi için placeholder değerler
    t_leads, t_spend, a_cpl, conv_rate = 0, 0, 0, 0

# --- ANA SAYFA TASARIMI ---

# Header Alanı
st.title("🦷 Dental Clinic: Performans & Veri Bilimi Dashboard")
st.subheader("Pazarlama ve Satış Süreçlerinin Veri Odaklı Optimizasyonu")

st.divider()

# --- ÜST SEVİYE METRİKLER (KPI CARDS) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Toplam Lead", value=t_leads)
with col2:
    st.metric(label="Toplam Pazarlama Harcaması", value=f"£{t_spend:,.0f}")
with col3:
    st.metric(label="Ortalama CPL (Lead Maliyeti)", value=f"£{a_cpl:.2f}")
with col4:
    st.metric(label="Satış Dönüşüm Oranı (Won %)", value=f"%{conv_rate:.1f}")

st.divider()

# --- PROJE DETAYLARI VE VİZYON ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("""
    ### 🎯 Projenin Amacı
    Bu dashboard, **Land of Smile** diş kliniğinin İngiltere (UK) pazarındaki büyüme stratejisini desteklemek amacıyla geliştirilmiştir. 
    Klasik reklam raporlamasının ötesine geçerek; reklam verilerini (Google/Meta), web davranışlarını (GTM) ve satış sonuçlarını (CRM) bir araya getirir.

    **Temel Hedefler:**
    * **Churn Tahminleme:** Form dolduran hastaların hangilerinin süreci terk edeceğini önceden saptamak.
    * **Nitelikli Lead Skorlama:** Bütçeyi sadece form getiren değil, "uçağa binip Antalya'ya gelecek" hastaları getiren kanallara odaklamak.
    * **İçerik Stratejisi:** Hangi tedavilerin ve içerik kümelerinin daha yüksek sadakat sağladığını belirlemek.
    """)

with right_col:
    st.info("### 🛠️ Kullanılan Teknolojiler")
    st.markdown("""
    - **Dil:** Python 3.10+
    - **Veri İşleme:** Pandas, NumPy
    - **Görselleştirme:** Plotly, Streamlit
    - **Makine Öğrenmesi:** Scikit-Learn (Random Forest)
    - **Tracking:** GTM & DataLayer Architecture
    """)

st.divider()
st.markdown("""
    ### Sonraki adımlar:
    - **AB Test senaryo üretimi:** Web'de ilgili içeriği düzenli Agentic olarak tarayarak hastaların çekinceleri, eleştiri, yasal zorluklar gibi pain pointleri belirleyip bunlara yönelik test senaryoları hazırlamak   
    - **Satış kısmı:** Hasta ile ilk iletişimden itibaren AI-Agent destekli iletişim (mesajlarda endişe, korku, fiyat/hizmet kalitesi duyarlılık gibi çıkarımlar ile satış danışmanının desteklenmesi)
    - **7/24 AI agent:** Sürecin tamamında sorulara web sitesindeki bilgiler ile cevap verebilecek yapay zeka ajan. 
    """)
st.divider()



st.success("👈 Devam etmek için sol taraftaki menüden bir sayfa seçiniz.")