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
        # Título do app
        st.title('Pesquisa de Mercado - Preço de Notebooks')

        # Logo Vorges
        image_logo = Image.open('images/Logo_Preto_Sem_Fundo.png')
        st.sidebar.image(image_logo, width=180)

        st.sidebar.write('Utilize os filtros para analisar os dados')
        
        # Informar a data da coleta e atualização
        ultima_coleta = self.df['_data_coleta'].unique()[0]
        ultima_coleta_formatada = pd.to_datetime(ultima_coleta).strftime('%d/%m/%Y %H:%M:%S')
        st.write(f"Última atualização: {ultima_coleta_formatada}")

    def show_kpis(self, df_filtered):
        st.subheader('Principais KPIs')

        # Configurando o layout em duas linhas
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        # Linha 1
        # KPI 1: Número de notebooks coletados
        total_notebooks = df_filtered.shape[0]
        col1.metric('Total de Notebooks', total_notebooks)

        # KPI 2: Preço médio dos notebooks
        avg_price = df_filtered['new_price_reais'].median()
        col2.metric('Mediana Preço', f'R$ {avg_price}')

        # KPI 3: Número de reviews
        total_reviews = df_filtered['reviews_amount'].sum()
        col3.metric('Total de Reviews', total_reviews)

        # Espaçamento entre as linhas
        st.markdown("<br>", unsafe_allow_html=True)

        # Linha 2
        # KPI 4: Média reviews_rating_number
        avg_rating = df_filtered['reviews_rating_number'].mean()
        col4.metric('Média de Avaliações', f'{avg_rating:.2f}')

        # KPI 5: Preço mais barato
        min_price = df_filtered['new_price_reais'].min()
        col5.metric('Preço Mínimo', f'R$ {min_price}')

        # KPI 6: Preço mais caro
        max_price = df_filtered['new_price_reais'].max()
        col6.metric('Preço Máximo', f'R$ {max_price}')

    def apply_filters(self):
        st.sidebar.header('Filtros')

        # Filtro de marca
        marcas = st.sidebar.multiselect('Selecione as marcas', options=self.df['marca'].unique(), default=self.df['marca'].unique())
        
        # Filtro de faixa de preço
        preco_min, preco_max = st.sidebar.slider('Faixa de Preço', float(self.df['new_price_reais'].min()), float(self.df['new_price_reais'].max()), (float(self.df['new_price_reais'].min()), float(self.df['new_price_reais'].max())))
        
        # Filtro de avaliação
        avaliacao_min, avaliacao_max = st.sidebar.slider('Faixa de Avaliação', float(self.df['reviews_rating_number'].min()), float(self.df['reviews_rating_number'].max()), (float(self.df['reviews_rating_number'].min()), float(self.df['reviews_rating_number'].max())))

        # Filtro faixa de desconto
        ordered_options = ['Até 10%', '11% a 20%', '21% a 30%', '31% a 40%', '41% a 50%', 'Acima de 50%', 'Sem desconto']
        faixa_desconto = st.sidebar.multiselect('Faixa de Desconto', options=ordered_options, default=['Até 10%', '11% a 20%', '21% a 30%', '31% a 40%', '41% a 50%', 'Acima de 50%', 'Sem desconto'], help='Selecione a faixa de desconto', key='faixa_desconto')

        # Filtro de search brand
        search_brand = st.sidebar.text_input('Pesquisar notebook', '', help='Digite o nome da marca para pesquisar')


        # Aplicar filtros
        df_filtered = self.df[(self.df['marca'].isin(marcas)) & 
                          (self.df['new_price_reais'] >= preco_min) & (self.df['new_price_reais'] <= preco_max) &
                          (self.df['reviews_rating_number'] >= avaliacao_min) & (self.df['reviews_rating_number'] <= avaliacao_max)]
    
        # Aplicar filtro de faixa de desconto
        if faixa_desconto:
            df_filtered = df_filtered[df_filtered['discount_range'].apply(lambda x: x in faixa_desconto)]


        # Aplicar filtro de search_brand se fornecido
        if search_brand:
            df_filtered = df_filtered[df_filtered['brand'].str.contains(search_brand, case=False)]

        return df_filtered

    def show_charts(self, df_filtered):

        # Marcas mais encontradas
        st.subheader('Marcas mais encontradas')
        col1, col2 = st.columns([4, 2])
        top_10_brands_page = df_filtered['marca'].value_counts().sort_values(ascending=False)
        col1.bar_chart(top_10_brands_page, color='#83c9ff')
        col2.write(top_10_brands_page)

        # Preço médio da marca
        st.subheader('Preço médio por marca')
        col1, col2 = st.columns([4, 2])
        df_non_zero = df_filtered[df_filtered['new_price_reais'] > 0]
        avg_price_per_brand = round(df_non_zero.groupby('marca')['new_price_reais'].mean().sort_values(ascending=False), 2)
        col1.bar_chart(avg_price_per_brand, color='#83c9ff')
        col2.write(avg_price_per_brand)

        # Satisfação dos clientes
        st.subheader('Satisfação dos clientes')
        col1, col2 = st.columns([4, 2])
        df_non_zero = df_filtered[df_filtered['reviews_rating_number'] > 0]
        avg_rating_per_brand = round(df_non_zero.groupby('marca')['reviews_rating_number'].mean().sort_values(ascending=False), 2)
        col1.bar_chart(avg_rating_per_brand, color='#83c9ff')
        col2.write(avg_rating_per_brand)

        # Histograma de preços
        st.subheader('Distribuição de Preços')
        fig = px.histogram(df_filtered, x='new_price_reais', nbins=30, title='Distribuição de Preços dos Notebooks', labels={'new_price_reais': 'Preço (R$)'}, color_discrete_sequence=['#83c9ff'])
        st.plotly_chart(fig)

        # Gráfico de dispersão Preço vs Avaliação
        st.subheader('Preço vs Avaliação')
        fig = px.scatter(df_filtered, x='new_price_reais', y='reviews_rating_number', title='Preço vs Avaliação', labels={'new_price_reais': 'Preço (R$)', 'reviews_rating_number': 'Avaliação'}, color_discrete_sequence=['#83c9ff'])
        st.plotly_chart(fig)

        # Gráfico de distribuição de preço por avaliação
        st.subheader('Distribuição de Preço por Avaliação')
        fig = go.Figure()
        for rating in sorted(df_filtered['reviews_rating_number'].unique()):
            fig.add_trace(go.Box(y=df_filtered[df_filtered['reviews_rating_number'] == rating]['new_price_reais'], name=str(rating)))
        fig.update_layout(title='Distribuição de Preço por Avaliação', xaxis_title='Avaliação', yaxis_title='Preço (R$)')
        st.plotly_chart(fig)

        # Heatmap de correlação
        df_filtered_renamed = df_filtered.rename(columns={
            'new_price_reais': 'Preço',
            'reviews_rating_number': 'Avaliação',
            'reviews_amount': 'Quantidade de Avaliações'
        })

        correlation_matrix = df_filtered_renamed[['Preço', 'Avaliação', 'Quantidade de Avaliações']].corr()
        st.subheader('Correlação entre Variáveis')
        fig = px.imshow(correlation_matrix, text_auto=True, title='Heatmap de Correlação')
        st.plotly_chart(fig)

        # Grafico de Pareto das marcas
        st.subheader('Análise de Pareto das Marcas')
        pareto_data = df_filtered['marca'].value_counts().reset_index()
        pareto_data.columns = ['marca', 'contagem']
        pareto_data['percentual_acumulado'] = pareto_data['contagem'].cumsum() / pareto_data['contagem'].sum() * 100

        fig = px.bar(pareto_data, x='marca', y='contagem', labels={'marca': 'Marca', 'contagem': 'Contagem'}, color_discrete_sequence=['#83c9ff'])
        fig.add_trace(go.Scatter(x=pareto_data['marca'], y=pareto_data['percentual_acumulado'], mode='lines+markers', name='Percentual Acumulado', yaxis='y2', line=dict(color='red')))

        fig.update_layout(
            yaxis2=dict(
                title='Percentual Acumulado',
                overlaying='y',
                side='right'
            )
        )
        st.plotly_chart(fig)

        # Grafico Treemap
        st.subheader('Participação de Mercado por Marca')
        market_share = df_filtered['marca'].value_counts().reset_index()
        market_share.columns = ['marca', 'contagem']

        fig = px.treemap(market_share, path=['marca'], values='contagem', labels={'marca': 'Marca', 'contagem': 'Contagem'})
        st.plotly_chart(fig)

        # Boxplot marca
        st.subheader('Variação dos Preços dos Notebooks por Marca')
        fig = px.box(df_filtered, x='marca', y='new_price_reais', labels={'marca': 'Marca', 'new_price_reais': 'Preço (R$)'}, color_discrete_sequence=['#83c9ff'])
        st.plotly_chart(fig)

        # Tabela com os dados
        st.subheader('Tabela de Dados')
        st.dataframe(df_filtered)


