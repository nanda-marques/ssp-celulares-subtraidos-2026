import pandas as pd

ARQUIVO = "dados/celulares_subtraidos_2026.xlsx"
ABA = "CELULAR_2026"

# Aba CELULAR_2026
df = pd.read_excel(ARQUIVO, sheet_name=ABA)
df.columns = df.columns.str.strip()

print(f"Linhas lidas: {len(df)}  |  Colunas: {df.shape[1]}")

# 2) Garantir datetime
df["DATA_OCORRENCIA_BO"] = pd.to_datetime(df["DATA_OCORRENCIA_BO"], errors="coerce")

# FILTRO: apenas ocorrências de 2026
antes = len(df)
df = df[df["DATA_OCORRENCIA_BO"].dt.year == 2026].copy()
print(f"Linhas de 2026: {len(df)}  (removidas: {antes - len(df)})")

# Colunas derivadas de tempo da DATA_OCORRENCIA_BO
df["ANO"] = df["DATA_OCORRENCIA_BO"].dt.year
df["MES"] = df["DATA_OCORRENCIA_BO"].dt.month
df["ANO_MES"] = df["DATA_OCORRENCIA_BO"].dt.to_period("M").astype(str)

# Dados numéricos
df["QUANTIDADE_OBJETO"] = pd.to_numeric(df["QUANTIDADE_OBJETO"], errors="coerce").fillna(1)
df["LATITUDE"] = pd.to_numeric(df["LATITUDE"], errors="coerce")
df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"], errors="coerce")

# Padronizar colunas de texto (para evitar erro de tipo misto)
colunas_texto = df.select_dtypes(include=["object", "string"]).columns
for col in colunas_texto:
    df[col] = df[col].astype("string")

# Garantir tipos numéricos em colunas a serem analisadas
df["QUANTIDADE_OBJETO"] = pd.to_numeric(df["QUANTIDADE_OBJETO"], errors="coerce").fillna(1).astype("int64")
df["LATITUDE"] = pd.to_numeric(df["LATITUDE"], errors="coerce")
df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"], errors="coerce")
df["MES"] = df["MES"].astype("int64")
df["ANO"] = df["ANO"].astype("int64")

# Salvar dados tratados em formato adequado para análise de dados, big data
df.to_parquet("dados/tratado.parquet")

# Verificação:
print("\n--- Verificação final ---")
print("Anos únicos:", sorted(df["ANO"].dropna().unique()))
print("Meses únicos:", sorted(df["MES"].dropna().unique()))
print("Municípios únicos:", df["NOME_MUNICIPIO"].nunique())
print("Rubricas únicas:", df["RUBRICA"].nunique())
print(f"Shape final: {df.shape}")
print(f"Total de celulares (soma QUANTIDADE_OBJETO): {int(df['QUANTIDADE_OBJETO'].sum())}")