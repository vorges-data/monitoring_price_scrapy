from main import DataTransformer

def main():
    data_path = '../../data/data.jsonl'
    db_path = '../../data/price_notebooks_ml.db'

    transformer = DataTransformer(data_path, db_path)
    transformer.transform()

if __name__ == "__main__":
    main()
