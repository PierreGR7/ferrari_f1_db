import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Ferrari F1 Dashboard", layout="wide")

# Connexion base SQLite
conn = sqlite3.connect('../ferrari_f1.db')


st.title("🏎️ Ferrari en Formule 1 – Tableau de bord historique")

# ---------- CHARGEMENT DES DONNÉES ----------
@st.cache_data
def load_data():
    query = """
    SELECT r.year, res.position, res.points, d.surname AS driver, res.status
    FROM results res
    JOIN races r ON r.race_id = res.race_id
    JOIN drivers d ON d.driver_id = res.driver_id
    WHERE res.constructor_id = 'ferrari'
    """
    return pd.read_sql_query(query, conn)

df = load_data()
df['position'] = pd.to_numeric(df['position'], errors='coerce')

# ---------- KPI GLOBALS ----------
total_points = df['points'].sum()
total_wins = df[df['position'] == 1].shape[0]
total_podiums = df[df['position'].isin([1, 2, 3])].shape[0]
total_retirements = df[df['status'].str.contains("Retired|Accident|Disqualified|Engine", case=False)].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🏁 Total Points", f"{int(total_points)}")
col2.metric("🥇 Victoires", f"{total_wins}")
col3.metric("🥈 Podiums", f"{total_podiums}")
col4.metric("❌ Abandons", f"{total_retirements}")

# ---------- POINTS PAR SAISON ----------
points_season = df.groupby('year')['points'].sum().reset_index()
st.subheader("📈 Évolution des points par saison")
st.line_chart(points_season.set_index('year'))

# ---------- VICTOIRES PAR SAISON ----------
wins_per_year = df[df['position'] == 1].groupby('year').size().reset_index(name='wins')
st.subheader("🏆 Victoires par saison")
st.bar_chart(wins_per_year.set_index('year'))

# ---------- PILOTES FERRARI ----------
st.subheader("👤 Classement des pilotes Ferrari (par points cumulés)")
pilot_points = df.groupby('driver')['points'].sum().reset_index().sort_values(by='points', ascending=False)
st.dataframe(pilot_points, use_container_width=True)

# ---------- FILTRE INTERACTIF PAR PILOTE ----------
pilote_selection = st.selectbox("🎯 Voir le détail pour un pilote", options=pilot_points['driver'].unique())
df_pilote = df[df['driver'] == pilote_selection]

st.write(f"📊 Détail des performances de {pilote_selection}")
st.bar_chart(df_pilote.groupby('year')['points'].sum())

conn.close()
