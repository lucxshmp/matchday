from connection import DBConnectionHandler

dbHandle = DBConnectionHandler()
dbHandle.connect_to_DB()
con1 = dbHandle.get_db_connection()
