import copy

import networkx as nx

from database.DAO import DAO
from model.model import Model

model = Model()
# grafo = model.creaGrafo("White", 2018)
# v0 = model._idMapProduct[94110]
"""vicini = sorted(grafo[v0], key=lambda x: grafo[v0][x]['weight'])
for v in vicini:
    print(grafo[v0][v]['weight'])"""


class Test:
    def __init__(self):
        self._bestPath = []
        self.grafo = nx.Graph()

    def createGraph(self):
        self.grafo.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

        # Aggiungi archi con pesi
        self.grafo.add_edge('A', 'B', weight=1)
        self.grafo.add_edge('A', 'C', weight=2)
        self.grafo.add_edge('B', 'C', weight=2)
        self.grafo.add_edge('B', 'D', weight=3)
        self.grafo.add_edge('C', 'D', weight=4)
        self.grafo.add_edge('C', 'E', weight=5)
        self.grafo.add_edge('D', 'E', weight=1)

        return self.grafo

    def getBestPath(self, v0):
        self._bestPath = []

        parziale = [v0]
        pesi = []
        archi_visitati = []
        self.ricorsione(parziale, pesi, archi_visitati)
        """vicini = sorted(self._grafo[v0], key=lambda x: self._grafo[v0][x]['weight'])
        for v in vicini:
            parziale.append(v)
            pesi = [self._grafo[v0][v]['weight']]
            self.ricorsione(parziale, pesi)
            parziale.pop()"""

        return self._bestPath

    def ricorsione(self, parziale, pesi, archi_visitati):
        """for i in parziale:
            print(i.Product_number,end=', ')
        print()"""
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        vicini = sorted(self.grafo[parziale[-1]], key=lambda x: self.grafo[parziale[-1]][x]['weight'])

        for v in vicini:
            vic = v
            peso = self.grafo[parziale[-1]][v]['weight']
            arco = (parziale[-1], v)
            if (not pesi or self.grafo[parziale[-1]][v]['weight'] >= max(pesi)) and (parziale[-1], v) not in archi_visitati and (v, parziale[-1]) not in archi_visitati:
                parziale.append(v)
                pesi.append(peso)
                archi_visitati.append((parziale[-2], v))
                self.ricorsione(parziale, pesi, archi_visitati)
                pesi.pop()
                archi_visitati.pop()
                parziale.pop()




if __name__ == '__main__':
    t = Test()
    grafo = t.createGraph()
    path = t.getBestPath('A')
    print(path)
