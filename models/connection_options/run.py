from connection import DBConnectionHandler

dbHandle = DBConnectionHandler()
dbHandle.connect_to_DB()
con1 = dbHandle.get_db_connection()

print(con1)

class Dados:
    def __init__(self):
        """
        Inicializa a classe Avaliacao, estabelecendo conexões com as coleções necessárias no banco de dados.
        """
        self.getconnection = con1
        self.__aglomerados = self.getconnection.get_collection('aglomerados')
        self.__pesquisadores = self.getconnection.get_collection("pesquisadores")
        
    def inserir_dados(self, collection, documents):
        """
        Insere documentos em uma coleção do MongoDB.

        Args:
            collection (str): Nome da coleção onde os dados serão inseridos.
            documents (list): Lista de dicionários contendo os dados a serem inseridos.
        """
        if collection == 'aglomerados':
            if documents:
                for doc in documents:
                    filtro = {"unidade": doc["unidade"], "sigla": doc["sigla"]}
                    if not self.__aglomerados.find_one(filtro):  # Verifica se já existe
                        self.__aglomerados.insert_one(doc)
                        print(f"Documento inserido: {doc}")
                    else:
                        print(f"Documento já existe no banco: {doc}")
                self.__aglomerados.insert_many(documents)
                print(f"Dados inseridos na coleção 'aglormerados': {len(documents)} documentos")
            else:
                print("Nenhum documento inserido na coleção 'aglomerados'")
        elif collection == 'pesquisadores':
            if documents:
                self.__aglomerados.insert_many(documents)
                print(f"Dados inseridos na coleção 'pesquisadores': {len(documents)} documentos")
            else:
                print("Nenhum documento inserido na coleção 'aglomerados'")
        else: 
            print(f"Coleção {collection} não reconhecida")

    def verificar_insercao(self, documentos):
        pass 