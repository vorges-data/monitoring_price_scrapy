import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon= '📊')

image = Image.open('images/Logo_Preto_Sem_Fundo.png')
st.sidebar.image( image, width = 120)

st.sidebar.markdown('## WebScraping Notebooks - Mercado Livre')
st.sidebar.markdown("""---""")

st.sidebar.write('"O que eu não posso criar, eu não entendo." - Richard Feynman')

#==============================================================================

st.write('# Projeto de WebScraping - Análise de Preços de Notebooks do Mercado Livre')
st.markdown("""---""")

st.markdown(
    """
    
    ### Como utilizar este Dashboard?
    No menu lateral deste Web App há duas páginas:
    - **Análise Gráfica:** Gráficos para análise dos diferentes tipos e marcas dos notebooks;
        - Distribuição de preços por marca
        - Avaliações médias por tipo de notebook
        - Comparação de preços e avaliações

    - **Cards Notebooks:** 20 principais notebooks em nota de avaliação e quantidade de avaliações na plataforma;
    
    
    Portanto, acesse o menu lateral e escolha a página que gostaria de visualizar!

    **Período de Atualização dos Dados:** 1x por semana às segundas-feiras.
    
    ### Ferramentas Utilizadas
    - **Python:** Linguagem principal utilizada no projeto.
    - **Scrapy:** Biblioteca de web scraping usada para coletar dados do Mercado Livre.
    - **Pandas:** Biblioteca para manipulação e análise de dados.
    - **Streamlit:** Framework para criação do dashboard interativo.
    - **SQLite:** Banco de dados utilizado para armazenar os dados raspados.
    - **Poetry:** Ferramenta para gerenciamento de dependências e ambiente virtual.

    ### Automação
    - **GitHub Actions:** Utilizado para automação das tarefas do projeto, incluindo a execução do script de web scraping uma vez por semana.

    ### Outros
    - **VSCode:** Editor de código recomendado para o desenvolvimento do projeto.

    ### Time de Desenvolvimento:
    - Vinicius Borges
    
    ### Contato:
    - Vinicius Borges: [Linkedin](https://www.linkedin.com/in/viniciusleitedata/)
    - Github do Projeto: [Github](https://github.com/vorges-data/monitoring_price_scrapy)
    - Blog Vorges: [Clique aqui para conferir!](www.vorges.com.br)
    
    

    """
)
st.markdown("""---""")