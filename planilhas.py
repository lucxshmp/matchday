import pandas as pd
import numpy as np
from bson import ObjectId

class LerPlanilhas:
    def __init__(self):
        self.planilha = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTDLc6GWTLeOF-sDxyDs92KCUWPe0YBxoDtqBQZHjLOpnMu-GbJSJnC_V62zqOpixGMPlSotL-asFRR/pub?output=xlsx'

    def ler_planilha_embrapiis(self, sheetname):
        """
        Lê a planilha na aba selecionada.
        """
        colunas = ['unidades', 'sigla', 'tema', 'linhaspesquisa', 'frentes', 'pontoFocal', 'tel', 'email', 'areaP', 'politica']
        df = pd.read_excel(self.planilha, sheet_name=sheetname, usecols=colunas, dtype=str)

        # Preencher os valores NaN da coluna 'unidades' com o último valor válido
        df["unidades"] = df["unidades"].ffill()

        # Agrupar as linhas de pesquisa por unidades
        df_grouped = df.groupby("unidades")["linhaspesquisa"].apply(list).reset_index()
        
        # Fazer o merge com o DF original 
        df_merged = df.drop(columns=["linhaspesquisa"]).drop_duplicates(subset="unidades")
        df_final = pd.merge(df_merged, df_grouped, on="unidades", how="left")
        
        return pd.DataFrame(df_final)


    def processarlinhas_EMBRAPIIS(self, dataframe):
        """
        Agrupa as linhas de pesquisa e formata os documentos para inserção no banco.
        """
        documentos = []

        for unidade, grupo in dataframe.groupby("unidades", dropna=True):

            doc = {
            "unidade": unidade,
            "sigla": grupo["sigla"].iloc[0] if not grupo["sigla"].isna().all() else "",
            "tema": grupo["tema"].iloc[0] if not grupo["tema"].isna().all() else "",
            "frentes": grupo["frentes"].iloc[0] if not grupo["frentes"].isna().all() else "",
            "pontoFocal": grupo["pontoFocal"].iloc[0].strip() if not grupo["pontoFocal"].isna().all() and isinstance(grupo["pontoFocal"].iloc[0], str) else "",
            "tel": float(grupo["tel"].iloc[0]) if not grupo["tel"].isna().all() and str(grupo["tel"].iloc[0]).replace(".", "", 1).isdigit() else None,
            "email": grupo["email"].iloc[0] if not grupo["email"].isna().all() else "",
            "areaP": grupo["areaP"].iloc[0] if not grupo["areaP"].isna().all() else "",
            "politica": int(grupo["politica"].iloc[0]) if not grupo["politica"].isna().all() and str(grupo["politica"].iloc[0]).isdigit() else None,
            "linhaspesquisa": grupo["linhaspesquisa"].iloc[0] if not grupo["sigla"].isna().all() else "",
                
            }

            documentos.append(doc)

        return documentos

    def ler_planilha_incts(self, sheetname):
        """
        Lê a planilha na aba selecionada.
        """
        colunas = ['sigla', 'nome', 'site', 'instituicao', 'cidade', 'uf', 'missao_nib', 'tipo', 'email']
        df = pd.read_excel(self.planilha, sheet_name=sheetname, usecols=colunas, dtype=str)

        return pd.DataFrame(df)
    
    
    def processarlinhas_incts(self, dataframe):
        """
        Agrupa as linhas de pesquisa e formata os documentos para inserção no banco.
        """
        documentos = []

        for sigla, grupo in dataframe.groupby("sigla", dropna=True):
            if grupo["uf"].iloc[0].lower() == "mg":
                doc = {
                "sigla": sigla,
                "nome": grupo["nome"].iloc[0] if not grupo["nome"].isna().all() else "",
                "site": grupo["site"].iloc[0] if not grupo["site"].isna().all() else "",
                "instituicao": grupo["instituicao"].iloc[0] if not grupo["instituicao"].isna().all() else "",
                "cidade": grupo["cidade"].iloc[0] if not grupo["cidade"].isna().all() else "",
                "uf": grupo["uf"].iloc[0] if not grupo["uf"].isna().all() else "",
                "missao_nib": int(grupo["missao_nib"].iloc[0]) if not grupo["missao_nib"].isna().all() and str(grupo["missao_nib"].iloc[0]).isdigit() else None,
                "tipo": grupo["tipo"].iloc[0] if not grupo["tipo"].isna().all() else "",
                "email": grupo["email"].iloc[0] if not grupo["email"].isna().all() else "",
                }

                documentos.append(doc)

        return documentos