import networkx as nx
from database.dao import DAO
from model.rifugio import Rifugio
from model.connessione import Connessione

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._id_map = {}
        # Lista di tutti i rifugi (lettura dal DAO)
        self._all_rifugi = DAO.leggi_rifugio()
        # Popola la mappa ID
        if self._all_rifugi:
            self._id_map = {}

            for rifugio in self._all_rifugi:
                # Usa l'ID del rifugio come chiave e l'oggetto rifugio come valore
                self._id_map[rifugio.id] = rifugio

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni.
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        # 1. Resetto il grafo
        self.G.clear()

        # 2. Ottengo le connessioni filtrate direttamente dal DAO
        connessioni_filtrate: list[Connessione] = DAO.leggi_connessione(year)

        if connessioni_filtrate is None:
            print("AVVISO: Nessuna connessione caricata dal DAO.")
            self.G.clear()
            return

        # 3. Identifico i nodi (oggetti Rifugio) coinvolti
        nodi_coinvolti_id: set[int] = set()
        for c in connessioni_filtrate:
            nodi_coinvolti_id.add(c.id_rifugio1)
            nodi_coinvolti_id.add(c.id_rifugio2)

        # 4. Aggiungo i nodi (oggetti Rifugio) al grafo
        # Recuperao gli oggetti Rifugio dalla mappa e vedo se esistono
        nodi_da_aggiungere = [self._id_map.get(id_rifugio)
                              for id_rifugio in nodi_coinvolti_id
                              if self._id_map.get(id_rifugio) is not None]

        self.G.add_nodes_from(nodi_da_aggiungere)

        # 5. Aggiungo gli archi tra gli oggetti Rifugio
        archi_da_aggiungere = []
        for c in connessioni_filtrate:
            rifugio1 = self._id_map.get(c.id_rifugio1)
            rifugio2 = self._id_map.get(c.id_rifugio2)

            # Aggiungo l'arco solo se entrambi i rifugi sono nel grafo
            if rifugio1 and rifugio2 and rifugio1 in self.G.nodes and rifugio2 in self.G.nodes:
                archi_da_aggiungere.append((rifugio1, rifugio2))

        self.G.add_edges_from(archi_da_aggiungere)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return list(self.G.nodes)

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        if node in self.G:
            # degree() restituisce il grado di un nodo
            return self.G.degree(node)
        return 0

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)

    def get_reachable_bfs_tree(self, start: Rifugio) -> list:
        """
        Tecnica 1: Utilizza i metodi NetworkX (bfs_tree) per trovare i nodi raggiungibili.
        :param start: nodo di partenza.
        :return: lista dei rifugi raggiungibili, escluso il nodo di partenza.
        """
        # Creiamo un albero di copertura (spanning tree) usando BFS.
        # L'albero contiene tutti i nodi raggiungibili, incluso 'start'.
        tree = nx.bfs_tree(self.G, start)
        reachable_nodes = list(tree.nodes)

        # Rimuoviamo il nodo di partenza dalla lista
        if start in reachable_nodes:
            reachable_nodes.remove(start)

        return reachable_nodes

    def get_reachable_iterative(self, start: Rifugio) -> list:
        """
        Tecnica 2: Algoritmo iterativo.
        :param start: nodo di partenza.
        :return: lista dei rifugi raggiungibili, escluso il nodo di partenza.
        """

        # La lista dei nodi da visitare
        da_visitare = [start]
        # L'insieme dei nodi già visitati/raggiungibili
        visitati: set[Rifugio] = {start}

        while da_visitare:
            # Estrai il primo elemento della lista
            u = da_visitare.pop(0)

            # Scorri tutti i vicini
            for v in self.G.neighbors(u):
                if v not in visitati:
                    visitati.add(v)
                    da_visitare.append(v)

        # visitati contiene tutti i nodi nella componente connessa, incluso 'start'.
        reachable_nodes = list(visitati)

        # Rimuoviamo il nodo di partenza
        if start in reachable_nodes:
            reachable_nodes.remove(start)

        return reachable_nodes

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
        # 1. Tecnica NetworkX
        risultato_nx = self.get_reachable_bfs_tree(start)

        # 2. Tecnica Algoritmo Iterativo
        risultato_iterativo = self.get_reachable_iterative(start)

        # Restituiamo il risultato di una delle due tecniche
        return risultato_nx
