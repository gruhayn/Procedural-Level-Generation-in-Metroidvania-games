import random
import json

import networkx as nx
import pygraphviz as pgv


NONE_SKILL = 0
STARTING_SKILL_VALUE = 1
STARTING_NODE_VALUE = 1


def shuffled_array(arr):
    # Create a copy of the original array
    arr_copy = arr[:]
    # Shuffle the copy
    random.shuffle(arr_copy)
    return arr_copy


class Node(object):

    def __init__(self, index):
        self.index = index
        self.existing_skills = []
        self.gained_skills = []

    def add_gained_skill(self, skill):
        if skill is None:
            return

        self.gained_skills.append(skill)
        self.gained_skills = list(set(self.gained_skills))

    def add_skill(self, skill):
        self.existing_skills.append(skill)

    def get_random_skill(self):
        if len(self.existing_skills) == 0:
            return NONE_SKILL
        return random.choice(self.existing_skills)

    def get_random_gained_and_existing_skill(self):
        if len(self.gained_skills+self.existing_skills) == 0:
            return NONE_SKILL
        return random.choice(self.gained_skills+self.existing_skills)

    def get_name(self):
        return "N" + str(self.index)

    def get_skills_joined(self):
        skill_str = "\n"

        for skill in self.existing_skills:
            skill_str = skill_str + str(skill) + " "

        return skill_str


class Road(object):

    def __init__(self, skill):
        self.skill_to_pass_road = skill


class Graph(object):

    def __init__(self, node_count, skill_count):
        self.connections = {}
        self.skills = []
        self.start_node = None
        self.end_node = None

        nodes = []
        for node_index in range(STARTING_NODE_VALUE, node_count + STARTING_NODE_VALUE):
            node = Node(node_index)
            nodes.append(node)

        self.start_node = nodes[0]
        self.end_node = nodes[-1]

        self.intermediate_nodes = [node for node in nodes if
                                   id(node) != id(self.start_node) and id(node) != id(self.end_node)]

        intermediate_nodes_length = len(self.intermediate_nodes)
        index = 0
        for skill_index in range(STARTING_SKILL_VALUE, skill_count + STARTING_SKILL_VALUE):
            self.intermediate_nodes[index % intermediate_nodes_length].add_skill(skill_index)
            self.skills.append(skill_index)
            index = index + 1

        print("Graph created. node count " + str(node_count) + " skill count " + str(skill_count))
        self.print_graph_nodes()

    def print_graph_nodes(self):
        print("Start Node")
        print(self.start_node.get_name() + " " + str(self.start_node.existing_skills) + " gained skills " + str(self.start_node.gained_skills))

        print("Intermediate nodes")
        for node in self.intermediate_nodes:
            print(node.get_name() + " " + str(node.existing_skills) + " gained skills " + str(self.start_node.gained_skills))

        print("End Node")
        print(self.end_node.get_name() + " " + str(self.end_node.existing_skills) + " gained skills " + str(self.start_node.gained_skills))

    def add_connection(self, from_node: Node, to_node: Node, road: Road):
        if from_node.get_name() == to_node.get_name():
            return

        skill_required = road.skill_to_pass_road
        if self.connections.get(from_node.get_name()) is None:
            self.connections[from_node.get_name()] = {}
            self.connections[from_node.get_name()][to_node.get_name()] = [skill_required]
        else:
            prev = self.connections[from_node.get_name()].get(to_node.get_name())
            if prev is None:
                prev = [skill_required]
            else:
                prev.append(skill_required)

            prev = list(set(prev))

            self.connections[from_node.get_name()][to_node.get_name()] = prev

    def print_connections(self):
        print(json.dumps(self.connections, sort_keys=False, indent=4))

    def get_node_by_name(self, name):
        all_nodes = [self.start_node] + self.intermediate_nodes + [self.end_node]
        for node in all_nodes:
            if node.get_name() == name:
                return node

    def set_gained_skills_of_nodes(self, winning_path):
        for node_index in range(2, len(winning_path), 2):
            node = winning_path[node_index]
            for road_index in range(1, node_index, 2):
                road = winning_path[road_index]
                node.add_gained_skill(road.skill_to_pass_road)


def generate_winning_path(graph):
    path = [graph.start_node] + [Road(NONE_SKILL)]

    for node in shuffled_array(graph.intermediate_nodes):
        path = path + [node] + [Road(node.get_random_skill())]

    path = path + [graph.end_node]

    print()
    print("Created path")
    for el in path:
        if isinstance(el, Node):
            print(el.get_name(), end=" ")

        if isinstance(el, Road):
            print(el.skill_to_pass_road, end=" ")

    print()

    return path

