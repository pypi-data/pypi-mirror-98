import networkx as nx
import numpy as np
import pandas as pd

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.mse import boot_estimate
from pge.init.creator import powerlaw
from pge.model.growth.pa import PADiGrowth
from pge.model.growth.pa_com_leader import PAСomDiGrowth
from pge.ranks.rank import estimate_rank


class PAFixComDiGrowth(PAСomDiGrowth):
    def __init__(self, graph, schema, deg, model_param):
        super().__init__(graph, schema, deg, model_param)
        self.chosen = None
        self.frm = "prt"
        self.coms = []

    def prep(self, graph):
        estimate_rank(graph, "one", pers=None)

        self.cur_alps = []
        sets = list(set(graph.get_attributes(self.frm)))
        for com in sets:
            ones = graph.get_attributes("one", graph.get_nodes_with(self.frm, com))
            self.cur_alps.append(
                boot_estimate(
                    HillEstimator,
                    ones,
                    1 / 2,
                    2 / 3,
                    30,
                    speed=False,
                )[0]
            )
            if self.cur_alps[-1] is None:
                self.cur_alps[-1] = np.infty
            else:
                self.cur_alps[-1] = 1 / self.cur_alps[-1]
        self.alps.append(self.cur_alps[np.argmin(self.cur_alps)])
        self.chosen = sets[np.argmin(self.cur_alps)]
        self.coms.append(self.chosen)

        graph.set_attrs(
            "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        graph.set_attrs(
            "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph

    def save(self, gr, to):
        nx.write_graphml(gr, to + ".graphml")
        prd = pd.DataFrame({"alp": self.alps, "com": self.coms})
        prd.to_csv(to + ".csv")

    def new_load(self, gr):
        for node in gr.get_ids():
            gr.set_attr(node, self.frm, self.gr.get_attr(node, "prt"))
        return gr

    def new_node_add(self, graph, to, tp, attrs):
        super().new_node_add(graph, to, tp, attrs)
        graph.set_attr(to, self.frm, -1)

    def stop(self):
        return self.chosen == -1


class PACancerDiGrowth(PADiGrowth):
    def __init__(self, graph, schema, deg, model_param):
        super().__init__(graph, schema, deg, model_param)
        self.frm = "prt"
        self.nws = 0
        self.nws_max = 5000
        self.outs = powerlaw(self.nws_max, 1, ac=0.05)

    def prep(self, graph):
        return graph

    def choice(self, graph, sz, tp="in"):
        if tp == "edge":
            nodes = graph.get_nodes_with("nw", 1)
            if nodes.size == 0:
                return None, None

            probs1 = np.array([graph.count_in_degree(node) for node in nodes]) + self.param[0]
            probs2 = np.array([graph.count_out_degree(node) for node in nodes]) + self.param[1]
            probs1 = probs1 / np.sum(probs1)
            probs2 = probs2 / np.sum(probs2)

            return np.random.choice(nodes, 1, replace=False, p=probs1)[0], \
                   np.random.choice(nodes, 1, replace=False, p=probs2)[0]
        else:
            return super().choice(graph, sz, tp=tp)

    def save(self, gr, to):
        for node in gr.get_ids():
            gr.set_attr(node, "nw-"+self.frm, -1)

        while gr.get_nodes_with("nw-"+self.frm, -1).size != 0:
            for node in gr.get_ids():
                if gr.get_attr(node, "nw-"+self.frm) == -1:
                    if gr.get_attr(node, "nw") == 1:
                        nbrs = np.append(gr.get_in_degrees(node), gr.get_out_degrees(node))
                        nodes = np.unique(gr.get_attributes(self.frm, nbrs))
                        if np.sum(np.isin([0], nodes)) == 1:
                            gr.set_attr(node, "nw-" + self.frm, 0)
                        elif np.sum(np.isin([1], nodes)) == 1:
                            gr.set_attr(node, "nw-" + self.frm, 1)
                        else:
                            gr.set_attr(node, "nw-" + self.frm, 2)
                    else:
                        gr.set_attr(node, "nw-" + self.frm, gr.get_attr(node, self.frm))

        estimate_rank(gr, "one", pers=None)
        nx.write_graphml(gr.get_nx_graph(), to + ".graphml")

    def new_load(self, gr):
        for node in gr.get_ids():
            gr.set_attr(node, self.frm, self.gr.get_attr(node, "prt"))
            gr.set_attr(node, "nw", 0)
        return gr

    def new_node_add(self, graph, to, tp, attrs):
        super().new_node_add(graph, to, tp, attrs)
        graph.set_attr(to, self.frm, -1)
        graph.set_attr(to, "nw", 1)

        for node in np.random.choice(graph.get_ids(stable=True), min(graph.size(), int(self.outs[self.nws])), replace=False):
            graph.add_edge(to, node)
            graph.set_edge_data(to, node, attrs[0], attrs[1] + 1)
        self.nws += 1

    def stop(self):
        return self.nws == self.nws_max

    def new_edge_add(self, gr, attrs):
        trg = gr.get_nodes_with("nw", 1)
        if trg.size == 0:
            return

        node1, node2 = self.choice(gr, None, tp="edge")
        if node1 is None:
            return
        gr.add_edge(node1, node2)
        gr.set_edge_data(node1, node2, attrs[0], attrs[1] + 1)
