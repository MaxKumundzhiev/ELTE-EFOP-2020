# ------------------------------------------
# 
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------

from typing import Dict

import hypernetx as hnx
from hypernetx import algorithms
import networkx as nx
import pandas as pd
from random import randint, choice

import matplotlib.pyplot as plt


def construct_graph_from_dict():
    """Construct a hypergraph dictionary mapping edge id's to vertex sets.

    Notes:
        A pair of entitysets (Nodes,Edges) such that Edges has depth 2, Nodes have depth 1, and the children of Edges is exactly the set of elements of Nodes.
          Intuitively, every element of Edges is a (hyper)edge, which is either empty or contains elements of Nodes.
          Every node in Nodes has membership in some edge in Edges.
          Since a node has depth 0 it is distinguished by its uid, properties, and memberships.
          A hypergraph is instantiated in the class Hypergraph.

    Returns:
        H: pair of entity sets (Nodes,Edges)
    """

    scenes = {
        0: ('FN', 'TH'),
        1: ('TH', 'JV'),
        2: ('BM', 'FN', 'JA'),
        3: ('JV', 'JU', 'CH', 'BM'),
        4: ('JU', 'CH', 'BR', 'CN', 'CC', 'JV', 'BM'),
        5: ('TH', 'GP'),
        6: ('GP', 'MP'),
        7: ('MA', 'GP')
    }
    return hnx.Hypergraph(scenes)


def generate_bipartite_data(rows: int):
    process_type = ['bulk', 'load', 'download', 'remove', 'create']
    activity_type = ['sequence', 'exclusive choice', 'parallel', 'multiple choice', 'multiple merge', 'cycle']

    columns_list = ['process_id', 'process_type', 'process_cost', 'execution_time', 'activity_type']

    result_df = pd.DataFrame(columns=columns_list)

    for number in range(rows):
        buffer = pd.DataFrame({
            'process_id': [number],
            'process_type': choice(process_type),
            'process_cost': [(str(randint(0, 200))) + '$'],
            'execution_time': [str(randint(0., 120.)) + (' sec')],
            'activity_type': choice(activity_type)
        })
        result_df = pd.concat([result_df, buffer], ignore_index=True)
    print(result_df)
    return result_df


def generate_hyper_from_bipartite(dataframe: pd.DataFrame):
    B = nx.Graph()
    B.add_nodes_from(dataframe['process_id'], bipartite=1)
    B.add_nodes_from(dataframe['activity_type'], bipartite=0)

    B.add_weighted_edges_from(
        [(row['process_id'], row['activity_type'], 1) for idx, row in dataframe.iterrows()],
        weight='weight')

    top_nodes = {n for n, d in B.nodes(data=True) if d['bipartite'] == 0}
    bottom_nodes = set(B) - top_nodes
    spectral_bipartivity = nx.bipartite.spectral_bipartivity(B)

    nodes = nx.bipartite.maximum_matching(B, top_nodes=bottom_nodes)

    left_nodes, right_nodes = [], []
    [left_nodes.append(key) for key in nodes.keys() if type(key) == str]
    [right_nodes.append(value) for value in nodes.values() if type(value) == int]
    clustering_coeff = nx.bipartite.clustering(B)
    latapy_clustering = nx.bipartite.clustering(B, mode='dot')
    average_graph_clustering = nx.average_clustering(B)
    # redundancy_coefficients = nx.bipartite.node_redundancy(B)

    rows = []
    for index, left in enumerate(left_nodes):
        rows_dict = ({
            'left_node': left,
            'right_node': right_nodes[index],
            'is_bipartite': nx.is_bipartite(B),
            'spectral_bipartivity': spectral_bipartivity,
            'clustering_coeff': clustering_coeff[index],
            'latapy_clustering': latapy_clustering[index],
            'average_graph_clustering': average_graph_clustering,
            # 'redundancy coefficients': redundancy_coefficients[index]
                    })
        rows.append(rows_dict)

    characteristic_df = pd.DataFrame(rows)
    HBG = hnx.Hypergraph.from_bipartite(B)
    return HBG, characteristic_df


def plot_graph(graph):
    """Plot hypergraph.
    """
    hnx.draw(graph)
    plt.show()
    return


if __name__ == "__main__":
    """Run processes.
    
    Notes:
        HG: hyper graph;
        BG: bipartate graph;
        HBG: hypergraph from bipartate graph;
    """
    # Hypergraph from dict
    HG = construct_graph_from_dict()
    #plot_graph(HG)

    # Hypergraph from predefiend bipartate graph
    data_df = generate_bipartite_data(20)
    HBG, df_characteristics = generate_hyper_from_bipartite(data_df)
    print(df_characteristics)
    #plot_graph(HBG)

    # Dual Hypergraph, Nodes and edges switched.
    HD = HBG.dual()
    #plot_graph(HD)

    print(algorithms.homology_mod2.hypergraph_homology_basis(HBG, k=2, shortest=True))