#============================================================================================
#================================ CARDS ====================================================


    def card(self, title, supplier, price, reviews_ratings, reviews_amount, image_url, product_url, installments, source):
        card_html = f"""
        <div class="card">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{image_url}" alt="Image" style="width: 190px; height: 190px; border-radius: 50%;"/>
            </div>
            <h3 style="color: #007bff; margin-bottom: 10px; font-size: 18px;">{title}</h3>
            <p style="color: #6c757d; margin-bottom: 10px;">Fornecedor: {supplier}</p>
            <p><b>Preço R$:</b> {price}</p>
            <p><b>Avaliação:</b> {reviews_ratings}</p>
            <p><b>Quantidade Avaliações:</b> {reviews_amount}</p>
            <p><b>Link do Notebook:</b> <a href="{product_url}" target="_blank">Clique aqui</a></p>
            <p><b>Parcelas</b> {installments}</p>
            <p><b>Fonte:</b> {source}</p>
        </div>
        """
        return card_html
    

    def run(self):
        self.show_title()
        df_filtered = self.apply_filters()
        self.show_kpis(df_filtered)
        self.show_charts(df_filtered)
        
        st.markdown("<h1 style='text-align: center;'>Principais Notebooks - Melhores Avaliados</h1>", unsafe_allow_html=True)

         # Selecionar os 10 principais notebooks com base em reviews_amount e reviews_rating_number, removendo duplicatas
        top_notebooks = (df_filtered.sort_values(by=['reviews_amount', 'reviews_rating_number'], ascending=False)
                                .drop_duplicates(subset=['reviews_amount', 'reviews_rating_number'])
                                .head(12)
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
        self.card(top_notebooks['brand'][0], top_notebooks['supplier'][0], top_notebooks['new_price_reais'][0], top_notebooks['reviews_rating_number'][0], top_notebooks['reviews_amount'][0], top_notebooks['img_product_url'][0], top_notebooks['product_url'][0], top_notebooks['installments'][0], "Mercado LIvre") +
        self.card(top_notebooks['brand'][1], top_notebooks['supplier'][1], top_notebooks['new_price_reais'][1], top_notebooks['reviews_rating_number'][1], top_notebooks['reviews_amount'][1], top_notebooks['img_product_url'][1], top_notebooks['product_url'][1], top_notebooks['installments'][1], "Mercado LIvre") +
        self.card(top_notebooks['brand'][2], top_notebooks['supplier'][2], top_notebooks['new_price_reais'][2], top_notebooks['reviews_rating_number'][2], top_notebooks['reviews_amount'][2], top_notebooks['img_product_url'][2], top_notebooks['product_url'][2], top_notebooks['installments'][2], "Mercado LIvre") +
        self.card(top_notebooks['brand'][3], top_notebooks['supplier'][3], top_notebooks['new_price_reais'][3], top_notebooks['reviews_rating_number'][3], top_notebooks['reviews_amount'][3], top_notebooks['img_product_url'][3], top_notebooks['product_url'][3], top_notebooks['installments'][3], "Mercado LIvre") +
        self.card(top_notebooks['brand'][4], top_notebooks['supplier'][4], top_notebooks['new_price_reais'][4], top_notebooks['reviews_rating_number'][4], top_notebooks['reviews_amount'][4], top_notebooks['img_product_url'][4], top_notebooks['product_url'][4], top_notebooks['installments'][4], "Mercado LIvre") +
        self.card(top_notebooks['brand'][5], top_notebooks['supplier'][5], top_notebooks['new_price_reais'][5], top_notebooks['reviews_rating_number'][5], top_notebooks['reviews_amount'][5], top_notebooks['img_product_url'][5], top_notebooks['product_url'][5], top_notebooks['installments'][5], "Mercado LIvre") +
        self.card(top_notebooks['brand'][6], top_notebooks['supplier'][6], top_notebooks['new_price_reais'][6], top_notebooks['reviews_rating_number'][6], top_notebooks['reviews_amount'][6], top_notebooks['img_product_url'][6], top_notebooks['product_url'][6], top_notebooks['installments'][6], "Mercado LIvre") +
        self.card(top_notebooks['brand'][7], top_notebooks['supplier'][7], top_notebooks['new_price_reais'][7], top_notebooks['reviews_rating_number'][7], top_notebooks['reviews_amount'][7], top_notebooks['img_product_url'][7], top_notebooks['product_url'][7], top_notebooks['installments'][7], "Mercado LIvre") +
        self.card(top_notebooks['brand'][8], top_notebooks['supplier'][9], top_notebooks['new_price_reais'][8], top_notebooks['reviews_rating_number'][8], top_notebooks['reviews_amount'][8], top_notebooks['img_product_url'][8], top_notebooks['product_url'][8], top_notebooks['installments'][8], "Mercado LIvre") +
        self.card(top_notebooks['brand'][9], top_notebooks['supplier'][9], top_notebooks['new_price_reais'][9], top_notebooks['reviews_rating_number'][9], top_notebooks['reviews_amount'][9], top_notebooks['img_product_url'][9], top_notebooks['product_url'][9], top_notebooks['installments'][9], "Mercado LIvre") +
        self.card(top_notebooks['brand'][10], top_notebooks['supplier'][10], top_notebooks['new_price_reais'][10], top_notebooks['reviews_rating_number'][10], top_notebooks['reviews_amount'][10], top_notebooks['img_product_url'][10], top_notebooks['product_url'][10], top_notebooks['installments'][10], "Mercado LIvre") +
        self.card(top_notebooks['brand'][11], top_notebooks['supplier'][11], top_notebooks['new_price_reais'][11], top_notebooks['reviews_rating_number'][11], top_notebooks['reviews_amount'][11], top_notebooks['img_product_url'][11], top_notebooks['product_url'][11], top_notebooks['installments'][11], "Mercado LIvre") +
        "</div>", unsafe_allow_html=True)


if __name__ == '__main__':
    db_path = 'data/price_notebooks_ml.db'
    app = PrecoNotebookApp(db_path)
    app.run()
