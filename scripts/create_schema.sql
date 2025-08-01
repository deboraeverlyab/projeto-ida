CREATE TABLE IF NOT EXISTS dim_tempo (
    id_tempo SERIAL PRIMARY KEY,
    mes VARCHAR(7) UNIQUE NOT NULL,
    ano INT NOT NULL,
    mes_numero INT NOT NULL,
    trimestre INT NOT NULL,
    semestre INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_servico (
    id_servico SERIAL PRIMARY KEY,
    nome_servico VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_grupo_economico (
    id_grupo_economico SERIAL PRIMARY KEY,
    nome_grupo_economico VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_variavel (
    id_variavel SERIAL PRIMARY KEY,
    nome_variavel VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS fato_ida (
    id_fato SERIAL PRIMARY KEY,
    id_tempo INT NOT NULL REFERENCES dim_tempo(id_tempo),
    id_servico INT NOT NULL REFERENCES dim_servico(id_servico),
    id_grupo_economico INT NOT NULL REFERENCES dim_grupo_economico(id_grupo_economico),
    id_variavel INT NOT NULL REFERENCES dim_variavel(id_variavel),
    valor NUMERIC(10, 2),
    CONSTRAINT unique_fato_ida UNIQUE (id_tempo, id_servico, id_grupo_economico, id_variavel)
);
