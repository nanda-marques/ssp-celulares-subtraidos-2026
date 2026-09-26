import base64
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import branca.colormap as cm

st.set_page_config(
    page_title="SSP/SP - Celulares Subtraídos",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .logo-container {
        background-color: #0B132B;
        padding: 18px 12px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .logo-container img {
        width: 100%;
        max-width: 190px;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    .ssp-header {
        padding: 24px;
        border-radius: 8px;
        background: linear-gradient(135deg, #0B2545 0%, #134074 100%);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(11, 37, 69, 0.15);
        margin-bottom: 24px;
    }
    .ssp-header h1 {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .ssp-header p {
        margin: 8px 0 0 0;
        color: #CEE1F2;
        font-size: 0.95rem;
    }
    .ssp-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 8px;
        color: #ffffff;
    }
    .kpi-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-left: 4px solid #134074;
        border-radius: 6px;
        padding: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .kpi-card h3 {
        margin: 0;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--text-color);
        opacity: 0.7;
        font-weight: 600;
    }
    .kpi-card p {
        margin: 8px 0 0 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-color);
    }
    .kpi-card small {
        display: block;
        margin-top: 4px;
        color: #134074;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .sidebar-metrics {
        margin-top: 16px;
        padding: 14px;
        border-radius: 6px;
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        font-size: 0.85rem;
    }
    .ssp-footer {
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid rgba(128, 128, 128, 0.2);
        text-align: center;
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


def renderizar_logo():
    logo_path = Path("assets/brasao.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""<div class="logo-container">
                <img src="data:image/png;base64,{encoded}" alt="Brasão SSP/SP">
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """<div class="logo-container">
                <h3 style='color: white; margin:0; font-size:1.1rem;'>SSP / SP</h3>
            </div>""",
            unsafe_allow_html=True,
        )


@st.cache_data
def carregar():
    return pd.read_parquet("dados/tratado.parquet")


df = carregar()

with st.sidebar:
    renderizar_logo()
    st.markdown("### Filtros de Consulta")

meses_disp = sorted(df["MES"].dropna().unique().tolist())
meses_sel = st.sidebar.multiselect("Mês", meses_disp, default=meses_disp)

top_municipios = (
    df.groupby("NOME_MUNICIPIO")["QUANTIDADE_OBJETO"]
    .sum()
    .sort_values(ascending=False)
    .head(30)
    .index.tolist()
)
municipios_sel = st.sidebar.multiselect("Município (Top 30)", top_municipios, default=top_municipios)

rubricas_disp = sorted(df["RUBRICA"].dropna().unique().tolist())
rubricas_sel = st.sidebar.multiselect("Rubrica", rubricas_disp, default=rubricas_disp)

locais_disp = sorted(df["DESCR_TIPOLOCAL"].dropna().unique().tolist())
locais_sel = st.sidebar.multiselect("Tipo de Local", locais_disp, default=locais_disp)

filtro = df[
    (df["MES"].isin(meses_sel))
    & (df["NOME_MUNICIPIO"].isin(municipios_sel))
    & (df["RUBRICA"].isin(rubricas_sel))
    & (df["DESCR_TIPOLOCAL"].isin(locais_sel))
].copy()

st.sidebar.markdown(
    f"""<div class="sidebar-metrics">
        <b>Registros Filtrados:</b><br>
        <span style="font-size: 1.25rem; font-weight: 700;">{len(filtro):,}</span>
    </div>""".replace(",", "."),
    unsafe_allow_html=True,
)

st.markdown("""
<div class="ssp-header">
    <h1>VISUALIZAÇÃO DE DADOS - Celulares Subtraídos</h1>
    <p>
        <span class="ssp-badge">Ano Base: 2026</span>
        <span class="ssp-badge">Portal de Dados Abertos</span>
        <span class="ssp-badge">Secretaria de Segurança Pública do Estado de São Paulo</span>
    </p>
</div>
""", unsafe_allow_html=True)

aba1, aba2, aba3 = st.tabs(["Visão Geral", "Série Temporal", "Georreferenciamento"])

with aba1:
    # Fonte alinhada ao tema do Streamlit (Source Sans Pro é o padrão)
    FONTE = "Source Sans Pro, sans-serif"
    COR_TEXTO = "#0B2545"   # azul-marinho institucional

    total_cel = int(filtro["QUANTIDADE_OBJETO"].sum())
    total_reg = len(filtro)
    mun_dist = filtro["NOME_MUNICIPIO"].nunique()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="kpi-card"><h3>Total de Celulares</h3><p>{total_cel:,}</p><small>Soma da quantidade de objetos</small></div>""".replace(",", "."),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="kpi-card"><h3>Ocorrências Registradas</h3><p>{total_reg:,}</p><small>Boletins de ocorrência</small></div>""".replace(",", "."),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="kpi-card"><h3>Municípios Atingidos</h3><p>{mun_dist}</p><small>Com registros no filtro</small></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_esq, col_dir = st.columns([3, 2], gap="large")

    with col_esq:
        st.markdown("#### Maiores Volumes por Município")
        agrupado = (
            filtro.groupby("NOME_MUNICIPIO")["QUANTIDADE_OBJETO"]
            .sum()
            .reset_index()
            .sort_values("QUANTIDADE_OBJETO", ascending=False)
            .head(15)
        )

        fig = px.bar(
            agrupado,
            x="QUANTIDADE_OBJETO",
            y="NOME_MUNICIPIO",
            orientation="h",
            color="QUANTIDADE_OBJETO",
            color_continuous_scale=[
                "#E3F2FD",
                "#64B5F6",
                "#1E88E5",
                "#0D47A1",
                "#0A2A66",
            ],
            labels={"QUANTIDADE_OBJETO": "Quantidade", "NOME_MUNICIPIO": ""},
        )
        fig.update_traces(
            marker_line_color="#0A2A66",
            marker_line_width=0.8,
            text=agrupado["QUANTIDADE_OBJETO"].apply(lambda x: f"{x:,}".replace(",", ".")),
            textposition="outside",
            textfont=dict(color="#2D468B", size=12, family=FONTE),
            cliponaxis=False,
        )
        fig.update_layout(
            font=dict(family=FONTE, size=13, color=COR_TEXTO),
            yaxis=dict(autorange="reversed", showgrid=False, zeroline=False),
            xaxis=dict(
                tickformat=",.0f",
                title=dict(text="Quantidade", font=dict(family=FONTE, size=13)),
                gridcolor="rgba(11,37,69,0.08)",
                zeroline=False,
            ),
            coloraxis_showscale=False,
            margin=dict(l=10, r=60, t=10, b=10),
            height=520,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_dir:
        st.markdown("#### Principais Rubricas")
        por_rubrica = (
            filtro.groupby("RUBRICA")["QUANTIDADE_OBJETO"]
            .sum()
            .reset_index()
            .sort_values("QUANTIDADE_OBJETO", ascending=False)
            .head(8)
        )

        cores = [
            "#0B2545",
            "#134074",
            "#2C5F7C",
            "#3E7CB1",
            "#5C8A8A",
            "#7A3E48",
            "#A67C52",
            "#BFC9D1",
        ]

        fig2 = px.pie(
            por_rubrica,
            names="RUBRICA",
            values="QUANTIDADE_OBJETO",
            color_discrete_sequence=cores,
        )
        fig2.update_traces(
            textposition="inside",
            textinfo="percent",
            textfont=dict(color="#FFFFFF", size=13, family=FONTE),
            insidetextorientation="horizontal",
            marker=dict(line=dict(color="#FFFFFF", width=1.5)),
            pull=[0.03] * len(por_rubrica),
        )
        fig2.update_layout(
            font=dict(family=FONTE, size=13, color=COR_TEXTO),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=520,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.10,
                xanchor="center",
                x=0.5,
                font=dict(family=FONTE, size=13, color=COR_TEXTO),
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="#BFC9D1",
                borderwidth=1,
                itemsizing="constant",
                itemwidth=30,
            ),
        )
        st.plotly_chart(fig2, use_container_width=True)

with aba2:
    st.markdown("#### Evolução Mensal dos Registros")
    serie = (
        filtro.groupby("ANO_MES")["QUANTIDADE_OBJETO"]
        .sum()
        .reset_index()
        .sort_values("ANO_MES")
    )

    if serie.empty:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=serie["ANO_MES"],
                y=serie["QUANTIDADE_OBJETO"],
                mode="lines+markers",
                line=dict(color="#134074", width=3, shape="spline"),
                marker=dict(size=8, color="#0B2545"),
                fill="tozeroy",
                fillcolor="rgba(19, 64, 116, 0.1)",
                hovertemplate="<b>%{x}</b><br>%{y:,} celulares<extra></extra>",
            )
        )

        maximo = serie.loc[serie["QUANTIDADE_OBJETO"].idxmax()]
        minimo = serie.loc[serie["QUANTIDADE_OBJETO"].idxmin()]

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickangle=-45),
            yaxis=dict(title="Qtd. Celulares"),
            margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f"""<div class="kpi-card"><h3>Pico de Ocorrências</h3><p>{maximo['ANO_MES']}</p><small>{int(maximo['QUANTIDADE_OBJETO']):,} unidades</small></div>""".replace(",", "."),
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""<div class="kpi-card"><h3>Menor Volume</h3><p>{minimo['ANO_MES']}</p><small>{int(minimo['QUANTIDADE_OBJETO']):,} unidades</small></div>""".replace(",", "."),
                unsafe_allow_html=True,
            )

with aba3:
    st.markdown("#### Mapeamento Espacial das Ocorrências")
    geo = filtro.dropna(subset=["LATITUDE", "LONGITUDE"])
    geo = geo[geo["LATITUDE"].between(-25, -19) & geo["LONGITUDE"].between(-54, -44)]

    if geo.empty:
        st.warning("Nenhum registro com coordenadas geográficas válidas para o filtro atual.")
    else:
        por_mun = (
            geo.groupby("NOME_MUNICIPIO")
            .agg(
                qtd=("QUANTIDADE_OBJETO", "sum"),
                lat=("LATITUDE", "mean"),
                lon=("LONGITUDE", "mean"),
            )
            .reset_index()
        )

        m = folium.Map(
            location=[-23.55, -46.63],
            zoom_start=7,
            tiles="OpenStreetMap",
            attr="OpenStreetMap",
        )

        amostra = geo.sample(n=min(15000, len(geo)), random_state=42)
        HeatMap(
            amostra[["LATITUDE", "LONGITUDE"]].values.tolist(),
            radius=7,
            blur=12,
            min_opacity=0.3,
            gradient={
                0.2: "#457B9D",   
                0.5: "#F4A261",   
                0.8: "#E76F51",  
                1.0: "#9B2226",  
            },
        ).add_to(m)

        colormap = cm.LinearColormap(
            ["#457B9D", "#F4A261", "#E76F51", "#9B2226"],
            vmin=por_mun["qtd"].min(),
            vmax=por_mun["qtd"].max(),
        )
        max_q = por_mun["qtd"].max()

        for _, r in por_mun.iterrows():
            folium.CircleMarker(
                location=[r["lat"], r["lon"]],
                radius=4 + (r["qtd"] / max_q) * 20,
                color=colormap(r["qtd"]),
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>{r['NOME_MUNICIPIO']}</b><br>{int(r['qtd']):,} celulares".replace(",", "."),
                    max_width=200,
                ),
            ).add_to(m)

        colormap.caption = "Volume por Município"
        colormap.add_to(m)

        st_folium(m, width=None, height=600, returned_objects=[])
        st.caption("Visualização combinada: Mapa de calor de densidade e círculos proporcionais por município.")

st.markdown(
    """<div class="ssp-footer">Secretaria de Segurança Pública do Estado de São Paulo (SSP-SP) — Disponível em: <a href="https://www.ssp.sp.gov.br/estatistica/consultas"> www.ssp.sp.gov.br/estatistica/consultas</a></div>""",
    unsafe_allow_html=True,
)