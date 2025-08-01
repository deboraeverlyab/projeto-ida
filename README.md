# Projeto IDA - Indicadores de Desempenho no Atendimento (Anatel)

## Descrição

Este projeto automatiza o download, processamento e armazenamento dos Indicadores de Desempenho no Atendimento (IDA) da Anatel, entre os anos de 2015 e 2019, para os serviços SMP, STFC e SCM.

Os dados são baixados dos arquivos `.ods` públicos da Anatel, combinados em um único DataFrame, e salvos em uma tabela PostgreSQL. Em seguida, uma view SQL é criada para analisar a taxa de variação mensal desses indicadores, por grupo econômico.

---

## Funcionalidades

- Download automático dos arquivos `.ods` por serviço e ano.
- Leitura e união dos dados em um DataFrame pandas.
- Armazenamento dos dados em uma tabela PostgreSQL.
- Criação de uma view SQL com cálculo da taxa de variação mensal.
- Consulta à view para visualização dos resultados.

---

## Requisitos

- Docker.

---

## Instalação e Uso com Docker

1. Clone o repositório:

   ```bash
   git clone https://github.com/deboraeverlyab/projeto-ida.git
   cd projeto-ida


2. Inicie os containers:

   ```bash
    docker-compose up --build


Isso vai:

- Criar e iniciar o container PostgreSQL.
- Executar o script Python que baixa, processa e salva os dados.
- Criar a view SQL.
- Consultar e exibir os dados da view no terminal do container.

3. Para parar os containers:

   ```bash
    docker-compose down

   
## Estrutura do Projeto

    .
    ├── src/
    │   ├── main.py               # Script principal
    │   ├── ler_unir_ods.py       # Funções para ler e unir arquivos .ods
    │   ├── baixar_dados.py       # Função para baixar arquivos .ods
    │   ├── sql.py                # Funções para salvar DataFrame e executar e visualizar SQL
    ├── scripts/
    │   ├── create_view.sql       # Script SQL que cria a view no banco
    │   ├── create_schemas.sql    # Script SQL que cria a tabela dimensão e fato
    ├── docker-compose.yml        # Arquivo de orquestração Docker
    ├── Dockerfile                # Imagem do container Python
    ├── requirements.txt          # Dependências Python
    └── README.md



# Contato
Criado por Débora Everly 

email: deboraeverlyl@hotmail.com

linkedin: https://www.linkedin.com/in/debora-everly/
