import streamlit as st
import pandas as pd
import plotly.graph_objects as go



st.divider()
st.header("📊 Sektörel Benchmark ve Mevcut Durum Analizi")
st.markdown("""
Aşağıdaki grafik, **Dental Clinic** performans verilerinin Birleşik Krallık (UK) Sağlık Turizmi pazarındaki genel benchmark değerleri ile kıyaslamasını gösterir.
""")


df = pd.read_csv("master_lead_dataframe.csv")
current_conv_rate = (df['status'] == 'Won').mean() * 100
current_cpl = df['spend_per_lead'].mean()

# Benchmark Değerleri
benchmarks = {
    "Won Rate (%)": {"current": current_conv_rate, "benchmark": 10.0, "goal": 15.0},
    "CPL (£)": {"current": current_cpl, "benchmark": 18.0, "goal": 12.0}
}

col_b1, col_b2 = st.columns(2)

with col_b1:
    # Won Rate Gauge Chart
    fig_gauge1 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = benchmarks["Won Rate (%)"]["current"],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Satış Dönüşüm Oranı (Won %)"},
        delta = {'reference': benchmarks["Won Rate (%)"]["benchmark"], 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [0, 20]},
            'bar': {'color': "#2ECC71"},
            'steps': [
                {'range': [0, 5], 'color': "#FADBD8"},
                {'range': [5, 10], 'color': "#D5F5E3"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': benchmarks["Won Rate (%)"]["benchmark"]}}))
    st.plotly_chart(fig_gauge1, use_container_width=True)

with col_b2:
    # CPL Gauge Chart (Düşük olması daha iyi olduğu için mantık ters)
    fig_gauge2 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = benchmarks["CPL (£)"]["current"],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Müşteri Edinme Maliyeti (CPL £)"},
        delta = {'reference': benchmarks["CPL (£)"]["benchmark"], 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [0, 40]},
            'bar': {'color': "#3498DB"},
            'steps': [
                {'range': [0, 12], 'color': "#D5F5E3"},
                {'range': [12, 18], 'color': "#FCF3CF"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': benchmarks["Won Rate (%)"]["benchmark"]}}))
    st.plotly_chart(fig_gauge2, use_container_width=True)

st.info(f"""
💡 **Analiz Notu:** UK pazarı için ortalama Won oranı %10, ideal CPL ise £18 altıdır. 
Şu anki verilerimize göre **Won oranımız %{current_conv_rate:.1f}** ile benchmarkın üzerindedir. 
Ancak **CPL değerimiz (£{current_cpl:.2f})** optimizasyona ihtiyaç duymaktadır.
""")

# Hiyerarşik Metriklerin Hesaplanması
total = len(df)
engaged = len(df[df['session_duration_sec'] > 120]) # 2 dk üzeri kalanlar (İlgi)
prospects = len(df[df['x_ray_status'] == True])     # Röntgen gönderenler (Güven)
won = len(df[df['status'] == 'Won'])                # Satış (Sonuç)

st.divider()
st.header("📉 Funnel Health: Metrik Hiyerarşisi ve Kayıp Analizi")
st.markdown("""
Bu hiyerarşi, bir kullanıcının web ziyaretçisinden hastaya dönüşme sürecindeki **progresif** adımları gösterir. 
Her aşama bir sonrakini besler; aradaki leakage bize hangi stratejiye odaklanmamız gerektiğini söyler.
""")

fig_funnel = go.Figure(go.Funnel(
    y = ["Toplam Lead", "Yüksek İlgi (120sn+)", "Güven (Röntgen Gönderen)", "Sonuç (Won)"],
    x = [total, engaged, prospects, won],
    textinfo = "value+percent initial",
    marker = {"color": ["#D6EAF8", "#85C1E9", "#3498DB", "#2874A6"]}
))

fig_funnel.update_layout(title_text="Dental Clinic - Dönüşüm Hunisi")
st.plotly_chart(fig_funnel, use_container_width=True)

st.info(f"""
### 🧐 Çıkarımlar:
1. **Farkındalık -> İlgi:** Toplam lead'lerin %{(engaged/total)*100:.1f}'i sitede derin vakit geçiriyor.
2. **İlgi -> Güven:** İlgi gösterenlerin %{(prospects/engaged)*100:.1f}'i röntgenini paylaşıyor. Bu, güven bariyerinin aşıldığı kritik adımdır.
3. **Güven -> Satış:** Röntgen gönderenlerin %{(won/prospects)*100:.1f}'i kliniğe geliyor.
""")