import random
import json

import networkx as nx

from default_values import STARTING_NODE_VALUE, STARTING_SKILL_VALUE, NONE_SKILL
from find_all_paths import find_all_paths
from print_winning_pathss_as_image_example import create_winning_path_image


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

    def get_random_gained_and_existing_skill(self, exclude_list):
        all_except_exclude_list = list(set(self.gained_skills + self.existing_skills) - set(exclude_list))
        if len(all_except_exclude_list) == 0:
            return NONE_SKILL
        return random.choice(all_except_exclude_list)

    def get_name(self):
        return "N" + str(self.index)

    def get_skills_joined(self):
        skill_str = "\n"

        for skill in self.existing_skills:
            skill_str = skill_str + str(skill) + " "

        return skill_str

    def get_gained_skills_joined(self, exclude_list = [NONE_SKILL]):
        skill_str = "\n"

        for skill in self.gained_skills:
            if skill not in exclude_list:
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

    def get_all_nodes(self):
        return [self.start_node] + self.intermediate_nodes + [self.end_node]

    def get_road_count(self):
        count = 0
        for from_node_name in self.connections.keys():
            for to_node_name in self.connections[from_node_name].keys():
                count = count + len(self.connections[from_node_name][to_node_name])
        return count

    def get_node_count(self):
        return len(self.intermediate_nodes) + 2 # 2 = one for start and one for end node

    def add_dummy_node(self, node):
        Node(self.get_node_count()+1, "D")

    def print_nodes_and_skills_that_can_be_obtain_in_them(self):
        print("Nodes and skills can be obtained in them")
        print(json.dumps(self.get_nodes_and_skills_that_can_be_obtain_in_them(), sort_keys=False, indent=4))

    def get_nodes_and_skills_that_can_be_obtain_in_them(self):
        dict = {}
        for int_node in self.intermediate_nodes:
            dict[int_node.get_name()] = int_node.existing_skills
        return dict

    def get_all_roads_that_come_to_node(self, to_node, backward_step_count):
        result = []
        check_node_names = [to_node.get_name()]
        node_names_comes_to_node = []
        while backward_step_count > 0:

            while len(check_node_names) > 0:
                check_node_name = check_node_names.pop()
                for from_node_name in self.connections.keys():
                    if self.connections[from_node_name].get(check_node_name) is not None:
                        result = result + self.connections[from_node_name].get(check_node_name)
                        node_names_comes_to_node.append(from_node_name)

            check_node_names = node_names_comes_to_node
            node_names_comes_to_node = []
            backward_step_count = backward_step_count - 1

        return result

    def print_graph_nodes(self):
        print("Graph nodes")
        print("Start Node")
        print(self.start_node.get_name() + " " + str(self.start_node.existing_skills) + " gained skills " + str(
            self.start_node.gained_skills))

        print("Intermediate nodes")
        for node in self.intermediate_nodes:
            print(node.get_name() + " " + str(node.existing_skills) + " gained skills " + str(node.gained_skills))

        print("End Node")
        print(self.end_node.get_name() + " " + str(self.end_node.existing_skills) + " gained skills " + str(
            self.end_node.gained_skills))

    def add_connection(self, from_node: Node, to_node: Node, road: Road):
        if from_node.get_name() == to_node.get_name():
            return

        skill_to_pass_road = road.skill_to_pass_road
        to_node_name = to_node.get_name()

        if self.connections.get(from_node.get_name()) is None:
            self.connections[from_node.get_name()] = {}
            self.connections[from_node.get_name()][to_node_name] = [skill_to_pass_road]
        else:
            prev = self.connections[from_node.get_name()].get(to_node_name)
            if prev is None:
                prev = [skill_to_pass_road]
            else:
                prev.append(skill_to_pass_road)

            prev = list(set(prev))

            self.connections[from_node.get_name()][to_node.get_name()] = prev

            print("Created road: " + from_node.get_name() + " " + str(skill_to_pass_road) + " " + to_node.get_name())
    def print_connections(self):
        print("Graph connections")
        print(json.dumps(self.connections, sort_keys=False, indent=4))

    def get_node_by_name(self, name):
        all_nodes = [self.start_node] + self.intermediate_nodes + [self.end_node]
        for node in all_nodes:
            if node.get_name() == name:
                return node

    def add_gained_skills_of_nodes(self, winning_path):
        for node_index in range(2, len(winning_path), 2):
            node = winning_path[node_index]
            for road_index in range(1, node_index, 2):
                road = winning_path[road_index]
                node.add_gained_skill(road.skill_to_pass_road)


