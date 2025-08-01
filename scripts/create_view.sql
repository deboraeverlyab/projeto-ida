DROP VIEW IF EXISTS view_taxa_variacao;

CREATE VIEW view_taxa_variacao AS
WITH dados_filtrados AS (
    SELECT
        dt.mes AS mes,
        dt.ano AS ano,
        dt.mes_numero AS mes_numero,
        dge.nome_grupo_economico AS grupo_economico,
        fi.valor AS valor
    FROM fato_ida fi
    JOIN dim_tempo dt ON fi.id_tempo = dt.id_tempo
    JOIN dim_grupo_economico dge ON fi.id_grupo_economico = dge.id_grupo_economico
    JOIN dim_variavel dv ON fi.id_variavel = dv.id_variavel
    WHERE dv.nome_variavel = 'Indicador de Desempenho no Atendimento (IDA)'
),
valores_com_variacao AS (
    SELECT
        TO_DATE(mes, 'YYYY-MM') AS data_mes,
        grupo_economico,
        valor,
        LAG(valor) OVER (PARTITION BY grupo_economico ORDER BY TO_DATE(mes, 'YYYY-MM')) AS valor_anterior
    FROM dados_filtrados
),
variacoes AS (
    SELECT
        data_mes,
        grupo_economico,
        valor,
        valor_anterior,
        CASE
            WHEN valor_anterior IS NOT NULL AND valor_anterior <> 0
                THEN ((valor - valor_anterior) / valor_anterior) * 100
            ELSE NULL
        END AS taxa_variacao
    FROM valores_com_variacao
),
media_mensal AS (
    SELECT
        data_mes,
        ROUND(AVG(taxa_variacao)::numeric, 2) AS taxa_variacao_media
    FROM variacoes
    GROUP BY data_mes
),
pivotado AS (
    SELECT
        v.data_mes,
        m.taxa_variacao_media,
        ROUND(MAX(CASE WHEN grupo_economico = 'ALGAR' THEN taxa_variacao - m.taxa_variacao_media END)::numeric, 2) AS ALGAR,
        ROUND(MAX(CASE WHEN grupo_economico = 'CLARO' THEN taxa_variacao - m.taxa_variacao_media END)::numeric, 2) AS CLARO,
        ROUND(MAX(CASE WHEN grupo_economico = 'OI' THEN taxa_variacao - m.taxa_variacao_media END)::numeric, 2) AS OI,
        ROUND(MAX(CASE WHEN grupo_economico = 'TIM' THEN taxa_variacao - m.taxa_variacao_media END)::numeric, 2) AS TIM,
        ROUND(MAX(CASE WHEN grupo_economico = 'VIVO' THEN taxa_variacao - m.taxa_variacao_media END)::numeric, 2) AS VIVO
    FROM variacoes v
    JOIN media_mensal m ON v.data_mes = m.data_mes
    GROUP BY v.data_mes, m.taxa_variacao_media
)
SELECT
    TO_CHAR(data_mes, 'YYYY-MM') AS mes,
    taxa_variacao_media,
    ALGAR,
    CLARO,
    OI,
    TIM,
    VIVO
FROM pivotado
ORDER BY data_mes;