def add_winning_paths_to_graph(graph, winning_paths):
    for path in winning_paths:
        for node_index in range(0, len(path) - 2, 2):
            from_node: Node = path[node_index]
            to_node: Node = path[node_index + 2]
            road: Road = path[node_index + 1]
            graph.add_connection(from_node, to_node, road)

    return graph

def add_connections_with_gained_skills(graph, winning_paths, sliding_count, neighbor_distance):
    for all_index in range(len(winning_paths) - 1):
        for index in range(2, len(winning_paths[all_index]) - 1, 2):
            from_node = winning_paths[all_index][index]
            to_path_index = (all_index + neighbor_distance) % len(winning_paths)
            to_node_index = (index + 2 * sliding_count)  # 2* sliding because there is road between nodes

            if (to_node_index > len(winning_paths[to_path_index]) - 1):
                to_node_index = to_node_index % len(winning_paths[to_path_index])
                if to_node_index % 2 == 1:
                    to_node_index = to_node_index - 1

            to_node = winning_paths[to_path_index][to_node_index]
            road = Road(from_node.get_random_gained_and_existing_skill())
            print(str(all_index) + " " + str(index) + " " + from_node.get_name())
            print(str(to_path_index) + " " + str(to_node_index) + " " + to_node.get_name() + " " + str(
                road.skill_to_pass_road))
            graph.add_connection(from_node, to_node, road)

    return graph

def add_sliding_paths_to_graph(graph, winning_paths, sliding_count, neighbor_distance):
    for all_index in range(len(winning_paths) - 1):
        for index in range(2, len(winning_paths[all_index]) - 1, 2):
            from_node = winning_paths[all_index][index]
            to_path_index = (all_index + neighbor_distance) % len(winning_paths)
            to_node_index = (index + 2*sliding_count) # 2* sliding because there is road between nodes

            if(to_node_index > len(winning_paths[to_path_index])-1 ):
                to_node_index = to_node_index % len(winning_paths[to_path_index])
                if to_node_index % 2 == 1:
                    to_node_index = to_node_index - 1

            to_node = winning_paths[to_path_index][to_node_index]
            road = Road(from_node.get_random_skill())
            print(str(all_index) + " " + str(index) + " " + from_node.get_name() )
            print(str(to_path_index) + " " + str(to_node_index) + " " + to_node.get_name() + " " +str(road.skill_to_pass_road))
            graph.add_connection(from_node, to_node, road)

    return graph



def generate_map(seed, minimum_winning_path_count, room_count, skill_count, sliding_count=1, neighbor_distance=5):
    random.seed(seed)
    graph = Graph(room_count, skill_count)

    winning_paths = []

    for i in range(minimum_winning_path_count):
        winning_path = generate_winning_path(graph)
        graph.set_gained_skills_of_nodes(winning_path)
        winning_paths.append(winning_path)

    graph = add_winning_paths_to_graph(graph, winning_paths)

    vizualize_graph(graph, "mid")

    #graph = add_sliding_paths_to_graph(graph, winning_paths, sliding_count, neighbor_distance)

    graph.print_connections()
    print("##########################################################")
    graph.print_graph_nodes()
    graph = add_connections_with_gained_skills(graph, winning_paths, sliding_count, neighbor_distance)



    graph.print_connections()
    return graph

def vizualize_graph(graph, output_filename):
    data = graph.connections


    # Create a directed multigraph
    G = nx.MultiDiGraph()

    # Iterate through the dictionary to add edges
    for parent, children in data.items():
        for child, edges in children.items():
            for edge in edges:
                parent_node = graph.get_node_by_name(parent)
                child_node = graph.get_node_by_name(child)

                parent_name = parent + parent_node.get_skills_joined()
                child_name = child + child_node.get_skills_joined()

                G.add_edge(parent_name, child_name, weight=edge)

    # Convert to a Graphviz graph
    A = nx.nx_agraph.to_agraph(G)

    # Set graph attributes
    A.graph_attr['label'] = "Map Visualization"
    A.node_attr['style'] = 'rounded'
    A.node_attr['fillcolor'] = 'lightblue'

    # Set edge labels
    for edge in A.edges():
        edge_weight = edge.attr['weight']
        edge.attr['label'] = f"{edge_weight}"

    # Render the graph
    output_file = output_filename + ".png"
    A.draw(output_file, prog='dot', format='png')

seed_in = 110
minimum_winning_path_count_in = 3
room_count_in = 6
skill_count_in = 3

graph = generate_map(seed_in, minimum_winning_path_count_in, room_count_in, skill_count_in)

vizualize_graph(graph, "end")
