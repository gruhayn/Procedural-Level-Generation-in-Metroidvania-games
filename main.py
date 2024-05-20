from mapGen import *

seed_in = 1
minimum_winning_path_count_in = 2
room_count_in = 10
skill_count_in = 4
sliding_count_in = 2
neighbor_distance_in = 3
backward_step_count_in = 2
required_skills_to_win_in = [0,1,2,3,4] #[skill_count_in, skill_count_in-1]

graph = generate_map(
    seed_in,
    minimum_winning_path_count_in,
    room_count_in,
    skill_count_in,
    sliding_count_in,
    neighbor_distance_in,
    backward_step_count_in,
    required_skills_to_win_in)

vizualize_graph(graph, "4. end")
graph.print_graph_nodes()
graph.print_connections()
graph.print_nodes_and_skills_that_can_be_obtain_in_them()

all_paths = find_all_paths(graph)

for path in all_paths:
    for i in path:
        print(str(i) + " ", end="")
    print()

graph.print_graph_nodes()