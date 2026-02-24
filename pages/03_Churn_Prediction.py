import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="ML - Churn Prediction", layout="wide")

st.title("🤖 Makine Öğrenmesi ile Churn Tahminleme")
st.markdown("""
Bu model, geçmiş verileri kullanarak bir müşteri adayının süreci terk etme (churn) olasılığını hesaplar. 
Satış ekibi bu tahminleri kullanarak **yüksek potansiyelli lead'lere** öncelik verebilir.
""")


# Veriyi Yükle
@st.cache_data
def load_and_train():
    df = pd.read_csv("master_lead_dataframe.csv")

    # Feature Engineering: Basit bir model için sayısal ve boolean sütunları seçiyoruz
    features = ['spend_per_lead', 'lead_quality_score', 'scroll_depth_pct', 'session_duration_sec', 'x_ray_status']
    X = df[features]
    y = df['is_churn']

    # Model Eğitimi
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, features


model, feature_names = load_and_train()

# --- SIDEBAR: KULLANICI GİRİŞİ ---
st.sidebar.header("📋 Yeni Lead Bilgileri")
st.sidebar.write("Tahminleme için değerleri ayarlayın:")


def user_input():
    spend = st.sidebar.slider('Lead Edinme Maliyeti (£)', 20, 150, 80)
    quality = st.sidebar.select_slider('Satış Ekibi Puanı (1-3)', options=[1, 2, 3], value=2)
    scroll = st.sidebar.slider('Site Kaydırma Derinliği (%)', 0, 100, 65)
    duration = st.sidebar.slider('Sitede Kalma (Saniye)', 30, 600, 250)
    xray = st.sidebar.checkbox('Röntgen Gönderdi mi?', value=True)

    data = {
        'spend_per_lead': spend,
        'lead_quality_score': quality,
        'scroll_depth_pct': scroll,
        'session_duration_sec': duration,
        'x_ray_status': xray
    }
    return pd.DataFrame(data, index=[0])


input_df = user_input()

# --- TAHMİNLEME BÖLÜMÜ ---
col1, col2 = st.columns([1, 1])

prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)

with col1:
    st.subheader("Tahmin Sonucu")
    if prediction[0] == 1:
        st.error("⚠️ YÜKSEK CHURN RİSKİ")
        st.write("Bu adayın vazgeçme olasılığı oldukça yüksek. Acil geri kazanım stratejisi gerekebilir.")
    else:
        st.success("✨ DÜŞÜK CHURN RİSKİ (POTANSİYEL SATIŞ)")
        st.write("Bu aday satışa çok yakın. Randevu onayı için odaklanılmalı.")

    # Güven Skoru
    prob = prediction_proba.max() * 100
    st.progress(int(prob))
    st.write(f"Model Güveni: %{prob:.1f}")

with col2:
    st.subheader("Neden Bu Tahmin?")
    # Feature Importance görselleştirmesi
    importance = pd.DataFrame({
        'Özellik': feature_names,
        'Etki Skoru': model.feature_importances_
    }).sort_values(by='Etki Skoru', ascending=True)

    fig_imp = pd.DataFrame(importance)
    st.bar_chart(data=importance, x='Özellik', y='Etki Skoru', horizontal=True)

st.divider()

# --- SENARYO ANALİZİ ---
st.subheader("💡 Stratejik Aksiyon Önerisi")
if prediction[0] == 1 and input_df['x_ray_status'][0] == False:
    st.warning(
        "Bu aday röntgen göndermemiş. Satış ekibi indirim teklif etmek yerine 'Ücretsiz Röntgen Analizi' randevusu vermeye çalışmalı.")
elif prediction[0] == 0:
    st.info(
        "Adayın sitede kalma süresi ve etkileşimi yüksek. VIP transfer ve otel detaylarını içeren bir teklif dosyası gönderilmesi dönüşümü hızlandıracaktır.")