from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from models.connection_options.run import DBConnectionHandler
import plotly.graph_objects as go
import requests

# Carregar geojson com dados do Brasil
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
geojson_data = requests.get(geojson_url).json()

class DashApp:
    def __init__(self):
        self.app = Dash(__name__)

    def tratar_dados_grafico1(self, df):
        # Contar a quantidade de instituições por política
        df_agrupado = df.groupby("Políticas de Neoindustrialização")["Instituição"].nunique().reset_index()
        df_agrupado.rename(columns={"Instituição": "Quantidade de Instituições"}, inplace=True)
        return df_agrupado

    def criarMapa(self, df_coords):
        # Filtrar o estado de Minas Gerais
        mg_feature = next((f for f in geojson_data["features"] if f["properties"]["name"] == "Minas Gerais"), None)
        
        if mg_feature is None:
            return go.Figure()  # Retorna uma figura vazia caso não encontre MG

        # Criar mapa com o estado de MG
        fig = go.Figure(go.Choroplethmapbox(
            geojson={"type": "FeatureCollection", "features": [mg_feature]},
            locations=["Minas Gerais"],
            z=[1],
            featureidkey="properties.name",
            colorscale=[[0, "green"], [1, "green"]],
            showscale=False,
            marker_opacity=0.6,
            marker_line_width=1
        ))

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=5.2,
            mapbox_center={"lat": -18.5, "lon": -44},
            mmargin={"r": 10, "t": 10, "l": 10, "b": 10},
            height=500
        )

        # Adiciona os marcadores dos aglomerados
        fig.add_trace(go.Scattermapbox(
            lat=df_coords["lat"],
            lon=df_coords["lon"],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=25,
                color='rgba(0, 150, 255, 0.4)',
                opacity=0.5
            ),
            text=df_coords["unidade"],
            hoverinfo='text'
        ))

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=5.5,
            mapbox_center={"lat": -18.5, "lon": -44},
            margin={"r":0,"t":0,"l":0,"b":0},
            height=500
        )

        return fig
    

    def criar_layout(self, df, df_coords):
        """Cria o layout do Dash"""
        if df.empty:
            return html.Div("Nenhum dado encontrado no banco")
        
        paleta_personalizada = [
        "#010221",  # RockON!-1-hex
        "#0A7373",  # RockON!-2-hex
        "#B7BF99",  # RockON!-3-hex
        "#EDAA25",  # RockON!-4-hex
        "#C43302",  # RockON!-5-hex
        ]

        # Gráfico de barras
        fig_bar = px.bar(df,
                        x="Políticas de Neoindustrialização",
                        y="Quantidade de Instituições",
                        barmode="group",
                        color_discrete_sequence=px.colors.qualitative.Set2)

        fig_bar.update_traces(
            text=df["Quantidade de Instituições"],
            textposition='outside'
        )

        fig_bar.update_layout(
            title="Distribuição de Instituições por Política de Neoindustrialização",
            xaxis_title="Políticas de Neoindustrialização",
            yaxis_title="Quantidade de Instituições",
            xaxis_tickangle=0,
            plot_bgcolor="#f9f9f9",
            paper_bgcolor="#f9f9f9",
            font=dict(family="Arial", size=14)
        )

        # Layout com dois gráficos
        return html.Div(style={'padding': '20px', 'fontFamily': 'Montserrat'}, children=[
            html.H1(
                "Dashboard de Aglomerados de Tecnologia",
                style={
                    "textAlign": "center",
                    "backgroundColor": "#25766F",
                    "color": "white",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "fontFamily": "Arial"
                }
            ),
            html.Div("Distribuição das instituições por política de neoindustrialização.",
                    style={"textAlign": "center", "marginBottom": "20px"}),

            dcc.Graph(id='grafico1', figure=fig_bar),

            html.H1("Complexos de pesquisa, desenvolvimento e inovação no estado de Minas Gerais",
                    style={
                    "textAlign": "center",
                    "backgroundColor": "#25766F",
                    "color": "white",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "fontFamily": "Arial"
                }
            ),

            dcc.Graph(id="mapa-MG", figure=self.criarMapa(df_coords))
        ])
    



