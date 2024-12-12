from default_values import NONE_SKILL
import math
import datetime

def is_entry_exist_in_history(history, from_node_name, to_node_name, gained_skills):
    #print(str(datetime.datetime.now())+" is_entry_exist_in_history")
    if history.get(from_node_name) is None or history[from_node_name].get(to_node_name) is None:
        return False

    history_skills = history[from_node_name].get(to_node_name)

    for gained_skill in gained_skills:
        if gained_skill not in history_skills:
            return False

    return True

def add_to_history(history, from_node_name, to_node_name, gained_skills):
    #print(str(datetime.datetime.now()) + " add_to_history")
    if history.get(from_node_name) is None:
        history[from_node_name] = {}

    history[from_node_name][to_node_name] = gained_skills

    return history

def pop_min_lenght_path(todo):
    #print(str(datetime.datetime.now()) + " pop_min_lenght_path")


    min = math.inf
    min_index = -1

    for i in range(len(todo)):
        (from_node_name, to_node, gained_skills, path, path_length) = todo[i]
        if min > path_length:
            min = path_length
            min_index = i

    (from_node_name, to_node, gained_skills, path, path_length) = todo[min_index]

    del todo[min_index]
    return (from_node_name, to_node, gained_skills, path, path_length, todo)

def check_required_skills(required_skills, gained_skills):
    #print(str(datetime.datetime.now()) + " check_required_skills")

    have_all_required_skills = False
    road = None
    for required_skill in required_skills:
        if type(required_skill) is list:
            required_skill_arr = required_skill
            all_gained_skills_match = True
            for required_skill_arr_el in required_skill_arr:
                if required_skill_arr_el not in gained_skills:
                    all_gained_skills_match = False
                    break

            if all_gained_skills_match:
                have_all_required_skills = True
                road = required_skill

        else:
            if required_skill in gained_skills:
                have_all_required_skills = True
                road = required_skill

        if have_all_required_skills:
            break

    return have_all_required_skills, road


def find_all_paths(graph):
    maxi = 0

    #print(str(datetime.datetime.now()) + " find_all_paths")
    all_paths = []
    start_node = graph.start_node
    end_node_name = graph.end_node.get_name()
    gained_skills = [NONE_SKILL]
    path = []
    paht_length = 0

    todo = [(start_node.get_name(), start_node, gained_skills, path, paht_length)]
    history = {}

    while len(todo) > 0:
        #print("todo "+str(len(todo)))
        maxi = max(maxi, len(todo))
        (from_node_name, current_node, gained_skills, path, path_length , todo) = pop_min_lenght_path(todo)

        current_node_name = current_node.get_name()

        if current_node_name == end_node_name:
            required_skills_to_win = graph.connections[from_node_name][current_node_name]

            can_win, _ = check_required_skills(required_skills_to_win, gained_skills)

            if can_win:
                path.append(current_node_name)
                all_paths.append(path)

            continue

        if is_entry_exist_in_history(history, from_node_name, current_node_name, gained_skills):
            continue

        path.append(current_node_name)

        existing_skills = list(set(current_node.existing_skills+[NONE_SKILL]))
        visited = []
        for existing_skill in existing_skills:
            gained_skills.append(existing_skill)
            gained_skills = list(set(gained_skills))

            neighbors = list(graph.connections[current_node_name].keys())
            for next_node_name in neighbors:
                if next_node_name in visited:
                    continue

                next_node = graph.get_node_by_name(next_node_name)
                required_skills = graph.connections[current_node_name][next_node_name]

                have_all_required_skills, road = check_required_skills(required_skills, gained_skills)

                if have_all_required_skills:
                    new_path = path[:]
                    new_path.append(road)
                    todo.append( (current_node_name, next_node, gained_skills[:], new_path[:], len(new_path) ) )
                    history = add_to_history(history, from_node_name, current_node_name, gained_skills)

                    visited.append(next_node_name)

    #print("maxi ", str(maxi))
    return all_paths