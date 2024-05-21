from mapGen import *

seed_in = 768234
minimum_winning_path_count_in = 3
room_count_in = 5
skill_count_in = 3
sliding_count_in = 1
neighbor_distance_in = 1
backward_step_count_in = 1
required_skills_to_win_in = [1,2, 3] #[skill_count_in, skill_count_in-1]


input_params = {
    "Seed": seed_in,
    "Minimum Winning Path Count" : minimum_winning_path_count_in,
    "Room Count" : room_count_in,
    "Skill Count": skill_count_in,
    "Sliding Count": sliding_count_in,
    "Neighbor Distance": neighbor_distance_in,
    "Backward Step Count": backward_step_count_in,
    "Required Skills to Win": required_skills_to_win_in
}



graph = generate_map(
    seed_in,
    minimum_winning_path_count_in,
    room_count_in,
    skill_count_in,
    sliding_count_in,
    neighbor_distance_in,
    backward_step_count_in,
    required_skills_to_win_in, input_params)


vizualize_graph(graph, "4. end", input_params)
graph.print_graph_nodes()
graph.print_connections()
graph.print_nodes_and_skills_that_can_be_obtain_in_them()

all_paths = find_all_paths(graph)

for path in all_paths:
    for i in path:
        print(str(i) + " ", end="")
    print()

graph.print_graph_nodes()