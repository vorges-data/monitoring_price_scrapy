import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('../../data/price_notebooks_ml.db')

# Query para buscar os dados
df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)

# Fechar a conexão
conn.close()

# Título do app
st.title('Pesquisa de Mercado - Preço de Notebooks')
st.subheader('Principais KPIs')



# Configurando o layout em duas linhas
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# Linha 1
# KPI 1: Número de notebooks coletados
total_notebooks = df.shape[0]
col1.metric('Total de Notebooks', total_notebooks)

# KPI 2: Preço médio dos notebooks
avg_price = df['new_price_reais'].median()
col2.metric('Mediana Preço', f'R$ {avg_price}')

# KPI 3: Número de reviews
total_reviews = df['reviews_amount'].sum()
col3.metric('Total de Reviews', total_reviews)

# Espaçamento entre as linhas
st.markdown("<br>", unsafe_allow_html=True)

# Linha 2
# KPI 4: Média reviews_rating_number
avg_rating = df['reviews_rating_number'].mean()
col4.metric('Média de Avaliações', f'{avg_rating:.2f}')

# KPI 5: Preço mais barato
min_price = df['new_price_reais'].min()
col5.metric('Preço Mínimo', f'R$ {min_price}')

# KPI 6: Preço mais caro
max_price = df['new_price_reais'].max()
col6.metric('Preço Máximo', f'R$ {max_price}')

st.dataframe(df)

