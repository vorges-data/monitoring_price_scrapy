import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from PIL import Image


class PrecoNotebookApp:
    def __init__(self, db_path):
        self.db_path = db_path
        self.df = self.load_data()

    def load_data(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect(self.db_path)
        
        # Query para buscar os dados
        df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)
        
        # Fechar a conexão
        conn.close()

        return df

    def show_title(self):
        # Logo Vorges
        image_logo = Image.open('images/Logo_Preto_Sem_Fundo.png')
        st.sidebar.image(image_logo, width=180)

        st.sidebar.write('Utilize os filtros para analisar os dados')
        
        # Informar a data da coleta e atualização
        ultima_coleta = self.df['_data_coleta'].unique()[0]
        ultima_coleta_formatada = pd.to_datetime(ultima_coleta).strftime('%d/%m/%Y %H:%M:%S')


    def apply_filters(self):
        st.sidebar.header('Filtros')

        
        # Filtro de marca
        marcas = st.sidebar.multiselect('Selecione as marcas', options=self.df['marca'].unique(), default=self.df['marca'].unique())
        
        
        # Filtro faixa de desconto
        ordered_options = ['Até 10%', '11% a 20%', '21% a 30%', '31% a 40%', '41% a 50%', 'Acima de 50%', 'Sem desconto']
        faixa_desconto = st.sidebar.multiselect('Faixa de Desconto', options=ordered_options, default=['Até 10%', '11% a 20%', '21% a 30%', '31% a 40%', '41% a 50%', 'Acima de 50%', 'Sem desconto'], help='Selecione a faixa de desconto', key='faixa_desconto')

        # Aplicar filtro
        df_filtered = self.df[self.df['marca'].isin(marcas)]

        # Aplicar filtro de faixa de desconto
        if faixa_desconto:
            df_filtered = df_filtered[df_filtered['discount_range'].apply(lambda x: x in faixa_desconto)]


            return df_filtered
    
    
