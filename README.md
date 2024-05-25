Acessar App Localmente
```bash
git clone https://github.com/vorges-data/monitoring_price_scrapy.git
pip install -r requirements.txt
cd src/dashboard
streamlit run app.py
```

Para executar o robô scraping
```bash
scrapy crawl mercadolivre -o ../../data/data.jsonl
```

Para rodar o arquivo de transformação dos dados
```bash
python run_transformation.py 
```

Para acessar o Webapp, [clique aqui!](https://vorges-data-monitoring-price-laptop.streamlit.app/)