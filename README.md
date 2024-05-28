
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


