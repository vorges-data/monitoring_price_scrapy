import pandas as pd
import sqlite3
from datetime import datetime
import re

# Path arquivo JSON
df = pd.read_json('../../data/data.jsonl', lines=True)

# Setar o pandas para mostrar todas as colunas
pd.set_option('display.max_columns', None)

# Adicionar coluna fonte dos dados
df['_source'] = "https://lista.mercadolivre.com.br/notebook#D[A:notebook]"

# Adicionar coluna data de coleta
df['_data_coleta'] = datetime.now()

# Remover pontos dos valores de preços e converter para inteiros
df['new_price_reais'] = df['new_price_reais'].astype(str).str.replace('.', '').astype(float)
df['old_price_reais'] = df['old_price_reais'].astype(str).str.replace('.', '').astype(float)
df['old_price_centavos'] = df['old_price_centavos'].astype(str).str.replace('.', '').astype(float)

# Garantir que todos os preços sejam tratados como float
df['new_price_reais'] = pd.to_numeric(df['new_price_reais'], errors='coerce')
df['old_price_reais'] = pd.to_numeric(df['old_price_reais'], errors='coerce')
df['old_price_centavos'] = pd.to_numeric(df['old_price_centavos'], errors='coerce')
df['reviews_rating_number'] = pd.to_numeric(df['reviews_rating_number'], errors='coerce')

# Transformar a tipagem das colunas
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
#df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float) # Não há notebook com centavos no preço
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remover os parenteses do reviews_amount
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar os preços
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
#df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100 # Não há notebook com centavos no preço

# Remover as colunas de preço antigas
df = df.drop(columns=['old_price_reais', 'old_price_centavos'])

# Calcular percentual de desconto
df['discount_percentage'] = df.apply(
    lambda row: ((row['old_price'] - row['new_price_reais']) / row['old_price']) * 100
    if row['old_price'] not in [None, 0] else 0,
    axis=1
)

# Definir lista de marcas conhecidas
marcas = ['Apple', 'Samsung', 'Dell', 'Asus', 'Lenovo', 'HP', 'Acer', 'Microsoft', 'Toshiba', 'Sony', 'MSI', 'Razer','LG','Huawei','Xiaomi','Google','Panasonic','Vaio','Positivo','Multilaser']

# Função para extrair a marca do notebook
def extrair_marca(brand_name):
    for marca in marcas:
        if re.search(marca, brand_name, re.IGNORECASE):
            return marca
    return 'Outras'

# Aplicar a função ao DataFrame
df['marca'] = df['brand'].apply(extrair_marca)


# Faixa de desconto
def categorize_discount(row):
    if row['discount_percentage'] == 0:
        return 'Sem desconto'
    elif 0 < row['discount_percentage'] <= 10:
        return 'Até 10%'
    elif 11 <= row['discount_percentage'] <= 20:
        return '11% a 20%'
    elif 21 <= row['discount_percentage'] <= 30:
        return '21% a 30%'
    elif 31 <= row['discount_percentage'] <= 40:
        return '31% a 40%'
    elif 41 <= row['discount_percentage'] <= 50:
        return '41% a 50%'
    else:
        return 'Acima de 50%'
# Criar a nova coluna com as faixas de desconto
df['discount_range'] = df.apply(categorize_discount, axis=1)

# Reordenar as colunas
nova_ordem = ['brand','marca','old_price','new_price_reais','discount_percentage','discount_range','reviews_amount','reviews_rating_number','_source','_data_coleta']
df = df[nova_ordem]

# Conectar ao banco de dados
conn = sqlite3.connect('../../data/price_notebooks_ml.db')

# Salvar o dataframe no banco de dados
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar a conexão
conn.close()