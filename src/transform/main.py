import pandas as pd
import sqlite3
from datetime import datetime
import re

class DataTransformer:
    def __init__(self, input_path, output_db_path):
        self.input_path = input_path
        self.output_db_path = output_db_path
        self.data = None

    def load_data(self):
        self.data = pd.read_json(self.input_path, lines=True)
        print("Data loaded successfully")

    def set_options(self):
        pd.set_option('display.max_columns', None)

    def add_columns(self):
        self.data['_source'] = "https://lista.mercadolivre.com.br/notebook#D[A:notebook]"
        self.data['_data_coleta'] = datetime.now()

    def clean_prices(self):
        self.data['new_price_reais'] = self.data['new_price_reais'].astype(str).str.replace('.', '').astype(float)
        self.data['old_price_reais'] = self.data['old_price_reais'].astype(str).str.replace('.', '').astype(float)
        self.data['old_price_centavos'] = self.data['old_price_centavos'].astype(str).str.replace('.', '').astype(float)

    def convert_columns(self):
        self.data['new_price_reais'] = pd.to_numeric(self.data['new_price_reais'], errors='coerce')
        self.data['old_price_reais'] = pd.to_numeric(self.data['old_price_reais'], errors='coerce')
        self.data['old_price_centavos'] = pd.to_numeric(self.data['old_price_centavos'], errors='coerce')
        self.data['reviews_rating_number'] = pd.to_numeric(self.data['reviews_rating_number'], errors='coerce')
        self.data['old_price_reais'] = self.data['old_price_reais'].fillna(0).astype(float)
        self.data['old_price_centavos'] = self.data['old_price_centavos'].fillna(0).astype(float)
        self.data['new_price_reais'] = self.data['new_price_reais'].fillna(0).astype(float)
        self.data['reviews_rating_number'] = self.data['reviews_rating_number'].fillna(0).astype(float)

    def clean_reviews(self):
        self.data['reviews_amount'] = self.data['reviews_amount'].str.replace('[\(\)]', '', regex=True)
        self.data['reviews_amount'] = self.data['reviews_amount'].fillna(0).astype(int)

    def calculate_prices(self):
        self.data['old_price'] = self.data['old_price_reais'] + self.data['old_price_centavos'] / 100
        self.data = self.data.drop(columns=['old_price_reais', 'old_price_centavos'])

    def calculate_discount(self):
        self.data['discount_percentage'] = self.data.apply(
            lambda row: ((row['old_price'] - row['new_price_reais']) / row['old_price']) * 100
            if row['old_price'] not in [None, 0] else 0,
            axis=1
        )

    def extract_brand(self):
        marcas = ['Apple', 'Samsung', 'Dell', 'Asus', 'Lenovo', 'HP', 'Acer', 'Microsoft', 'Toshiba', 'Sony', 'MSI', 'Razer','LG','Huawei','Xiaomi','Google','Panasonic','Vaio','Positivo','Multilaser']
        def extrair_marca(brand_name):
            for marca in marcas:
                if re.search(marca, brand_name, re.IGNORECASE):
                    return marca
            return 'Outras'
        self.data['marca'] = self.data['brand'].apply(extrair_marca)

    def categorize_discount(self):
        def categorize(row):
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
        self.data['discount_range'] = self.data.apply(categorize, axis=1)

    def reorder_columns(self):
        nova_ordem = ['brand','marca','old_price','new_price_reais','discount_percentage','discount_range','reviews_amount','reviews_rating_number','supplier','installments','product_url','img_product_url','_source','_data_coleta']
        self.data = self.data[nova_ordem]

    def save_to_db(self):
        conn = sqlite3.connect(self.output_db_path)
        self.data.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)
        conn.close()
        print("Data saved to database successfully")

    def transform(self):
        self.load_data()
        self.set_options()
        self.add_columns()
        self.clean_prices()
        self.convert_columns()
        self.clean_reviews()
        self.calculate_prices()
        self.calculate_discount()
        self.extract_brand()
        self.categorize_discount()
        self.reorder_columns()
        self.save_to_db()

if __name__ == "__main__":
    transformer = DataTransformer('../../data/data.jsonl', '../../data/price_notebooks_ml.db')
    transformer.transform()
