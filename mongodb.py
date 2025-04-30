import pandas as pd
import requests
from time import sleep

class Dados:
    def __init__(self, connection):
        """
        Inicializa a classe Dados, estabelecendo conexões com as coleções necessárias no banco de dados.
        Args: 
            connection (str): Conexão ao banco de dados mongoDB.
        """
        self.getconnection = connection
        self.__aglomerados = self.getconnection.get_collection('aglomerados')
        self.__pesquisadores = self.getconnection.get_collection("pesquisadores")
        
    def inserir_dados_embrapii(self, collection, documents):
        """
        Insere documentos em uma coleção do MongoDB, evitando duplicações.

        Args:
            collection (str): Nome da coleção onde os dados serão inseridos.
            documents (list): Lista de dicionários contendo os dados a serem inseridos.
        """
        if collection == 'aglomerados':
            for doc in documents:
                filtro = {"unidade": doc["unidade"], "sigla": doc["sigla"]}
                if  self.__aglomerados.find_one(filtro):  # Verifica se já existe
                    print(f"Documento já existe no banco e será ignorado: {doc}")
                else:
                    self.__aglomerados.insert_one(doc)
                    print(f"Documento inserido: {doc}")
        
        elif collection == 'pesquisadores':
            for doc in documents:
                filtro = {"email": doc["email"]}  # Exemplo de chave para evitar duplicações
                if not self.__pesquisadores.find_one(filtro):
                    self.__pesquisadores.insert_one(doc)
                    print(f"Documento inserido: {doc}")
                else:
                    print(f"Documento já existe no banco e será ignorado: {doc}")
        else: 
            print(f"Coleção {collection} não reconhecida")

    def inserir_dados_incts(self, collection, documents):
        """
        Insere documentos em uma coleção do MongoDB, evitando duplicações.

        Args:
            collection (str): Nome da coleção onde os dados serão inseridos.
            documents (list): Lista de dicionários contendo os dados a serem inseridos.
        """
        if collection == 'aglomerados':
            for doc in documents:
                filtro = {"sigla": doc["sigla"]}
                if  self.__aglomerados.find_one(filtro):  # Verifica se já existe
                    print(f"Documento já existe no banco e será ignorado: {doc}")
                else:
                    self.__aglomerados.insert_one(doc)
                    print(f"Documento inserido: {doc}")
        
        elif collection == 'pesquisadores':
            for doc in documents:
                filtro = {"email": doc["email"]}  # Exemplo de chave para evitar duplicações
                if not self.__pesquisadores.find_one(filtro):
                    self.__pesquisadores.insert_one(doc)
                    print(f"Documento inserido: {doc}")
                else:
                    print(f"Documento já existe no banco e será ignorado: {doc}")
        else: 
            print(f"Coleção {collection} não reconhecida")

    def corrigir_planilhas(self):
        try:
            filtro = {"nome": {"$exists": True}}
            self.__aglomerados.update_many(
                filtro,
                {"$rename": {"nome": "unidade"}}
            )
            print("Planilha corrigida com sucess")
        except Exception as e:
            print(f"Erro: {e}")

    def agrupar_docs_grafico1(self):
        lista = []
        try:
            filtro = {"sigla": {"$exists": True}}
            itens = self.__aglomerados.find(
                filtro
            )
            for item in itens:
                documento = {
                "Políticas de Neoindustrialização": item["politica"],
                "Instituição": item["unidade"],
                }
                lista.append(documento)
        except Exception as e:
            print(f"Erro: {e}")
        return lista
    
    def adicionar_coordenadas(self):
        """
        Adiciona coordenadas geográficas (latitude e longitude) aos documentos dos aglomerados com base no nome da cidade.
        """
        aglomerados = self.__aglomerados.find({"cidade": {"$exists": True, "$ne": ""}, "coordenadas": {"$exists": False}})

        for aglomerado in aglomerados:
            cidade = aglomerado.get("cidade")
            uf = "Minas Gerais"

            if cidade: 
                try: 
                    url = f"https://nominatim.openstreetmap.org/search"
                    params = {
                        'q': f"{cidade}, {uf}, Brasil",
                        'format': 'json',
                        'limit': 1
                    }

                    response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
                    data = response.json()

                    if data: 
                        latitude = float(data[0]['lat'])
                        longitude = float(data[0]['lon'])

                        self.__aglomerados.update_one(
                            {"_id": aglomerado["_id"]},
                            {"$set": {"coordenadas": {"lat": latitude, "lon": longitude}}}
                        )
                        print(f"Coordenadas adicionadas para {cidade}: {latitude}, {longitude}")
                    else:
                        print(f"Coordenadas não encontradas para {cidade}")
                except Exception as e:
                    print(f"erro ao buscar coordenadas para {cidade}: {e}")
                sleep(3)    
    
    def carregar_e_agrupar_dados(self):
        """
        Carrega os dados dos aglomerados com coordenadas e agrupa as unidades que compartilham as mesmas coordenadas.
        """
        # Carregar os dados com coordenadas
        dados = list(self.__aglomerados.find({"coordenadas": {"$exists": True}}))
        
        # Criar DataFrame com as coordenadas e unidades
        df = pd.DataFrame([{
            "unidade": doc.get("unidade"),
            "lat": doc["coordenadas"]["lat"],
            "lon": doc["coordenadas"]["lon"]
        } for doc in dados])
        
        # Agrupar as unidades por coordenada
        df_agrupado = df.groupby(['lat', 'lon']).agg({
            'unidade': lambda x: '<br>'.join(x)  # Junta as unidades com a mesma coordenada
        }).reset_index()
        
        return df_agrupado
