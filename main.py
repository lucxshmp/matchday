from models.connection_options.run import DBConnectionHandler
from mongodb import Dados
from planilhas import LerPlanilhas
import pandas as pd
from dash import Dash
from app import DashApp
import os

def main():
    # Criar conexão com o banco de dados
    dbHandle = DBConnectionHandler()
    dbHandle.connect_to_DB()
    con1 = dbHandle.get_db_connection()
    
    # Criar instância da classe Dados
    dados_db = Dados(con1)
    # Criar instância da classe LerPlanilhas
    leitor = LerPlanilhas()
    #Criar instância da classe DashApp
    grafico1 =  DashApp()
    df_mapa = dados_db.carregar_e_agrupar_dados()

    """Fazer esse procedimento caso adicionar mais informações de outros institutos na planilha"""
    #try:
        # Ler a planilha
        #nome_aba = "incts"  # lendo a aba de incts
        #df = leitor.ler_planilha_incts(nome_aba)
        
        # Processar os dados
        #documentos = leitor.processarlinhas_incts(df)
        
        #Inserir no banco
        #if documentos:
            #dados_db.inserir_dados_incts('aglomerados', documentos)
        #else:
            #print("Nenhum documento para inserir.")

    #except Exception as e:
    #    print(f"Erro: {e}")

    df_grafico1 = pd.DataFrame(dados_db.agrupar_docs_grafico1())
    df_grafico1 = grafico1.tratar_dados_grafico1(df_grafico1)
    layoutgrafico1 = grafico1.criar_layout(df_grafico1, df_mapa)

    mapa = grafico1.criarMapa(df_mapa)
    grafico1.app.layout = layoutgrafico1
    port = int(os.environ.get("PORT", 8050))
    grafico1.app.run(host="0.0.0.0", port=port, debug=False)
    
    

if __name__ == "__main__":
    main()
