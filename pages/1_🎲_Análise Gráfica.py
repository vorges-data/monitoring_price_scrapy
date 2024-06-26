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
        st.write(f"**Última atualização:** {ultima_coleta_formatada}")

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


    def run(self):
        self.show_title()
        df_filtered = self.apply_filters()
        self.show_kpis(df_filtered)
        self.show_charts(df_filtered)


if __name__ == '__main__':
    db_path = 'data/price_notebooks_ml.db'
    app = PrecoNotebookApp(db_path)
    app.run()
