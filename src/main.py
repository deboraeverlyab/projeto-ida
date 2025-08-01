from ler_unir_ods import ler_unir
from baixar_dados import baixar_ods
from sql import (salvar_df_no_postgres, executar_sql, consultar_view,
                 popular_dim_tempo, popular_dim_servico, popular_dim_grupo_economico,
                 popular_dim_variavel, popular_fato_ida)
import os

# Parâmetros
anos = range(2015, 2020)  # 2015 a 2019
# Serviços:
# Telefonia Celular (Serviço Móvel Pessoal – SMP)
# Telefonia Fixa Local (Serviço Telefônico Fixo Comutado – STFC)
# Banda Larga Fixa (Serviço de Comunicação Multimídia – SCM).
servicos = ["STFC", "SMP", "SCM"] 
# URL para baixar os .ods
base_url = "https://www.anatel.gov.br/dadosabertos/PDA/IDA"

# Pasta raiz
base_dir = "/dados"

# Separação dos dados: dados/SMP/, dados/SCM/, dados/STFC/
for servico in servicos:
    os.makedirs(os.path.join(base_dir, servico), exist_ok=True)

# Loop de download
for servico in servicos:
    for ano in anos:
        baixar_ods(servico, ano, base_url, base_dir)

df = ler_unir(base_dir, servicos, anos)

if df is not None:
    print(df.head())

    # Configuração do PostgreSQL
    config = {
        "user": "admin",
        "password": "admin123",
        "host": "postgres",
        "port": 5432,
        "database": "postgres_db"
    }

    # Criar esquema do Data Mart (modelo estrela)
    print("Criando esquema do Data Mart.")
    executar_sql("scripts/create_schema.sql", config)

    # Popular tabelas de dimensão
    print("Populando tabelas de dimensão.")
    popular_dim_tempo(df, config)
    popular_dim_servico(df, config)
    popular_dim_grupo_economico(df, config)
    popular_dim_variavel(df, config)

    # Popular tabela de fatos
    print("Populando tabela de fatos.")
    popular_fato_ida(df, config)

    # Manter a tabela original para compatibilidade com a view existente
    salvar_df_no_postgres(df, tabela="indicador_ida", db_config=config)

    # Criar view de taxa de variação
    executar_sql("scripts/create_view.sql", config)
    
    # Consultar e exibir resultados
    df_view = consultar_view("view_taxa_variacao", config)
    df_view.fillna(0, inplace=True) 
    print(df_view)

else:
    print("Erro: ler_unir() retornou None.")