import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard Clínico - Bellatriz", layout="wide", initial_sidebar_state="expanded")
st.title("🐾 Dashboard Clínico Avançado - Bellatriz")
st.markdown("Acompanhamento completo da evolução laboratorial, focado na resposta ao Glucantime e função renal.")

# --- DADOS DOS EXAMES ---
dados = {
    'Data': ['2026-06-06', '2026-06-16', '2026-07-10', '2026-08-01', '2026-08-12'],
    'Hematócrito': [24.0, 28.0, 37.6, 52.0, 48.0],
    'Leucócitos': [41.5, 6.5, 7.95, 9.2, 4.9],
    'Plaquetas': [148, 151, 346, 248, 296],
    'Creatinina': [None, 1.0, 0.8, 1.7, 1.2],
    'Ureia': [None, 51.0, 16.0, 53.4, 41.4],
    'Fósforo': [None, None, 5.8, 7.2, 7.0],
    'Proteinas': [10.2, None, None, 9.9, 8.1]
}
df = pd.DataFrame(dados)
df['Data'] = pd.to_datetime(df['Data'])

inicio_glucantime = '2026-06-08'
fim_glucantime = '2026-07-18'

# --- KPIs (ÚLTIMO EXAME) ---
st.subheader("📌 Status Atual (Baseado no exame de 12/08/2026)")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Hematócrito", "48.0 %", "Normal", delta_color="off")
k2.metric("Plaquetas", "296 mil/mm³", "Normal", delta_color="off")
k3.metric("Creatinina", "1.2 mg/dL", "Normal", delta_color="off")
k4.metric("Fósforo", "7.0 mg/dL", "Elevado ⚠️", delta_color="inverse")
k5.metric("Proteínas Totais", "8.1 g/dL", "Ligeiramente Elevado", delta_color="inverse")
st.markdown("---")

# --- SISTEMA DE ABAS ---
tab1, tab2, tab3 = st.tabs(["🩸 Hematologia", "💧 Função Renal", "🔬 Proteínas & Laudos"])

