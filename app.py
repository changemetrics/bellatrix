import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Dashboard Clínico - Bellatriz", layout="wide")
st.title("🐾 Dashboard Clínico Interativo - Bellatriz")
st.markdown("Acompanhamento da evolução laboratorial e resposta ao tratamento (Leishmaniose).")

# Dados estruturados
dados = {
    'Data': ['2026-06-06', '2026-06-16', '2026-07-10', '2026-08-01', '2026-08-12'],
    'Hematócrito': [24.0, 28.0, 37.6, 52.0, 48.0],
    'Leucócitos': [41.5, 6.5, 7.95, 9.2, 4.9],
    'Creatinina': [None, 1.0, 0.8, 1.7, 1.2],
    'Fósforo': [None, None, 5.8, 7.2, 7.0]
}
df = pd.DataFrame(dados)
df['Data'] = pd.to_datetime(df['Data'])

# Tratamento Glucantime
inicio_glucantime = '2026-06-08'
fim_glucantime = '2026-07-18'

st.subheader("🩸 Evolução Hematológica")
col1, col2 = st.columns(2)

# Gráfico 1: Hematócrito
fig_hem = go.Figure()
fig_hem.add_trace(go.Scatter(x=df['Data'], y=df['Hematócrito'], mode='lines+markers', name='Hematócrito (%)', line=dict(color='firebrick', width=3)))
fig_hem.add_hrect(y0=37, y1=55, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (37-55%)")
fig_hem.add_vrect(x0=inicio_glucantime, x1=fim_glucantime, fillcolor="green", opacity=0.1, annotation_text="Glucantime")
fig_hem.update_layout(title="Hematócrito (Anemia)")
col1.plotly_chart(fig_hem, use_container_width=True)

# Gráfico 2: Leucócitos
fig_leuc = go.Figure()
fig_leuc.add_trace(go.Scatter(x=df['Data'], y=df['Leucócitos'], mode='lines+markers', name='Leucócitos (mil/mm³)', line=dict(color='royalblue', width=3)))
fig_leuc.add_hrect(y0=6, y1=17, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (6-17)")
fig_leuc.add_vrect(x0=inicio_glucantime, x1=fim_glucantime, fillcolor="green", opacity=0.1, annotation_text="Glucantime")
fig_leuc.update_layout(title="Leucócitos (Infecção/Inflamação)")
col2.plotly_chart(fig_leuc, use_container_width=True)

st.subheader("💧 Marcadores Renais")
# Gráfico 3: Função Renal
fig_renal = go.Figure()
fig_renal.add_trace(go.Scatter(x=df['Data'], y=df['Creatinina'], mode='lines+markers', name='Creatinina (mg/dL)', line=dict(color='purple', width=3)))
fig_renal.add_trace(go.Scatter(x=df['Data'], y=df['Fósforo'], mode='lines+markers', name='Fósforo (mg/dL)', line=dict(color='darkorange', width=3)))
fig_renal.add_hrect(y0=0.5, y1=1.5, line_width=0, fillcolor="purple", opacity=0.1, annotation_text="Ref. Creatinina")
fig_renal.update_layout(title="Creatinina e Fósforo (Foco pós-tratamento)")
st.plotly_chart(fig_renal, use_container_width=True)