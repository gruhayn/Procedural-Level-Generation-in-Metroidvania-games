from pathlib import Path

import Constants
from mapGen import *
from print_winning_pathss_as_image_example import create_path_image_with_filename
import json
import os

seed_in = 126213768
minimum_winning_path_count_in = 1
room_count_in = 10
skill_count_in = 50
sliding_count_in = 1
neighbor_distance_in = 2
backward_step_count_in = 2
required_skills_to_win_in = [i for i in range(5)]


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

#######################SCENARIO CREATION################################################################3
# scenario_index = input("Scenario index:")
#
# file_path = Constants.get_base_folder(scenario_index)
# if not os.path.exists(file_path):
#     os.makedirs(file_path)
#
# with open(Constants.create_file_name(scenario_index, Constants.CONNECTIONS_FILE_NAME), 'w') as file:
#     json.dump(graph.get_connections(), file, indent=4)
#
# with open(Constants.create_file_name(scenario_index, Constants.NODES_FILE_NAME), 'w') as file:
#     json.dump(graph.get_graph_nodes(), file, indent=4)
#
# with open(Constants.create_file_name(scenario_index, Constants.SCENARIO_PARAMS), 'w') as file:
#     json.dump(input_params, file, indent=4)

################################################################3####################################################

#graph.print_graph_nodes()
#graph.print_connections()
vizualize_graph(graph, "4. end", input_params, False)
#graph.print_nodes_and_skills_that_can_be_obtain_in_them()

# all_paths = find_all_paths(graph)
# print("")
# for index in range(len(all_paths)):
#     path = all_paths[index]
#     path_str = ["{0}".format(str(i)) for i in path]
#     print(path)
#
#     print(path_str)
#     create_path_image_with_filename("pathfind"+str(index), path, format="pdf")
#     for i in path:
#         print(str(i) + " ", end="")
#     print()


# graph.print_graph_nodes()