# --- ABA 1: HEMATOLOGIA ---
with tab1:
    col1, col2 = st.columns(2)
    
    # Hematócrito
    fig_hem = go.Figure()
    fig_hem.add_trace(go.Scatter(x=df['Data'], y=df['Hematócrito'], mode='lines+markers+text', name='Hematócrito (%)', text=df['Hematócrito'], textposition="top center", line=dict(color='firebrick', width=3)))
    fig_hem.add_hrect(y0=37, y1=55, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (37-55%)")
    fig_hem.add_vrect(x0=inicio_glucantime, x1=fim_glucantime, fillcolor="green", opacity=0.1, annotation_text="Glucantime")
    fig_hem.update_layout(title="Série Vermelha: Hematócrito")
    col1.plotly_chart(fig_hem, use_container_width=True)

    # Leucócitos
    fig_leuc = go.Figure()
    fig_leuc.add_trace(go.Scatter(x=df['Data'], y=df['Leucócitos'], mode='lines+markers+text', name='Leucócitos', text=df['Leucócitos'], textposition="top center", line=dict(color='royalblue', width=3)))
    fig_leuc.add_hrect(y0=6, y1=17, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (6-17)")
    fig_leuc.add_vrect(x0=inicio_glucantime, x1=fim_glucantime, fillcolor="green", opacity=0.1, annotation_text="Glucantime")
    fig_leuc.update_layout(title="Série Branca: Leucócitos (mil/mm³)")
    col2.plotly_chart(fig_leuc, use_container_width=True)
    
    # Plaquetas
    fig_plaq = go.Figure()
    fig_plaq.add_trace(go.Scatter(x=df['Data'], y=df['Plaquetas'], mode='lines+markers+text', name='Plaquetas', text=df['Plaquetas'], textposition="top center", line=dict(color='darkmagenta', width=3)))
    fig_plaq.add_hrect(y0=200, y1=575, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (200-575)")
    fig_plaq.add_vrect(x0=inicio_glucantime, x1=fim_glucantime, fillcolor="green", opacity=0.1)
    fig_plaq.update_layout(title="Plaquetas (mil/mm³) - Recuperação da Pancitopenia", height=350)
    st.plotly_chart(fig_plaq, use_container_width=True)

# --- ABA 2: FUNÇÃO RENAL ---
with tab2:
    st.info("⚠️ Foco de atenção atual: Monitoramento de nefrocalcinose (USG de 12/08) e pico de marcadores no início de Agosto.")
    col_r1, col_r2 = st.columns(2)
    
    # Creatinina e Fósforo
    fig_renal = go.Figure()
    fig_renal.add_trace(go.Scatter(x=df['Data'].dropna(), y=df['Creatinina'].dropna(), mode='lines+markers+text', name='Creatinina', text=df['Creatinina'].dropna(), textposition="bottom center", line=dict(color='purple', width=3)))
    fig_renal.add_trace(go.Scatter(x=df['Data'].dropna(), y=df['Fósforo'].dropna(), mode='lines+markers+text', name='Fósforo', text=df['Fósforo'].dropna(), textposition="top center", line=dict(color='darkorange', width=3)))
    fig_renal.add_hrect(y0=0.5, y1=1.5, line_width=0, fillcolor="purple", opacity=0.1, annotation_text="Ref. Creatinina")
    fig_renal.add_hrect(y0=2.6, y1=6.2, line_width=0, fillcolor="orange", opacity=0.1, annotation_text="Ref. Fósforo")
    fig_renal.update_layout(title="Creatinina e Fósforo (mg/dL)")
    col_r1.plotly_chart(fig_renal, use_container_width=True)
    
    # Ureia
    fig_ureia = go.Figure()
    fig_ureia.add_trace(go.Scatter(x=df['Data'].dropna(), y=df['Ureia'].dropna(), mode='lines+markers+text', name='Ureia', text=df['Ureia'].dropna(), textposition="top center", line=dict(color='teal', width=3)))
    fig_ureia.add_hrect(y0=21.4, y1=59.9, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (21.4-59.9)")
    fig_ureia.update_layout(title="Ureia (mg/dL)")
    col_r2.plotly_chart(fig_ureia, use_container_width=True)

# --- ABA 3: PROTEÍNAS E LINKS ---
with tab3:
    st.write("A elevação de proteínas totais")
    fig_prot = go.Figure()
    # Filtra apenas os dias que têm dados de proteína
    df_prot = df.dropna(subset=['Proteinas'])
    fig_prot.add_trace(go.Scatter(x=df_prot['Data'], y=df_prot['Proteinas'], mode='lines+markers+text', name='Proteínas Totais', text=df_prot['Proteinas'], textposition="top center", line=dict(color='chocolate', width=3)))
    fig_prot.add_hrect(y0=5.5, y1=8.0, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Normal (5.5-8.0)")
    fig_prot.update_layout(title="Proteínas Totais (g/dL)")
    st.plotly_chart(fig_prot, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📄 Laudos Originais Recentes (PDF)")
    
    c1, c2, c3 = st.columns(3)
    c1.link_button("📊 Hemogramas", "https://drive.google.com/file/d/1zf-cRA-eEHYDrJveXALQwt2uKsB61RcJ/view?usp=share_link", use_container_width=True)
    c2.link_button("🩸 Bioquímicos e Urina", "https://drive.google.com/file/d/1rbFyq6Hy6QLdCCqO8Ff4HoO8nHs4ak-L/view?usp=share_link", use_container_width=True)
    c3.link_button("🖥️ Ultrassonografias", "https://drive.google.com/drive/folders/13HG9KhJEQoio_jWBzo4CTAAj2QQn049m?usp=share_link", use_container_width=True)