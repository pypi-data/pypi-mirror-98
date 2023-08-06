import numpy as np
import networkx as nx

from pge.init.classes.graph import SGraph


class CustomCreator:
    @staticmethod
    def partitioned_grow(types, prt):
        graph = nx.Graph()
        count = 0
        for tp in types:
            nw_graph = tp[0](*tp[1])
            nw_graph.set_attrs("prt", count)
            graph = nx.union(graph, nw_graph.get_nx_graph(), rename=(None, tp[2]))
            count += 1

        graph = SGraph(graph)
        nodes = graph.get_ids(stable=True)
        dg = [int(prt * graph.count_out_degree(node)) + 1 for node in nodes]
        dg = np.array([np.random.choice(i, 1, p=(np.arange(i) + 1)[::-1] / (np.sum(np.arange(i) + 1)))[0] for i in dg])
        if np.sum(dg) % 2 != 0:
            dg[0] += 1
        prts = graph.get_attributes("prt")

        for i in np.arange(nodes.size):
            if dg[i] == 0:
                continue

            indx = np.arange(nodes.size)[(prts != prts[i]) & (dg > 0)]
            if indx.size == 0:
                continue
            adds = np.random.choice(indx, dg[i])

            for add in adds:
                if dg[add] > 0:
                    graph.add_edge(nodes[i], nodes[add])
                    dg[add] -= 1
            dg[i] = 0
        return graph

    @staticmethod
    def partitioned_di_grow(types, prt, path, rep=1):
        graph_ = nx.DiGraph()
        count = 0
        for tp in types:
            nw_graph = tp[0](*tp[1])
            nx.write_graphml(nw_graph.get_nx_graph(), path + str(tp[2]) + ".graphml")
            print(tp[2])
            nw_graph.set_attrs("prt", count)
            graph_ = nx.union(graph_, nw_graph.get_nx_graph(), rename=(None, tp[2] + "-"))
            count += 1

        try:
            prt = [prt_ for prt_ in prt]
        except:
            prt = [prt]

        for prt_ in prt:
            for _ in np.arange(rep):
                graph = SGraph(graph_)
                nodes = graph.get_ids(stable=True)
                dg_out = [int(prt_ * graph.count_out_degree(node)) + 1 for node in nodes]
                dg_out = np.array(
                    [np.random.choice(i, 1, p=(np.arange(i) + 1)[::-1] / (np.sum(np.arange(i) + 1)))[0] for i in
                     dg_out])
                dg_in = [int(prt_ * graph.count_in_degree(node)) + 1 for node in nodes]
                dg_in = np.array(
                    [np.random.choice(i, 1, p=(np.arange(i) + 1)[::-1] / (np.sum(np.arange(i) + 1)))[0] for i in dg_in])
                print(prt_, np.sum(dg_in), np.sum(dg_out))

                prts = graph.get_attributes("prt")
                id_ns = np.arange(nodes.size)
                np.random.shuffle(id_ns)
                for i in id_ns:
                    if dg_in[i] != 0:
                        indx = np.arange(nodes.size)[(prts != prts[i]) & (dg_out > 0)]
                        if indx.size == 0:
                            continue

                        adds = np.random.choice(indx, dg_in[i])

                        for add in adds:
                            if dg_out[add] > 0:
                                graph.add_edge(nodes[i], nodes[add])
                                dg_out[add] -= 1
                        dg_in[i] = 0

                nx.write_graphml(graph.get_nx_graph(), path + "custom_" + str(prt_) + "_" + str(_) + ".graphml")
