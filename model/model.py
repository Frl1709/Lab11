import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listaAnni = []
        self._listaColori = []
        self._product = None
        self._grafo = nx.Graph()
        self._idMapProduct = {}
        self._bestPath = []

    def getBestPath(self, v0):
        self._bestPath = []

        parziale = [v0]
        pesi = []
        archi_visitati = []
        self.ricorsione(parziale, pesi, archi_visitati)

        return self._bestPath

    def ricorsione(self, parziale, pesi, archi_visitati):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        vicini = sorted(self._grafo[parziale[-1]], key=lambda x: self._grafo[parziale[-1]][x]['weight'])

        for v in vicini:
            peso = self._grafo[parziale[-1]][v]['weight']
            if (not pesi or self._grafo[parziale[-1]][v]['weight'] >= max(pesi)) and (parziale[-1], v) not in archi_visitati and (v, parziale[-1]) not in archi_visitati:
                parziale.append(v)
                pesi.append(peso)
                archi_visitati.append((parziale[-2], v))
                self.ricorsione(parziale, pesi, archi_visitati)
                pesi.pop()
                archi_visitati.pop()
                parziale.pop()

    def getArchiPesanti(self):
        sorted_edges = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return sorted_edges

    def creaGrafo(self, color, anno):
        self._grafo.clear()
        self.addNodes(color)
        self.addEdges(anno, color)

    def addNodes(self, color):
        self._product = DAO.getProduct(color)
        self._grafo.add_nodes_from(self._product)
        for node in self._product:
            self._idMapProduct[node.Product_number] = node

    def addEdges(self, anno, colore):
        connection = DAO.getConnection(anno, colore)
        for c in connection:
            self._grafo.add_edge(self._idMapProduct[c[0]], self._idMapProduct[c[1]], weight=c[2])

    def getParamsDD(self):
        self._listaAnni = DAO.getAllYears()
        self._listaColori = DAO.getAllColor()

        return self._listaAnni, self._listaColori

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
