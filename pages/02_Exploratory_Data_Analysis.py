import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EDA - Derinlemesine Analiz", layout="wide")


# Veriyi Yükle
@st.cache_data
def load_data():
    # master_df içindeki veri tutarsızlıklarını temizleyerek yüklüyoruz
    df = pd.read_csv("master_lead_dataframe.csv")
    df.loc[df['status'] == 'Won', 'loss_reason'] = None
    return df


df = load_data()

st.title("🔍 Keşifçi Veri Analizi ve Lead İçgörüleri")
st.markdown("""
Bu analiz, pazarlama kanallarından gelen verilerin satış başarısı ve müşteri davranışı ile olan korelasyonunu ortaya koyar.
""")

# --- BÖLÜM 1: Platform Performansı ---
st.header("1. Reklam Kanalı ve Satış Verimliliği")
col1, col2 = st.columns([1, 1])

with col1:
    # Platform bazlı Status dağılımı
    fig_platform = px.histogram(df, x="platform", color="status",
                                barmode="group",
                                title="Platform Bazlı Satış Hunisi (Pipeline)",
                                labels={'status': 'Satış Durumu', 'platform': 'Kanal'},
                                color_discrete_map={'Won': '#2ECC71', 'Lost': '#E74C3C', 'Nurturing': '#F1C40F',
                                                    'No_Response': '#95A5A6'})
    st.plotly_chart(fig_platform, use_container_width=True)

with col2:
    # Harcama vs Won Oranı
    # Her platform için Won oranını hesaplayalım
    won_rates = df.groupby('platform')['status'].apply(lambda x: (x == 'Won').mean() * 100).reset_index()
    won_rates.columns = ['platform', 'won_rate']

    fig_won = px.bar(won_rates, x='platform', y='won_rate',
                     title="Hangi Kanal Daha Çok 'Satış' Getiriyor? (Won %)",
                     labels={'won_rate': 'Satış Oranı (%)'},
                     color='platform',
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_won, use_container_width=True)

st.divider()

# --- BÖLÜM 2: Davranışsal Analiz (Churn Sinyalleri) ---
st.header("2. Dijital Ayak İzleri ve Churn İlişkisi")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Röntgen Gönderiminin Etkisi")
    # Sunburst grafik: Röntgen durumu -> Status
    fig_sun = px.sunburst(df, path=['x_ray_status', 'status'],
                          color='x_ray_status',
                          color_discrete_map={True: '#27AE60', False: '#C0392B'},
                          title="Röntgen Gönderenler vs Göndermeyenlerin Final Durumu")
    st.plotly_chart(fig_sun, use_container_width=True)
    st.info("💡 **İçgörü:** Röntgen gönderen hastaların satışa dönme oranı istatistiksel olarak daha yüksektir.")

with col4:
    st.subheader("Sitede Kalma Süresi ve Churn Korelasyonu")
    # Box plot: Churn durumuna göre session duration
    fig_box = px.box(df, x="is_churn", y="session_duration_sec",
                     color="is_churn",
                     title="Sitede Kalma Süresi Churn'ü Tahmin Eder mi?",
                     labels={'is_churn': 'Churn (1: Evet, 0: Hayır)', 'session_duration_sec': 'Süre (Saniye)'},
                     color_discrete_map={0: '#2ECC71', 1: '#E74C3C'})
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# --- BÖLÜM 3: Tedavi ve Kayıp Analizi ---
st.header("3. Tedavi Türleri ve Kayıp Nedenleri")
c1, c2 = st.columns(2)

with c1:
    fig_treat = px.treemap(df, path=['treatment_type', 'status'],
                           title="Tedavi Türlerine Göre Lead Dağılımı")
    st.plotly_chart(fig_treat, use_container_width=True)

with c2:
    # Sadece Lost olanların nedenleri
    lost_df = df[df['status'] == 'Lost'].dropna(subset=['loss_reason'])
    if not lost_df.empty:
        fig_loss = px.pie(lost_df, names="loss_reason",
                          title="Müşterileri Neden Kaybediyoruz? (Churn Reasons)",
                          hole=0.4)
        st.plotly_chart(fig_loss, use_container_width=True)
    else:
        st.write("Henüz analiz edilecek kayıp nedeni verisi bulunmuyor.")

st.success("Analiz Tamamlandı. Bu veriler Churn Prediction modelini beslemek için kullanılacaktır.")