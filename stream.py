import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("nba_elo_filtrado.csv")

df = load_data()

st.title("🏀 Dashboard NBA - Juegos Ganados y Perdidos")

# --- SIDEBAR ---
st.sidebar.header("Filtros")

# Año
anio = st.sidebar.selectbox("Selecciona un año", sorted(df['year_id'].unique()))

# Equipos
equipos = df[df['year_id'] == anio]['team_id'].unique()
equipo = st.sidebar.selectbox("Selecciona un equipo", sorted(equipos))

# Tipo de juego
tipo_juego = st.sidebar.radio("Tipo de juego", ["Temporada regular", "Playoffs", "Ambos"], horizontal=True)

# --- FILTRAR DATOS ---
df_filtrado = df[(df['year_id'] == anio) & (df['team_id'] == equipo)]

if tipo_juego == "Temporada regular":
    df_filtrado = df_filtrado[df_filtrado['is_playoffs'] == 0]
elif tipo_juego == "Playoffs":
    df_filtrado = df_filtrado[df_filtrado['is_playoffs'] == 1]

# Resetear índice por si es necesario
df_filtrado = df_filtrado.sort_values("date_game").reset_index(drop=True)

# --- ACUMULADO DE GANADOS Y PERDIDOS ---
df_filtrado['ganados'] = (df_filtrado['game_result'] == 'W').astype(int)
df_filtrado['perdidos'] = (df_filtrado['game_result'] == 'L').astype(int)
df_filtrado['acum_ganados'] = df_filtrado['ganados'].cumsum()
df_filtrado['acum_perdidos'] = df_filtrado['perdidos'].cumsum()

# --- GRÁFICA DE LÍNEAS ---
st.subheader("📈 Juegos Ganados vs Perdidos (Acumulado)")

fig, ax = plt.subplots()
ax.plot(df_filtrado['date_game'], df_filtrado['acum_ganados'], label='Ganados', color='green')
ax.plot(df_filtrado['date_game'], df_filtrado['acum_perdidos'], label='Perdidos', color='red')
ax.set_xlabel("Fecha del juego")
ax.set_ylabel("Juegos acumulados")
ax.legend()
st.pyplot(fig)

# --- GRÁFICA DE PASTEL ---
st.subheader("🥧 Porcentaje de juegos ganados y perdidos")

total_wins = df_filtrado['ganados'].sum()
total_losses = df_filtrado['perdidos'].sum()

fig2, ax2 = plt.subplots()
ax2.pie([total_wins, total_losses],
        labels=['Ganados', 'Perdidos'],
        colors=['green', 'red'],
        autopct='%1.1f%%',
        startangle=90)
ax2.axis('equal')
st.pyplot(fig2)
