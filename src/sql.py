import pandas as pd
from sqlalchemy import create_engine
import psycopg2

def get_db_engine(db_config: dict):
    url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    return create_engine(url)

def salvar_df_no_postgres(df: pd.DataFrame, tabela: str, db_config: dict):
    if df.empty:
        print("DataFrame vazio. Nada foi salvo.")
        return

    engine = get_db_engine(db_config)

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
    engine = get_db_engine(db_config)

    query = f"SELECT * FROM {nome_view} LIMIT {limite};"
    try:
        df = pd.read_sql(query, engine)
        print(f"Consulta à view '{nome_view}' executada com sucesso. Mostrando até {limite} linhas.")
        return df
    except Exception as e:
        print(f"Erro ao consultar a view '{nome_view}':", e)
        return pd.DataFrame()

def popular_dim_tempo(df: pd.DataFrame, db_config: dict):
    engine = get_db_engine(db_config)
    df_tempo = df[['mes', 'ano_mes']].drop_duplicates().copy()
    df_tempo['ano'] = df_tempo['ano_mes'].dt.year
    df_tempo['mes_numero'] = df_tempo['ano_mes'].dt.month
    df_tempo['trimestre'] = (df_tempo['ano_mes'].dt.quarter)
    df_tempo['semestre'] = (df_tempo['ano_mes'].dt.month - 1) // 6 + 1
    df_tempo['mes'] = df_tempo['ano_mes'].dt.strftime('%Y-%m')
    df_tempo = df_tempo[['mes', 'ano', 'mes_numero', 'trimestre', 'semestre']]
    df_tempo.to_sql('dim_tempo', engine, if_exists='append', index=False)
    print("Dimensão de Tempo populada com sucesso!")

def popular_dim_servico(df: pd.DataFrame, db_config: dict):
    engine = get_db_engine(db_config)
    df_servico = df[['servico']].drop_duplicates().rename(columns={'servico': 'nome_servico'}) 
    df_servico.to_sql('dim_servico', engine, if_exists='append', index=False)
    print("Dimensão de Serviço populada com sucesso!")

def popular_dim_grupo_economico(df: pd.DataFrame, db_config: dict):
    engine = get_db_engine(db_config)
    df_grupo = df[['grupo_economico']].drop_duplicates().rename(columns={'grupo_economico': 'nome_grupo_economico'}) 
    df_grupo.to_sql('dim_grupo_economico', engine, if_exists='append', index=False)
    print("Dimensão de Grupo Econômico populada com sucesso!")

def popular_dim_variavel(df: pd.DataFrame, db_config: dict):
    engine = get_db_engine(db_config)
    df_variavel = df[["variavel"]].drop_duplicates().rename(columns={'variavel': 'nome_variavel'}) 
    df_variavel.to_sql('dim_variavel', engine, if_exists='append', index=False)
    print("Dimensão de Variável populada com sucesso!")

def popular_fato_ida(df: pd.DataFrame, db_config: dict):
    engine = get_db_engine(db_config)
    
    # Obter IDs das dimensões
    df_fato = df.copy()
    
    with engine.connect() as conn:
        dim_tempo_map = pd.read_sql("SELECT id_tempo, mes FROM dim_tempo", conn).set_index('mes')['id_tempo'].to_dict()
        dim_servico_map = pd.read_sql("SELECT id_servico, nome_servico FROM dim_servico", conn).set_index('nome_servico')['id_servico'].to_dict()
        dim_grupo_economico_map = pd.read_sql("SELECT id_grupo_economico, nome_grupo_economico FROM dim_grupo_economico", conn).set_index('nome_grupo_economico')['id_grupo_economico'].to_dict()
        dim_variavel_map = pd.read_sql("SELECT id_variavel, nome_variavel FROM dim_variavel", conn).set_index('nome_variavel')['id_variavel'].to_dict()

    df_fato['id_tempo'] = df_fato['mes'].map(dim_tempo_map)
    df_fato['id_servico'] = df_fato['servico'].map(dim_servico_map)
    df_fato['id_grupo_economico'] = df_fato['grupo_economico'].map(dim_grupo_economico_map)
    df_fato['id_variavel'] = df_fato['variavel'].map(dim_variavel_map)

    df_fato = df_fato[["id_tempo", "id_servico", "id_grupo_economico", "id_variavel", "valor"]]
    df_fato.to_sql('fato_ida', engine, if_exists='append', index=False)
    print("Tabela Fato IDA populada com sucesso!")
