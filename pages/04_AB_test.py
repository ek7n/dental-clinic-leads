import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.power import TTestIndPower
import plotly.graph_objects as go

st.set_page_config(page_title="A/B Test Tasarımı & Analizi", layout="wide")

st.title("🧪 A/B Testi: Stratejik Planlama ve Güç Analizi")
st.markdown("""
Bu sayfa iki bağımsız modülden oluşur: 
1. **A Priori:** Test öncesi kaç kişiye ihtiyacımız var? 
2. **Posteriori:** Mevcut testimiz ne kadar güvenilir?
""")

# --- MODÜL 1: A PRIORI (ÖNSEL HESAPLAMA) ---
st.header("1️⃣ A Priori: Örneklem Planlaması")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Hedefler")
    target_conv_a = st.number_input("Baz Dönüşüm Oranı (A) %", value=5.0, step=0.5) / 100
    expected_uplift = st.slider("Hedeflenen Artış (Uplift) %", 5, 100, 20) / 100

    # Hedef B oranını hesapla
    target_conv_b = target_conv_a * (1 + expected_uplift)

    # Effect Size (Cohen's h) hesaplama
    h = 2 * (np.arcsin(np.sqrt(target_conv_b)) - np.arcsin(np.sqrt(target_conv_a)))

    power_gen = TTestIndPower()
    required_n = power_gen.solve_power(effect_size=h, alpha=0.05, power=0.80, ratio=1.0)

with col2:
    st.info(
        f"**Hipotez:** Varyant B'nin dönüşüm oranını %{target_conv_a * 100:.1f}'den %{target_conv_b * 100:.1f}'ye çıkarmasını bekliyoruz.")
    st.metric("Grup Başına Gereken Gözlem Sayısı", f"{int(np.ceil(required_n))} Hasta")
    st.write(
        "Bu sayı, %80 güç ve %5 anlamlılık düzeyi ile hedeflenen farkı yakalamak için gereken minimum kişi sayısıdır.")

st.divider()

# --- MODÜL 2: POSTERIORI (ARTÇIL GÜÇ HESAPLAMASI) ---
st.header("2️⃣ Posteriori: Gözlemlenen Güç Analizi")
cp1, cp2 = st.columns([1, 2])

with cp1:
    st.subheader("Gerçekleşen Veriler")
    current_n = st.number_input("Mevcut Örneklem (Grup Başına)", min_value=10, value=500)
    actual_a = st.slider("A Grubu Gerçekleşen %", 0.0, 20.0, 5.2) / 100
    actual_b = st.slider("B Grubu Gerçekleşen %", 0.0, 20.0, 7.1) / 100

    # Mevcut veriden effect size
    h_post = 2 * (np.arcsin(np.sqrt(actual_b)) - np.arcsin(np.sqrt(actual_a)))
    observed_power = power_gen.solve_power(effect_size=h_post, nobs1=current_n, alpha=0.05, ratio=1.0)

with cp2:
    st.subheader("Test Gücü Sonucu")
    fig_power = go.Figure(go.Indicator(
        mode="gauge+number",
        value=observed_power * 100,
        title={'text': "Gözlemlenen Güç (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2ECC71" if observed_power >= 0.8 else "#E74C3C"},
            'steps': [
                {'range': [0, 80], 'color': "#FADBD8"},
                {'range': [80, 100], 'color': "#D5F5E3"}]}
    ))
    st.plotly_chart(fig_funnel if 'fig_funnel' in locals() else fig_power, use_container_width=True)

    if observed_power < 0.8:
        st.warning(
            f"Dikkat: Test gücü hedef seviye olan %80'in altında (%{observed_power * 100:.1f}). Sonuçlar yanıltıcı olabilir.")
    else:
        st.success(f"Tebrikler: Test gücü %{observed_power * 100:.1f} ile güvenli seviyede.")