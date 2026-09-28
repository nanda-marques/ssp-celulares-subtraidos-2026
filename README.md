# Celulares Subtraídos no Estado de São Paulo — 2026

Análise interativa dos registros de **celulares subtraídos** no estado de São Paulo, com base nos dados abertos da **Secretaria de Segurança Pública do Estado de São Paulo (SSP-SP)**.

O projeto entrega três visualizações — **exploração interativa**, **série temporal** e **mapa geográfico** — em uma aplicação única desenvolvida em Python com **Streamlit**, **Plotly** e **Folium**.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red)
---

## Sobre a base de dados

- **Fonte:** Secretaria de Segurança Pública do Estado de São Paulo — Portal de Dados Abertos
- **Referência oficial:** https://www.ssp.sp.gov.br/estatistica/consultas
- **Recorte:** ocorrências com `DATA_OCORRENCIA_BO` em **2026**
- **Volume final após tratamento:** **163.485 registros** e **178.518 celulares** subtraídos

Detalhes em [`dados/README.md`](dados/README.md).

---

## Funcionalidades

### 1. Exploração interativa
Dashboard com quatro filtros combináveis — **Mês**, **Município**, **Rubrica** e **Tipo de Local** — que atualizam em tempo real:
- KPIs (total de celulares, ocorrências, municípios atingidos);
- ranking dos 15 municípios com maior volume;
- distribuição percentual das 8 principais rubricas.

### 2. Série temporal
Gráfico de linha com a evolução mensal dos registros em 2026, com destaque para o **pico** e o **menor volume** do período.

### 3. Georreferenciamento
Mapa interativo combinando:
- **heatmap** de densidade das ocorrências (amostra de até 15 mil pontos);
- **círculos proporcionais** ao volume por município, com popup informativo.

---

## Stack 

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Manipulação de dados | pandas, pyarrow |
| Visualização | Plotly, Folium |
| Aplicação | Streamlit, streamlit-folium |
| Formato intermediário | Parquet |

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/nanda-marques/ssp-celulares-subtraidos-2026.git
cd ssp-celulares-subtraidos-2026
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Baixar a base de dados
Siga as instruções em ``dados/README.md`` e salve o arquivo como ``dados/celulares_subtraidos_2026.xlsx.``

### 5. Tratar os dados

```bash
python scripts/tratamento.py
```

### 6. Rodar a aplicação
```bash
streamlit run scripts/app.py
```

### Resultados Principais

* **Exploração Interativa:** Os filtros demonstram concentração expressiva na Região Metropolitana de São Paulo. Ao restringir para a capital, a participação relativa dos demais municípios cai drasticamente, evidenciando o peso da cidade de São Paulo no total estadual.

* **Série Temporal:** A análise mensal de 2026 apresenta os seguintes indicadores:

| Indicador | Valor / Referência |
| :--- | :--- |
| **Período de maior valor** | Maio/2026 — 28.205 unidades |
| **Período de menor valor** | Junho/2026 — 22.856 unidades |
| **Tendência** | Oscilante, sem crescimento ou queda sustentada no período disponível |

> *Nota:* O ano-base 2026 está incompleto na base consultada (dados consolidados até julho), o que limita conclusões definitivas sobre a tendência anual.

* **Distribuição Geográfica:** O mapa revelou que o crime se concentra onde há maior densidade populacional, maior circulação de pedestres e maior quantidade de aparelhos em uso. A forte presença na Baixada Santista (Itanhaém, Praia Grande) sugere que o verificar pontos turísticos também é um fator importante. 
