# ------------------------------------------
# 
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------


import pandas as pd
import networkx as nx
from random import choice, randint


def generate_data(rows: int):
    process_type = ['bulk', 'load', 'download', 'remove', 'create']
    activity_type = ['sequence', 'exclusive choice', 'parallel', 'multiple choice', 'multiple merge', 'cycle']
    columns_list = ['process_id', 'process_type', 'process_cost', 'execution_time', 'user_role']

    result_df = pd.DataFrame(columns=columns_list)

    for number in range(rows):
        buffer = pd.DataFrame({
            'activity_id': [number],
            'process_cost': [randint(100, 500)],
            'execution_time': [randint(0, 200)],
            'process_type': choice(process_type),
            'activity_type': choice(activity_type)
        })
        result_df = pd.concat([result_df, buffer], ignore_index=True)
    print(result_df)
    return result_df


def generate_graph(dataframe: pd.DataFrame):
    B = nx.Graph()
    B.add_nodes_from (dataframe['activity_id'], bipartite=0)
    B.add_nodes_from (dataframe['activity_type'], bipartite=1)
    B.add_weighted_edges_from(
        [(row['process_id'], row['process_type'], 1) for idx, row in dataframe.iterrows()],
        weight='weight')

    print(f'Graph Nodes: {B.nodes(data=True)}')
    print(f'Graph edges: {B.edges(data=True)}')
    return B


def plot_graph(bi_graph, dataframme):
    import matplotlib.pyplot as plt
    pos = {node: [0, i] for i, node in enumerate(dataframme['process_id'])}
    pos.update({node: [1, i] for i, node in enumerate(dataframme['process_type'])})

    nx.draw(bi_graph, pos, with_labels=False)
    for p in pos:  # raise text positions
        pos[p][1] += 0.25
    nx.draw_networkx_labels(bi_graph, pos)
    plt.show()


data = generate_data(50)
graph = generate_graph(data)

plot_graph(graph, data)


