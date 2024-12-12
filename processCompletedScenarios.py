import os
import json
import pprint
import pandas as pd
import seaborn as sns
from collections import defaultdict
import matplotlib.pyplot as plt

import Constants


def read_result_files(root_folder, scenario_filter):
    results = []

    # Traverse through the root folder
    for person_folder in os.listdir(root_folder):
        person_folder_path = os.path.join(root_folder, person_folder)

        # Ensure we're looking at a folder
        if os.path.isdir(person_folder_path):
            scenarios_folder = os.path.join(person_folder_path, 'scenarios')

            # Check if 'scenarios' folder exists
            if os.path.exists(scenarios_folder):
                for scenario in scenario_filter:
                    scenario_folder = os.path.join(scenarios_folder, str(scenario))

                    # Check if the scenario folder exists
                    if os.path.exists(scenario_folder):
                        # Load SCENARIO_PARAMS.json file to get required skills to win
                        params_file_path = os.path.join(scenario_folder, 'SCENARIO_PARAMS.json')
                        if os.path.exists(params_file_path):
                            with open(params_file_path, 'r') as params_file:
                                scenario_params = json.load(params_file)
                        else:
                            print(f"SCENARIO_PARAMS.json not found for scenario {scenario_folder}")
                            scenario_params = {}

                        # Iterate over the files in the scenario folder
                        for file_name in os.listdir(scenario_folder):
                            # Check if the file contains 'SCENARIO_RESULTS' and ends with '.json'
                            if "SCENARIO_RESULTS" in file_name and file_name.endswith('.json'):
                                file_path = os.path.join(scenario_folder, file_name)
                                try:
                                    # Open and read the JSON file
                                    with open(file_path, 'r') as json_file:
                                        data = json.load(json_file)
                                        # Attach scenario params to each result
                                        data['scenario_params'] = scenario_params
                                        results.append(data)  # Append data to results list
                                except json.JSONDecodeError:
                                    print(f"Error reading JSON from {file_path}")

    return results


def calculate_statistics(data):
    total_runs = len(data)
    total_wins = 0
    total_elapsed_time = 0
    total_valid_actions = 0
    total_invalid_actions = 0
    action_counts = {}
    scenario_movement = {}

    for entry in data:
        # Extract common details
        elapsed_time = entry['elapsedTime']
        is_win = entry['historyOfActions'].get('isWin', False)
        actions = entry['historyOfActions']

        # Update general statistics
        total_elapsed_time += elapsed_time
        if is_win:
            total_wins += 1

        valid_actions = 0
        invalid_actions = 0

        # Analyze each action in historyOfActions
        for action_key, action_data in actions.items():
            if action_key.isdigit():  # Check for numbered actions (1, 2, 3,...)
                action_name = action_data['action']
                action_name.strip()
                is_okay_action = action_data['isOkayAction']

                # Update valid or invalid action counts
                if is_okay_action:
                    valid_actions += 1
                    if 'go' in action_name:
                        # Track movements to different scenarios
                        location = action_name.split(' ')[-1]
                        scenario_movement[location] = scenario_movement.get(location, 0) + 1
                else:
                    invalid_actions += 1

                # Track the type of action
                action_counts[action_name] = action_counts.get(action_name, 0) + 1

        # Update totals for all runs
        total_valid_actions += valid_actions
        total_invalid_actions += invalid_actions

    # Calculate overall statistics
    average_time = total_elapsed_time / total_runs if total_runs > 0 else 0
    win_rate = (total_wins / total_runs) * 100 if total_runs > 0 else 0
    average_valid_actions = total_valid_actions / total_runs if total_runs > 0 else 0
    average_invalid_actions = total_invalid_actions / total_runs if total_runs > 0 else 0

    # Print or return statistics
    statistics = {
        'Total Runs': total_runs,
        'Total Wins': total_wins,
        'Win Rate (%)': win_rate,
        'Total Elapsed Time': total_elapsed_time,
        'Average Elapsed Time': average_time,
        'Total Valid Actions': total_valid_actions,
        'Average Valid Actions': average_valid_actions,
        'Total Invalid Actions': total_invalid_actions,
        'Average Invalid Actions': average_invalid_actions,
        'Action Frequency': action_counts,
        'Scenario Movements': scenario_movement
    }

    return statistics