def generate_graph_str(graph: Graph, include_gained_skills=False):
    arr = []
    all_nodes = graph.get_all_nodes()

    for node in all_nodes:
        node_str = node.get_name()
        node_str = node_str + node.get_skills_joined()
        if include_gained_skills:
            node_str = node_str + node.get_gained_skills_joined()
        arr.append(node_str)

    return arr

def winning_path_to_str_array(winning_path):
    arr = []

    for i in winning_path:
        if isinstance(i, Road):
            arr.append(str(i.skill_to_pass_road))
        elif isinstance(i, Node):
            arr.append(str(i.get_name()))

    return arr

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
    print("Adding winning paths")

    for path in winning_paths:
        for node_index in range(0, len(path) - 2, 2):
            from_node: Node = path[node_index]
            to_node: Node = path[node_index + 2]
            road: Road = path[node_index + 1]
            graph.add_connection(from_node, to_node, road)

    print("End of adding winning paths")

    return graph


def add_connections_with_gained_skills(graph, winning_paths, sliding_count, neighbor_distance, backward_step_count):
    print("Adding connections with gained skills")
    for all_index in range(len(winning_paths)):
        for index in range(0, len(winning_paths[all_index]) - 1, 2):
            can_add_connection = True

            from_node = winning_paths[all_index][index]
            to_path_index = (all_index + neighbor_distance) % len(winning_paths)
            to_node_index = (index + 2 * sliding_count)  # 2* sliding because there is road between nodes

            if (to_node_index > len(winning_paths[to_path_index]) - 1):
                to_node_index = to_node_index % len(winning_paths[to_path_index])
                if to_node_index % 2 == 1:  # if it is road
                    to_node_index = to_node_index - 1

            to_node = winning_paths[to_path_index][to_node_index]

            exclude_roads = graph.get_all_roads_that_come_to_node(to_node, backward_step_count)
            exclude_roads = exclude_roads + [NONE_SKILL]
            road = Road(from_node.get_random_gained_and_existing_skill(exclude_roads))

            if road.skill_to_pass_road == NONE_SKILL:
                can_add_connection = False

            if can_add_connection and to_node.get_name() == graph.end_node.get_name():
                required_skills = []
                for from_node_name in graph.connections.keys():
                    if graph.connections[from_node_name].get(to_node.get_name()) is not None:
                        required_skills = required_skills + graph.connections[from_node_name].get(to_node.get_name())

                for skill in required_skills:
                    if road.skill_to_pass_road < skill:
                        can_add_connection = False

            if not can_add_connection:
                continue

            graph.add_connection(from_node, to_node, road)


    print("End of adding connections with gained skills")

    return graph


# def add_sliding_paths_to_graph(graph, winning_paths, sliding_count, neighbor_distance):
#     for all_index in range(len(winning_paths) - 1):
#         for index in range(2, len(winning_paths[all_index]) - 1, 2):
#             from_node = winning_paths[all_index][index]
#             to_path_index = (all_index + neighbor_distance) % len(winning_paths)
#             to_node_index = (index + 2 * sliding_count)  # 2* sliding because there is road between nodes
#
#             if (to_node_index > len(winning_paths[to_path_index]) - 1):
#                 to_node_index = to_node_index % len(winning_paths[to_path_index])
#                 if to_node_index % 2 == 1:
#                     to_node_index = to_node_index - 1
#
#             to_node = winning_paths[to_path_index][to_node_index]
#             road = Road(from_node.get_random_skill())
#             print(str(all_index) + " " + str(index) + " " + from_node.get_name())
#             print(str(to_path_index) + " " + str(to_node_index) + " " + to_node.get_name() + " " + str(
#                 road.skill_to_pass_road))
#             graph.add_connection(from_node, to_node, road)
#
#     return graph

def adjust_graph_based_on_required_skill_to_win(graph, required_skills_to_win):
    print("Adjusting graph based on required skills to win")

    if required_skills_to_win is None or len(required_skills_to_win) == 0:
        print("No roads changed based on required_skills_to_win")
        return graph

    print("Checking required_skills_to_win")
    new_required_skills_to_win = []
    for required_skill_to_win in required_skills_to_win:
        if required_skill_to_win in graph.skills:
            new_required_skills_to_win.append(required_skill_to_win)
        else:
            print(str(required_skill_to_win) + " skill omitted. Because not in list. List: " + str(graph.skills))

    required_skills_to_win = new_required_skills_to_win

    print("Changed roads based on required skills to win. required_skills: " + str(required_skills_to_win))

    end_node_name = graph.end_node.get_name()
    for from_node_name in graph.connections.keys():
        if graph.connections[from_node_name].get(end_node_name) is not None:
            #
            required_skills_to_end = graph.connections[from_node_name][end_node_name]

            # new_required_skills_to_end = []
            # for required_skill_to_end in required_skills_to_end:
            #     if required_skill_to_end not in required_skills_to_win:
            #         required_skill_to_win = random.choice(required_skills_to_win)
            #         new_required_skills_to_end.append(required_skill_to_win)
            #         print("from node " + from_node_name + " end node " + end_node_name +
            #               " changed road from " + str(required_skill_to_end) + " to " + str(required_skill_to_win))
            #     else:
            #         new_required_skills_to_end.append(required_skill_to_end)
            print("from node " + from_node_name + " end node " + end_node_name +
                  " changed road from " + str(required_skills_to_end) + " to " + str(required_skills_to_win))
            graph.connections[from_node_name][end_node_name] = [required_skills_to_win+[NONE_SKILL]]

    print("End of adjusting graph based on required skills to win")

    return graph

