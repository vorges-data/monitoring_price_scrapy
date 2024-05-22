import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('../data/notebooks_ml.db')

# Query para buscar os dados
df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)

# Fechar a conexão
conn.close()

# Título do app
st.title('Pesquisa de Mercado - Notebooks')