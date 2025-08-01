import pandas as pd
from sqlalchemy import create_engine
import psycopg2

def salvar_df_no_postgres(df: pd.DataFrame, tabela: str, db_config: dict):
    if df.empty:
        print("DataFrame vazio. Nada foi salvo.")
        return

    url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(url)

    print(f"Salvando no banco: {db_config['database']} - Tabela: {tabela}")
    df.to_sql(tabela, engine, if_exists='replace', index=False)
    print("Dados salvos com sucesso!")

def executar_sql(path_sql, config):
    with open(path_sql, 'r', encoding='utf-8') as file:
        sql = file.read()

    try:
        conn = psycopg2.connect(
            dbname=config["database"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Script SQL executado com sucesso.")
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao executar SQL:", e)

def consultar_view(nome_view: str, db_config: dict, limite: int = 10) -> pd.DataFrame:
    url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(url)

    query = f"SELECT * FROM {nome_view} LIMIT {limite};"
    try:
        df = pd.read_sql(query, engine)
        print(f"Consulta à view '{nome_view}' executada com sucesso. Mostrando até {limite} linhas.")
        return df
    except Exception as e:
        print(f"Erro ao consultar a view '{nome_view}':", e)
        return pd.DataFrame() 