def print_dict_human_readable(d):
    human_readable_dict = ""
    for key, value in d.items():
        if value is None:
            human_readable_dict = human_readable_dict  + "\n" + f"{key}: not set"
        elif isinstance(value, list):
            human_readable_dict = human_readable_dict + "\n"+ f"{key}: {', '.join(map(str, value))}"
        else:
            human_readable_dict = human_readable_dict + "\n"+ f"{key}: {value}"
    return human_readable_dict

def vizualize_graph(graph, output_filename, input_params, add_postfix = True, add_comprehensive_deatils = False):
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
    if add_comprehensive_deatils:
        A.graph_attr['label'] = "Map Visualization\n"+"Node Count: " + str(graph.get_node_count()) \
                            + "\nSkills: " + str(graph.skills) \
                            + "\nRoad Count: " + str(graph.get_road_count()) \
                            + "\nWinning Path Count: " + str(len(find_all_paths(graph))) \
                            + "\nInput parameters: " + print_dict_human_readable(input_params)
    else:
        A.graph_attr['label'] = "Map Visualization"

    A.graph_attr['rankdir'] = 'LR' #added for horizontal image
    A.node_attr['style'] = 'rounded'
    A.node_attr['fillcolor'] = 'lightblue'
    A.graph_attr['size'] = "10,10!"
    A.graph_attr['nodesep'] = 0.5  # Increase the space between nodes
    A.graph_attr['ranksep'] = 1  # Increase the space between ranks

    # Set edge labels
    for edge in A.edges():
        edge_weight = edge.attr['weight']
        if edge_weight != NONE_SKILL:
            edge.attr['label'] = f"{edge_weight}"
        else:
            del edge.attr['label']

    postfix = ""
    if add_postfix:
        for key, value in input_params.items():
            if value is None:
                postfix = postfix  + "_"
            elif isinstance(value, list):
                postfix = postfix + "_"+ f"{', '.join(map(str, value))}"
            else:
                postfix = postfix + "_"+ f"{value}"


        # Render the graph
    output_file = output_filename + postfix + ".png"
    A.draw(output_file, prog='dot', format='png')
    print(output_file + " file created")


def generate_map(seed, minimum_winning_path_count, room_count, skill_count, sliding_count, neighbor_distance,
                 backward_step_count, required_skill_to_win, input_params):
    random.seed(seed)
    graph = Graph(room_count, skill_count)
    graph_str = generate_graph_str(graph)
    create_winning_path_image(-2, graph_str)
    winning_paths = []

    for i in range(minimum_winning_path_count):
        winning_path = generate_winning_path(graph)
        winning_path_str = winning_path_to_str_array(winning_path)
        create_winning_path_image(i, winning_path_str)
        graph.add_gained_skills_of_nodes(winning_path)
        winning_paths.append(winning_path)

    graph_str = generate_graph_str(graph, True)
    create_winning_path_image(-1, graph_str)

    graph = add_winning_paths_to_graph(graph, winning_paths)

    # graph = add_sliding_paths_to_graph(graph, winning_paths, sliding_count, neighbor_distance)
    print("##########################################################")

    graph.print_connections()
    graph.print_graph_nodes()
    vizualize_graph(graph, "1. winning_paths", input_params)

    print("##########################################################")

    graph = add_connections_with_gained_skills(graph, winning_paths, sliding_count, neighbor_distance,
                                               backward_step_count)

    print("##########################################################")

    graph.print_connections()
    graph.print_graph_nodes()
    vizualize_graph(graph, "2. gained skills", input_params)

    print("##########################################################")

    graph = adjust_graph_based_on_required_skill_to_win(graph, required_skill_to_win)

    print("##########################################################")

    graph.print_connections()
    graph.print_graph_nodes()
    vizualize_graph(graph, "3. required_skills_to_win", input_params)

    print("##########################################################")

    return graph


