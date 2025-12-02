from database.DB_connect import DBConnect
from model.connessione import Connessione   #fare classe connessione e classe rifugio
from model.rifugio import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def leggi_connessione():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        try:
            cursor.execute(query)
            for row in cursor:
                connessione = Connessione(row["id"],row["id_rifugio1"], row["id_rifugio2"], row["distanza"], row["difficolta"], row["durata"], row["anno"])
                result.append(connessione)
        except Exception as e:
            print(f"errore durante la lettura della query")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def leggi_rifugio():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        try:
            cursor.execute(query)
            for row in cursor:
                rifugio = Rifugio(row["nome"], row["localita"], row["altitudine"], row["capienza"],row["aperto"])
                result.append(rifugio)
        except Exception as e:
            print(f"errore durante la lettura della query")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result



