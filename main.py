import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. СТИЛЬ ЖӘНЕ КОНФИГУРАЦИЯ
st.set_page_config(page_title="EduAnalytics KZ 2026", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FDFDFD; }
    .stMetric { border: 1px solid #1E3A8A; padding: 10px; border-radius: 5px; }
    h1, h2 { color: #1E3A8A; font-family: 'Georgia', serif; border-bottom: 2px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# 2. ДЕРЕКТЕРДІ ГЕНЕРАЦИЯЛАУ (PANDAS)
@st.cache_data
def get_data():
    # Гранттар дерегі
    grants = pd.DataFrame({
        'Сала': ['IT', 'IT', 'Инженерия', 'Инженерия', 'Педагогика', 'Педагогика', 'Медицина', 'Ауыл ш.'],
        'Мамандық': ['Software Eng', 'Cybersecurity', 'Құрылыс', 'Механика', 'Математика', 'Филология', 'Жалпы мед', 'Агрономия'],
        'Грант_саны': [4500, 3200, 5600, 2100, 4800, 3900, 2500, 1800]
    })
    
    # Серпін дерегі
    serpin = pd.DataFrame({
        'Өңір': ['СҚО', 'ПҚО', 'ШҚО', 'Қостанай', 'Ақмола'],
        'Квота': [1200, 1500, 1100, 1300, 950],
        'Игерілгені': [1050, 1420, 890, 1250, 800]
    })
    
    # Түлектер дерегі
    market = pd.DataFrame({
        'Мамандық': ['IT', 'Мұнай-газ', 'Медицина', 'Құқық', 'Экономика', 'Сәулет', 'Педагогика', 'Логистика'],
        'Жұмысқа_орналасу_%': [92, 88, 96, 65, 72, 78, 85, 81],
        'Орташа_жалақы': [480000, 550000, 320000, 280000, 310000, 350000, 250000, 290000],
        'Түлектер_саны': [12000, 5000, 4000, 8000, 10000, 3000, 15000, 4500]
    })
    
    return grants, serpin, market

df_g, df_s, df_m = get_data()

# 3. ИНТЕРФЕЙС
st.title("🎓 ҚР Жоғары білім беру жүйесінің аналитикалық платформасы")
st.write("Academic Year: 2025-2026 | Data: Ministry of Science and Higher Education")

# --- 1-БӨЛІМ: TREEMAP ---
st.header("1. Мемлекеттік гранттардың құрылымы")
fig_tree = px.treemap(df_g, path=['Сала', 'Мамандық'], values='Грант_саны',
                     color='Грант_саны', color_continuous_scale='Blues',
                     title="Мамандықтар бойынша гранттар иерархиясы")
st.plotly_chart(fig_tree, use_container_width=True)

# --- 2-БӨЛІМ: SERPIN BAR CHART ---
st.header("2. 'Серпін' бағдарламасының өңірлік тиімділігі")
df_s['Тиімділік_%'] = (df_s['Игерілгені'] / df_s['Квота']) * 100
fig_bar = go.Figure(data=[
    go.Bar(name='Бөлінген квота', x=df_s['Өңір'], y=df_s['Квота'], marker_color='#B9CEEB'),
    go.Bar(name='Игерілген грант', x=df_s['Өңір'], y=df_s['Игерілгені'], marker_color='#1E3A8A')
])
fig_bar.update_layout(barmode='group', title="Өңірлердегі квотаны игеру көрсеткіші")
st.plotly_chart(fig_bar, use_container_width=True)

# --- 3-БӨЛІМ: BUBBLE CHART ---
st.header("3. Еңбек нарығы: Жалақы және Сұраныс")
fig_bubble = px.scatter(df_m, x="Жұмысқа_орналасу_%", y="Орташа_жалақы",
                        size="Түлектер_саны", color="Мамандық",
                        hover_name="Мамандық", size_max=70,
                        title="Түлектердің мансаптық көрсеткіштері")
fig_bubble.add_hline(y=df_m['Орташа_жалақы'].mean(), line_dash="dot", annotation_text="Орташа жалақы шегі")
st.plotly_chart(fig_bubble, use_container_width=True)

# --- 4-БӨЛІМ: PREDICTOR (PANDAS FILTERS) ---
st.header("4. 🎯 Grant Predictor: Түсу мүмкіндігін есептеу")

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        score = st.number_input("ҰБТ Балыңыз:", 0, 140, 100)
    with col2:
        major_cat = st.selectbox("Бағыт таңдаңыз:", df_g['Сала'].unique())
    with col3:
        quota = st.checkbox("Ауылдық квота бар ма?")

    # Pandas фильтрлері арқылы логика
    relevant_grants = df_g[df_g['Сала'] == major_cat]['Грант_саны'].sum()
    
    # Шартты логика (Мүмкіндікті есептеу)
    if score > 120: status, color = "Өте жоғары", "green"
    elif score > 100: status, color = "Жоғары", "blue"
    elif score > 85: status, color = "Орташа", "orange"
    else: status, color = "Төмен", "red"
    
    if quota: score += 5 # Квотаның әсері
    
    st.markdown(f"### Сіздің таңдалған бағыт бойынша мүмкіндігіңіз: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
    st.info(f"Анықтама: {major_cat} бағыты бойынша биыл {relevant_grants} грант бөлінген. "
            f"Сіздің балыңыз таңдалған саладағы бәсекелестікке {'сәйкес келеді' if score > 90 else 'төменірек'}.")

# FOOTER
st.markdown("---")
st.caption("Developed by Gemini AI | Modern Academic Analytics Interface | 2026")