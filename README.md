
# Projeto de WebScraping - Análise de Preços de Notebooks do Mercado Livre

## Como utilizar este Dashboard?

No menu lateral deste Web App, há duas páginas:

1. **Análise Gráfica**: Gráficos para análise dos diferentes tipos e marcas de notebooks, incluindo:
   - Distribuição de preços por marca
   - Avaliações médias por tipo de notebook
   - Comparação de preços e avaliações

2. **Cards Notebooks**: Exibição dos 12 principais notebooks em termos de nota de avaliação e quantidade de avaliações na plataforma.

Para navegar, acesse o menu lateral e escolha a página que gostaria de visualizar!

**Período de Atualização dos Dados**: 1x por semana, às segundas-feiras.

## Ferramentas Utilizadas

- **Python**: Linguagem principal utilizada no projeto.
- **Scrapy**: Biblioteca de web scraping usada para coletar dados do Mercado Livre.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Streamlit**: Framework para criação do dashboard interativo.
- **SQLite**: Banco de dados utilizado para armazenar os dados raspados.
- **Poetry**: Ferramenta para gerenciamento de dependências e ambiente virtual.

## Automação

- **GitHub Actions**: Utilizado para automação das tarefas do projeto, incluindo a execução do script de web scraping uma vez por semana.

## Outros

- **VSCode**: Editor de código recomendado para o desenvolvimento do projeto.

## Time de Desenvolvimento

- Vinicius Borges

## Contato

- **LinkedIn**: [Vinicius Borges](link do LinkedIn)
- **GitHub do Projeto**: [GitHub](link do GitHub)
- **Blog Vorges**: [Clique aqui para conferir!](link do Blog)


## Como Instalar e Executar este Projeto Localmente

Para instalar e executar este projeto localmente, siga os passos abaixo:

1. Clone o repositório:
```bash
git clone https://github.com/vorges-data/monitoring_price_scrapy.git
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate # No Windows, use `venv\Scripts\activate`
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Para executar o robô Web Scraper
```bash
scrapy crawl mercadolivre -o ../../data/data.jsonl
```

5. Para rodar o arquivo de transformação dos dados
```bash
python src/transform/run_transformation.py 
```

6. Para iniciar o Dashboard Streamlit:
```bash
streamlit run monitoramento_preco/run Home.py
```

Para acessar o Webapp, [clique aqui!](https://vorges-data-monitoring-price-laptop.streamlit.app/)


