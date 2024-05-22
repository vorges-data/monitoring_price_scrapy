import pandas as pd
import sqlite3
from datetime import datetime

# Path arquivo JSON
df = pd.read_json('../data/data.jsonl', lines=True)

# Setar o pandas para mostrar todas as colunas
pd.set_option('display.max_columns', None)

# Adicionar coluna fonte dos dados
df['_source'] = "https://lista.mercadolivre.com.br/notebook#D[A:notebook]"

# Adicionar coluna data de coleta
df['_data_coleta'] = datetime.now()

# Transformar a tipagem das colunas
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remover os parenteses do reviews_amount
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar os preços
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover as colunas de preço antigas
df = df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'])

# Conectar ao banco de dados
conn = sqlite3.connect('../data/notebooks_ml.db')

# Salvar o dataframe no banco de dados
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar a conexão
conn.close()