def collect_paths_and_abilities(data):
    player_runs = {}
    abilities_distribution = defaultdict(int)  # Track how many times each ability was gained
    paths_used = defaultdict(int)  # Track how often each full path was taken
    node_visits = defaultdict(int)  # Track how often each node (location) was visited
    for entry in data:
        player_name = f"{entry['name']} {entry['surname']}"
        actions = entry['historyOfActions']
        scenario_params = entry.get('scenario_params', {})
        required_skills_to_win = scenario_params.get("Required Skills to Win", [])

        path = ['N1']  # Players start at N1 by default
        abilities_gained = {0}  # Start with ability 0 by default

        for action_key, action_data in actions.items():
            if action_key.isdigit():  # Only look at numbered actions
                action_name = action_data['action'].strip()
                is_okay_action = action_data['isOkayAction']

                if is_okay_action:

                    if 'go' in action_name:
                        # Track the movement to the new scenario location
                        location = action_name.split(' ')[-1].strip()  # Extract location (e.g., N4)
                        path.append(location)
                        # Track node visits
                        node_visits[location] += 1

                    elif 'gain' in action_name:
                        # Track the gained abilities
                        parts = action_name.split(' ')
                        if len(parts) > 1:
                            ability = parts[-1].strip()  # Extract the ability number
                            if ability.isdigit():  # Only add valid numeric abilities
                                abilities_gained.add(int(ability))

        # Check if the player acquired all required skills to win
        acquired_all_required_skills = all(skill in abilities_gained for skill in required_skills_to_win)

        # Update ability distribution
        for ability in abilities_gained:
            abilities_distribution[ability] += 1

        # Convert path to tuple (immutable) and update path usage
        path_tuple = tuple(path)
        paths_used[path_tuple] += 1

        # Store each run for the player, including whether they acquired all required skills
        if player_name not in player_runs:
            player_runs[player_name] = []

        player_runs[player_name].append({
            'path': path,
            'abilities': sorted(abilities_gained),  # Sort abilities numerically
            'required_skills': required_skills_to_win,
            'acquired_all_required_skills': acquired_all_required_skills
        })

    return player_runs, abilities_distribution, paths_used, node_visits



# Define the root folder and scenario values to filter
root_folder = 'completedScenariosUnzippedDataRaw'
scenario_filter4 = [3]

# Fetch all results from the filtered scenarios
result_data4 = read_result_files(Constants.COMPLETED_SCENARIOS_FOLDER, scenario_filter4)

# Assuming 'result_data' is the data returned by read_result_files
player_runs4, abilities_distribution4, paths_used4, node_visits4 = collect_paths_and_abilities(result_data4)

# Collect all data in one structure
all_results4 = {
    'Player Runs': player_runs4,
    'Picked Abilities Counts': abilities_distribution4,
    'Paths Used': paths_used4,
    'Node Visit Counts': node_visits4,
    'Statistics': calculate_statistics(result_data4)
}

# Pretty print the collected data
pprint.pprint(all_results4)

scenario_filter2 = [2]

# Fetch all results from the filtered scenarios
result_data2 = read_result_files(Constants.COMPLETED_SCENARIOS_FOLDER, scenario_filter2)

# Assuming 'result_data' is the data returned by read_result_files
player_runs2, abilities_distribution2, paths_used2, node_visits2 = collect_paths_and_abilities(result_data2)

all_keys = list(set(list(player_runs2.keys()) + list(player_runs4.keys())))

isSame = 0
isNotSame = 0
for player in all_keys:
    pprint.pprint(player)
    if player_runs2.get(player) is not None and player_runs4.get(player) is not None:
        if player_runs2.get(player)[0]['path'] == player_runs4.get(player)[0]['path']:
            isSame = isSame + 1
            continue

    isNotSame = isNotSame + 1
pprint.pprint(isSame)
pprint.pprint(isNotSame)

# Collect all data in one structure
all_results2 = {
    'Player Runs': player_runs2,
    'Picked Abilities Counts': abilities_distribution2,
    'Paths Used': paths_used2,
    'Node Visit Counts': node_visits2,
    'Statistics': calculate_statistics(result_data2)
}
