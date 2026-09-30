import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard Clínico - Bellatrix", layout="wide")
st.title("🐾 Dashboard Clínico - Bellatriz")
st.markdown("Acompanhamento da evolução laboratorial (Leishmaniose e Marcadores Renais).")

# --- DADOS DOS EXAMES ---
dados = {
    'Data': ['2026-06-06', '2026-06-16', '2026-07-10', '2026-08-01', '2026-08-12', '2026-09-01'],
    'Hematócrito': [24.0, 28.0, 37.6, 52.0, 48.0, 35.6],
    'Leucócitos': [41.5, 6.5, 7.95, 9.2, 4.9, 6.7],
    'Plaquetas': [148, 151, 346, 248, 296, 609],
    'Creatinina': [None, 1.0, 0.8, 1.7, 1.2, None],
    'Ureia': [None, 51.0, 16.0, 53.4, 41.4, None],
    'Fósforo': [None, None, 5.8, 7.2, 7.0, None],
    'Proteinas': [10.2, None, None, 9.9, 8.1, None]
}
df = pd.DataFrame(dados)
df['Data'] = pd.to_datetime(df['Data'])

# Datas do tratamento
inicio_glucantime = '2026-06-08'
fim_glucantime = '2026-07-18'

# --- KPIs (ÚLTIMO EXAME) ---
st.subheader("📌 Status Atual (Exame de 12/08/2026)")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Hematócrito", "48.0 %", "Normal", delta_color="off")
k2.metric("Plaquetas", "296 mil/mm³", "Normal", delta_color="off")
k3.metric("Creatinina", "1.2 mg/dL", "Normal", delta_color="off")
k4.metric("Fósforo", "7.0 mg/dL", "Elevado ⚠️", delta_color="inverse")
k5.metric("Proteínas Totais", "8.1 g/dL", "Atenção", delta_color="inverse")

st.markdown("---")

# --- DESTAQUE PARA O TRATAMENTO ---
st.success("🟢 **PERÍODO DE TRATAMENTO:** A faixa verde clara em **todos os gráficos abaixo** representa a janela de 40 dias de tratamento com **Glucantime** (08/06 a 18/07).")

def adicionar_fundo_glucantime(fig):
    fig.add_vrect(x0=inicio_glucantime, x1=fim_glucantime, fillcolor="green", opacity=0.15, line_width=0, annotation_text="Glucantime (40 dias)", annotation_position="top left")
    return fig

# ================= GRÁFICOS VERTICAIS =================

# 1. Hematócrito
st.subheader("🩸 Hematócrito")
fig_hem = go.Figure()
fig_hem.add_trace(go.Scatter(x=df['Data'], y=df['Hematócrito'], mode='lines+markers+text', text=df['Hematócrito'], textposition="top center", line=dict(color='firebrick', width=3)))
fig_hem.add_hrect(y0=37, y1=55, line_width=0, fillcolor="gray", opacity=0.15, annotation_text="Normal (37-55%)")
fig_hem = adicionar_fundo_glucantime(fig_hem)
fig_hem.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_hem, use_container_width=True)

st.markdown("---")

# 2. Leucócitos
st.subheader("🦠 Leucócitos")
fig_leuc = go.Figure()
fig_leuc.add_trace(go.Scatter(x=df['Data'], y=df['Leucócitos'], mode='lines+markers+text', text=df['Leucócitos'], textposition="top center", line=dict(color='royalblue', width=3)))
fig_leuc.add_hrect(y0=6, y1=17, line_width=0, fillcolor="gray", opacity=0.15, annotation_text="Normal (6-17)")
fig_leuc = adicionar_fundo_glucantime(fig_leuc)
fig_leuc.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_leuc, use_container_width=True)

st.markdown("---")