#============================================================================================
#================================ CARDS ====================================================


    def card(self, title, supplier, price, reviews_ratings, reviews_amount, image_url, product_url, installments, source):
        card_html = f"""
        <div class="card">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{image_url}" alt="Image" style="width: 190px; height: 190px; border-radius: 50%;"/>
            </div>
            <h3 style="color: #007bff; margin-bottom: 10px; font-size: 18px;">{title}</h3>
            <p style="color: #6c757d; margin-bottom: 10px;">🚚 Fornecedor: {supplier}</p>
            <p><b>💲 Preço R$:</b> {price}</p>
            <p><b>😀 Avaliação:</b> {reviews_ratings}</p>
            <p><b>🏆 Quantidade Avaliações:</b> {reviews_amount}</p>
            <p><b>🔗 Link do Notebook:</b> <a href="{product_url}" target="_blank">Clique aqui</a></p>
            <p><b>💸 Parcelas</b> {installments}</p>
            <p><b>💻 Fonte:</b> {source}</p>
        </div>
        """
        return card_html
    

    def run(self):
        self.show_title()
        df_filtered = self.apply_filters()
        

        st.markdown("<h1 style='text-align: center;'>Principais Notebooks - Melhores Avaliados</h1>", unsafe_allow_html=True)

         # Selecionar os 10 principais notebooks com base em reviews_amount e reviews_rating_number, removendo duplicatas
        top_notebooks = (df_filtered.sort_values(by=['reviews_amount', 'reviews_rating_number'], ascending=False)
                                .drop_duplicates(subset=['reviews_amount', 'reviews_rating_number'])
                                .head(20)
                                .reset_index(drop=True))


        # Flexbox container
        st.markdown("""
        <style>
        .card-container {
            display: flex;
            justify-content: space-around;
            gap: 20px;
            flex-wrap: wrap;
        }
        .card {
            background-color: #f1f1f1;
            padding: 20px;
            border-radius: 10px;
            width: 300px;
            box-sizing: border-box;
            flex: 0 0 300px;
            margin: 20px 0;
        }
        .card img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin-bottom: 10px;
        }
        .card h3 {
            color: #007bff;
            margin-bottom: 10px;
        }
        .card p {
            color: #6c757d;
            margin-bottom: 10px;
        }
        </style>
        <div class="card-container">
        """ + 
        self.card(top_notebooks['brand'][0], top_notebooks['supplier'][0], top_notebooks['new_price_reais'][0], top_notebooks['reviews_rating_number'][0], top_notebooks['reviews_amount'][0], top_notebooks['img_product_url'][0], top_notebooks['product_url'][0], top_notebooks['installments'][0], "Mercado Livre") +
        self.card(top_notebooks['brand'][1], top_notebooks['supplier'][1], top_notebooks['new_price_reais'][1], top_notebooks['reviews_rating_number'][1], top_notebooks['reviews_amount'][1], top_notebooks['img_product_url'][1], top_notebooks['product_url'][1], top_notebooks['installments'][1], "Mercado Livre") +
        self.card(top_notebooks['brand'][2], top_notebooks['supplier'][2], top_notebooks['new_price_reais'][2], top_notebooks['reviews_rating_number'][2], top_notebooks['reviews_amount'][2], top_notebooks['img_product_url'][2], top_notebooks['product_url'][2], top_notebooks['installments'][2], "Mercado Livre") +
        self.card(top_notebooks['brand'][3], top_notebooks['supplier'][3], top_notebooks['new_price_reais'][3], top_notebooks['reviews_rating_number'][3], top_notebooks['reviews_amount'][3], top_notebooks['img_product_url'][3], top_notebooks['product_url'][3], top_notebooks['installments'][3], "Mercado Livre") +
        self.card(top_notebooks['brand'][4], top_notebooks['supplier'][4], top_notebooks['new_price_reais'][4], top_notebooks['reviews_rating_number'][4], top_notebooks['reviews_amount'][4], top_notebooks['img_product_url'][4], top_notebooks['product_url'][4], top_notebooks['installments'][4], "Mercado Livre") +
        self.card(top_notebooks['brand'][5], top_notebooks['supplier'][5], top_notebooks['new_price_reais'][5], top_notebooks['reviews_rating_number'][5], top_notebooks['reviews_amount'][5], top_notebooks['img_product_url'][5], top_notebooks['product_url'][5], top_notebooks['installments'][5], "Mercado Livre") +
        self.card(top_notebooks['brand'][6], top_notebooks['supplier'][6], top_notebooks['new_price_reais'][6], top_notebooks['reviews_rating_number'][6], top_notebooks['reviews_amount'][6], top_notebooks['img_product_url'][6], top_notebooks['product_url'][6], top_notebooks['installments'][6], "Mercado Livre") +
        self.card(top_notebooks['brand'][7], top_notebooks['supplier'][7], top_notebooks['new_price_reais'][7], top_notebooks['reviews_rating_number'][7], top_notebooks['reviews_amount'][7], top_notebooks['img_product_url'][7], top_notebooks['product_url'][7], top_notebooks['installments'][7], "Mercado Livre") +
        self.card(top_notebooks['brand'][8], top_notebooks['supplier'][9], top_notebooks['new_price_reais'][8], top_notebooks['reviews_rating_number'][8], top_notebooks['reviews_amount'][8], top_notebooks['img_product_url'][8], top_notebooks['product_url'][8], top_notebooks['installments'][8], "Mercado Livre") +
        self.card(top_notebooks['brand'][9], top_notebooks['supplier'][9], top_notebooks['new_price_reais'][9], top_notebooks['reviews_rating_number'][9], top_notebooks['reviews_amount'][9], top_notebooks['img_product_url'][9], top_notebooks['product_url'][9], top_notebooks['installments'][9], "Mercado Livre") +
        self.card(top_notebooks['brand'][10], top_notebooks['supplier'][10], top_notebooks['new_price_reais'][10], top_notebooks['reviews_rating_number'][10], top_notebooks['reviews_amount'][10], top_notebooks['img_product_url'][10], top_notebooks['product_url'][10], top_notebooks['installments'][10], "Mercado Livre") +
        self.card(top_notebooks['brand'][11], top_notebooks['supplier'][11], top_notebooks['new_price_reais'][11], top_notebooks['reviews_rating_number'][11], top_notebooks['reviews_amount'][11], top_notebooks['img_product_url'][11], top_notebooks['product_url'][11], top_notebooks['installments'][11], "Mercado Livre") +
        self.card(top_notebooks['brand'][12], top_notebooks['supplier'][12], top_notebooks['new_price_reais'][12], top_notebooks['reviews_rating_number'][12], top_notebooks['reviews_amount'][12], top_notebooks['img_product_url'][12], top_notebooks['product_url'][12], top_notebooks['installments'][12], "Mercado Livre") +
        self.card(top_notebooks['brand'][13], top_notebooks['supplier'][13], top_notebooks['new_price_reais'][13], top_notebooks['reviews_rating_number'][13], top_notebooks['reviews_amount'][13], top_notebooks['img_product_url'][13], top_notebooks['product_url'][13], top_notebooks['installments'][13], "Mercado Livre") +
        self.card(top_notebooks['brand'][14], top_notebooks['supplier'][14], top_notebooks['new_price_reais'][14], top_notebooks['reviews_rating_number'][14], top_notebooks['reviews_amount'][14], top_notebooks['img_product_url'][14], top_notebooks['product_url'][14], top_notebooks['installments'][14], "Mercado Livre") +
        self.card(top_notebooks['brand'][15], top_notebooks['supplier'][15], top_notebooks['new_price_reais'][15], top_notebooks['reviews_rating_number'][15], top_notebooks['reviews_amount'][15], top_notebooks['img_product_url'][15], top_notebooks['product_url'][15], top_notebooks['installments'][15], "Mercado Livre") +
        self.card(top_notebooks['brand'][16], top_notebooks['supplier'][16], top_notebooks['new_price_reais'][16], top_notebooks['reviews_rating_number'][16], top_notebooks['reviews_amount'][16], top_notebooks['img_product_url'][16], top_notebooks['product_url'][16], top_notebooks['installments'][16], "Mercado Livre") +
        self.card(top_notebooks['brand'][17], top_notebooks['supplier'][17], top_notebooks['new_price_reais'][17], top_notebooks['reviews_rating_number'][17], top_notebooks['reviews_amount'][17], top_notebooks['img_product_url'][17], top_notebooks['product_url'][17], top_notebooks['installments'][17], "Mercado Livre") +
        self.card(top_notebooks['brand'][18], top_notebooks['supplier'][18], top_notebooks['new_price_reais'][18], top_notebooks['reviews_rating_number'][18], top_notebooks['reviews_amount'][18], top_notebooks['img_product_url'][18], top_notebooks['product_url'][18], top_notebooks['installments'][18], "Mercado Livre") +
        self.card(top_notebooks['brand'][19], top_notebooks['supplier'][19], top_notebooks['new_price_reais'][19], top_notebooks['reviews_rating_number'][19], top_notebooks['reviews_amount'][19], top_notebooks['img_product_url'][19], top_notebooks['product_url'][19], top_notebooks['installments'][1], "Mercado Livre") +
        "</div>", unsafe_allow_html=True)


if __name__ == '__main__':
    db_path = 'data/price_notebooks_ml.db'
    app = PrecoNotebookApp(db_path)
    app.run()
