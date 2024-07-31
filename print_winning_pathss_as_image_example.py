import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

# # Define the winning paths
# winning_paths = [
#     ["N1", "0", "N2", "1", "N3", "[1, 2, 0]", "N5"]
# ]
#
# def create_graph(path):
#     G = nx.MultiDiGraph()
#     for i in range(len(path) - 1):
#         if isinstance(path[i + 1], list):
#             G.add_edge(path[i], f"{path[i + 1]}", weight='')
#         else:
#             G.add_edge(path[i], path[i + 1], weight=path[i + 1])
#     return G


def create_graph(path):
    G = nx.DiGraph()
    # Convert all elements to strings to ensure they are hashable
    path = [str(node) for node in path]
    for i in range(len(path) - 1):
        G.add_edge(path[i], path[i + 1], weight=path[i + 1])
    return G

def create_path_image_with_filename(output_file, path):
    G = create_graph(path)
    A = to_agraph(G)
    A.graph_attr['rankdir'] = 'LR'
    A.node_attr['style'] = 'rounded'
    A.node_attr['fillcolor'] = 'lightblue'
    A.graph_attr['size'] = "10,10!"
    A.graph_attr['nodesep'] = 0.5
    A.graph_attr['ranksep'] = 1
    A.draw(output_file, prog='dot', format='png')
    print(output_file + " file created")

def create_winning_path_image(idx, path):
    print("create_winning_path_image start")
    print(path)
    output_file = f"winning_path_{idx + 1}.png"
    create_path_image_with_filename(output_file, path)

# for idx, path in enumerate(winning_paths):
#     create_winning_path_image(idx, path)

