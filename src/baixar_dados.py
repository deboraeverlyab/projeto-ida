import os
import requests

# Função para baixar arquivo .ods
def baixar_ods(servico, ano, base_url, base_dir):
    url = f"{base_url}/{servico}{ano}.ods"
    nome_arquivo = f"{servico}_{ano}.ods"
    caminho = os.path.join(base_dir, servico, nome_arquivo)

    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            with open(caminho, "wb") as f:
                f.write(resposta.content)
            print(f"[OK] Baixado: {nome_arquivo}")
        else:
            print(f"[ERRO] {url} - Status {resposta.status_code}")
    except Exception as e:
        print(f"[FALHA] {url} - {e}")


