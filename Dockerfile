FROM python:3.11.12-bookworm

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código, incluindo a pasta src/
COPY . .

# Comando para rodar o script principal
CMD ["python3", "src/main.py"]