# 3. Plaquetas
st.subheader("🩹 Plaquetas")
fig_plaq = go.Figure()
fig_plaq.add_trace(go.Scatter(x=df['Data'], y=df['Plaquetas'], mode='lines+markers+text', text=df['Plaquetas'], textposition="top center", line=dict(color='darkmagenta', width=3)))
fig_plaq.add_hrect(y0=200, y1=575, line_width=0, fillcolor="gray", opacity=0.15, annotation_text="Normal (200-575)")
fig_plaq = adicionar_fundo_glucantime(fig_plaq)
fig_plaq.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_plaq, use_container_width=True)

st.markdown("---")

# 4. Creatinina e Fósforo (AGORA COM AS DATAS ALINHADAS CORRETAMENTE)
st.subheader("💧 Marcadores Renais: Creatinina e Fósforo")
fig_renal = go.Figure()

# Filtramos os dados corretamente para manter o alinhamento do eixo X
df_crea = df.dropna(subset=['Creatinina'])
df_phos = df.dropna(subset=['Fósforo'])

fig_renal.add_trace(go.Scatter(x=df_crea['Data'], y=df_crea['Creatinina'], mode='lines+markers+text', name='Creatinina', text=df_crea['Creatinina'], textposition="bottom center", line=dict(color='purple', width=3)))
fig_renal.add_trace(go.Scatter(x=df_phos['Data'], y=df_phos['Fósforo'], mode='lines+markers+text', name='Fósforo', text=df_phos['Fósforo'], textposition="top center", line=dict(color='darkorange', width=3)))
fig_renal.add_hrect(y0=0.5, y1=1.5, line_width=0, fillcolor="purple", opacity=0.1, annotation_text="Ref. Creatinina")
fig_renal.add_hrect(y0=2.6, y1=6.2, line_width=0, fillcolor="orange", opacity=0.1, annotation_text="Ref. Fósforo")
fig_renal = adicionar_fundo_glucantime(fig_renal)
fig_renal.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_renal, use_container_width=True)

st.markdown("---")

# 5. Ureia (COM AS DATAS ALINHADAS)
st.subheader("🧪 Ureia")
fig_ureia = go.Figure()
df_ureia = df.dropna(subset=['Ureia'])
fig_ureia.add_trace(go.Scatter(x=df_ureia['Data'], y=df_ureia['Ureia'], mode='lines+markers+text', text=df_ureia['Ureia'], textposition="top center", line=dict(color='teal', width=3)))
fig_ureia.add_hrect(y0=21.4, y1=59.9, line_width=0, fillcolor="gray", opacity=0.15, annotation_text="Normal (21.4-59.9)")
fig_ureia = adicionar_fundo_glucantime(fig_ureia)
fig_ureia.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_ureia, use_container_width=True)

st.markdown("---")

# 6. Proteínas Totais
st.subheader("🔬 Proteínas Totais")
fig_prot = go.Figure()
df_prot = df.dropna(subset=['Proteinas'])
fig_prot.add_trace(go.Scatter(x=df_prot['Data'], y=df_prot['Proteinas'], mode='lines+markers+text', text=df_prot['Proteinas'], textposition="top center", line=dict(color='chocolate', width=3)))
fig_prot.add_hrect(y0=5.5, y1=8.0, line_width=0, fillcolor="gray", opacity=0.15, annotation_text="Normal (5.5-8.0)")
fig_prot = adicionar_fundo_glucantime(fig_prot)
fig_prot.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_prot, use_container_width=True)

st.subheader("📄 Laudos Originais Recentes (PDF)")

c1, c2, c3 = st.columns(3)
c1.link_button("🩸 Hemogramas", "https://drive.google.com/drive/folders/1JQJ_TKomK1efxpeu3OkepfQsd5ZLzIuv?usp=share_link", use_container_width=True)
c2.link_button("📊 Bioquímicos e Urinálises", "https://drive.google.com/drive/folders/13mVXsIo-n7cuYqAl9-zmtMGWYsGGB7Dv?usp=share_link", use_container_width=True)
c3.link_button("🖥️ Ultrassonografias", "https://drive.google.com/drive/folders/13HG9KhJEQoio_jWBzo4CTAAj2QQn049m?usp=share_link", use_container_width=True)
