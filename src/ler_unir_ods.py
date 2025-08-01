import pandas as pd
import os

def encontrar_linha_cabecalho(caminho):
    try:
        df_temp = pd.read_excel(caminho, engine='odf', header=None)
        for i, row in df_temp.iterrows():
            row_str = ' '.join(str(cell) for cell in row.values if pd.notnull(cell)).lower()
            if "grupo econômico" in row_str or "prestadora" in row_str:
                return i
        return None
    except Exception as e:
        print(f"[ERRO] ao tentar identificar o cabeçalho em {caminho}: {e}")
        return None

def ler_arquivo(caminho, ano, servico):
    linha_cabecalho = encontrar_linha_cabecalho(caminho)
    if linha_cabecalho is None:
        print(f"[ERRO] Cabeçalho não encontrado em: {caminho}")
        return None
    try:
        df = pd.read_excel(caminho, engine='odf', skiprows=linha_cabecalho)
        df = df.loc[:, ~df.columns.isnull()]  # Remove colunas totalmente vazias
        df['ano'] = ano
        df['servico'] = servico
        print(f"[OK] Lido: {caminho}")
        return df
    except Exception as e:
        print(f"[ERRO] Falha ao ler {caminho}: {e}")
        return None

def carregar_todos_dados(BASE_DIR, SERVICOS, ANOS):
    todos_dados = []
    for servico in SERVICOS:
        for ano in ANOS:
            caminho = os.path.join(BASE_DIR, servico, f"{servico}_{ano}.ods")
            if not os.path.exists(caminho):
                print(f"[AVISO] Arquivo não encontrado: {caminho}")
                continue
            df = ler_arquivo(caminho, ano, servico)
            if df is not None:
                todos_dados.append(df)
    return todos_dados

def processar_dados(todos_dados):
    if not todos_dados:
        print("[ERRO] Nenhum dado carregado.")
        return None

    df_final = pd.concat(todos_dados, ignore_index=True)

    id_vars = ["GRUPO ECONÔMICO", "VARIÁVEL", "ano", "servico"]
    df_long = df_final.melt(id_vars=id_vars, var_name="mes", value_name="valor")

    df_long.columns = [col.lower().replace(" ", "_") for col in df_long.columns]
    df_long = df_long.rename(columns={
        "grupo_econômico": "grupo_economico",
        "variável": "variavel"
    })

    df_long = df_long[df_long["valor"].notna()]

    df_long["ano_mes"] = pd.to_datetime(df_long["mes"], format="%Y-%m")

    return df_long

def ler_unir(BASE_DIR, SERVICOS, ANOS):
    todos_dados = carregar_todos_dados(BASE_DIR, SERVICOS, ANOS)
    df_tratado = processar_dados(todos_dados)
    if df_tratado is not None:
        df_tratado.to_csv("dados_tratados.csv", index=False)
    return df_tratado

