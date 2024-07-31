from mapGen import *
from print_winning_pathss_as_image_example import create_path_image_with_filename

seed_in = 126213768
minimum_winning_path_count_in = 3
room_count_in = 5
skill_count_in = 6
sliding_count_in = 1
neighbor_distance_in = 1
backward_step_count_in = 1
required_skills_to_win_in = [1, 2] #[skill_count_in, skill_count_in-1]


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
print("Winning paths:")
for index in range(len(all_paths)):
    path = all_paths[index]
    path_str = ["{0}".format(str(i)) for i in path]
    print(path)

    print(path_str)
    create_path_image_with_filename("pathfind"+str(index)+".png", path)
    for i in path:
        print(str(i) + " ", end="")
    print()


graph.print_graph_nodes()