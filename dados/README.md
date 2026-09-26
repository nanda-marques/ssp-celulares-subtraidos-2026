# Dados

## Fonte

Secretaria de Segurança Pública do Estado de São Paulo (SSP-SP) — Portal de Dados Abertos.

- Página oficial: https://www.ssp.sp.gov.br/estatistica/consultas
- Consulta: **Celulares subtraídos**
- Ano: **2026**

## Como obter

1. Acesse https://www.ssp.sp.gov.br/estatistica/consultas
2. Selecione **Celulares subtraídos** > ano **2026**
3. Baixe o arquivo `.xlsx` (contém 3 abas: `METODOLOGIA`, `DICIONARIO DE DADOS`, `CELULAR_2026`)
4. Salve como `dados/celulares_subtraidos_2026.xlsx`

## Tratamento aplicado

O script `scripts/01_tratamento.py`:

- lê a aba `CELULAR_2026`;
- mantém apenas registros com `DATA_OCORRENCIA_BO` em **2026**;
- cria colunas derivadas `ANO`, `MES` e `ANO_MES`;
- converte colunas de texto para `string` (evita erro de tipo misto no Parquet);
- salva o resultado em `dados/tratado.parquet` (não versionado).

## Dicionário resumido das variáveis usadas

| Coluna | Descrição |
|---|---|
| `DATA_OCORRENCIA_BO` | Data do fato |
| `NOME_MUNICIPIO` | Município do fato |
| `RUBRICA` | Classificação do delito |
| `DESCR_TIPOLOCAL` | Tipo do local (via pública, residência etc.) |
| `LATITUDE` / `LONGITUDE` | Coordenadas geográficas do local |
| `QUANTIDADE_OBJETO` | Quantidade de celulares subtraídos no registro |

Os dados originais **não são versionados** neste repositório por questões de tamanho e de boas práticas.