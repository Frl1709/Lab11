import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        self._listYear, self._listColor = self._model.getParamsDD()

        for a in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(a))

        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))

    def handle_graph(self, e):
        self._model.creaGrafo(self._view._ddcolor.value, self._view._ddyear.value)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene "
                                                  f"{self._model.getNumNodes()} nodi."))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene "
                                                  f"{self._model.getNumEdges()} archi."))

        sort_edge = self._model.getArchiPesanti()
        nodes = {}
        for i in range(3):
            self._view.txtOut.controls.append(ft.Text(
                f"Arco da {sort_edge[i][0].Product_number} a {sort_edge[i][1].Product_number}, peso={sort_edge[i][2]['weight']}"))
            if sort_edge[i][0] not in nodes:
                nodes[sort_edge[i][0]] = 1
            else:
                nodes[sort_edge[i][0]] += 1

            if sort_edge[i][1] not in nodes:
                nodes[sort_edge[i][1]] = 1
            else:
                nodes[sort_edge[i][1]] += 1

        res = []
        for n in nodes:
            if nodes[n] > 1:
                res.append(n.Product_number)

        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {res}"))
        self.fillDDProduct()
        self._view.btn_search.disabled = False
        self._view.update_page()

    def fillDDProduct(self):
        if self._model._product is not None:
            for a in self._model._product:
                self._view._ddnode.options.append(ft.dropdown.Option(a.Product_number))

    def handle_search(self, e):
        v0 = self._model._idMapProduct[int(self._view._ddnode.value)]
        bestPath = self._model.getBestPath(v0)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(bestPath)-1}"))
        self._view.update_page()

