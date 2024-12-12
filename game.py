import json
import time
from datetime import datetime
import random

import Constants

DEBUG = False


def debug_print(text):
    if DEBUG:
        print(text)


def can_go_to_next(required_abilities, gained_abilities):
    debug_print("ca")
    debug_print(required_abilities)
    debug_print(gained_abilities)

    for required_ability in required_abilities:
        if required_ability not in gained_abilities:
            return False

    return True


def scenario(connections_file, nodes_file):
    historyOfActions = {}
    historyOfActions["isWin"] = False
    actionIndex = 0

    with open(connections_file, 'r') as file:
        connections = json.load(file)

    with open(nodes_file, 'r') as file:
        nodes = json.load(file)

    debug_print(nodes)
    debug_print(connections)

    gained_abilities = [0]
    current_node = nodes["start"]

    while current_node != nodes["end"]:
        print()
        print("You are at: " + current_node)
        print("Your abilities: " + str(gained_abilities))
        print()
        abilities_to_gain = [ability for ability in nodes[current_node] if ability not in gained_abilities]

        if abilities_to_gain is not None and len(abilities_to_gain) > 0:
            print("You can gain following abilities: " + str(abilities_to_gain))
            print()

        to_connections = connections[current_node]

        nodes_to_go = []
        debug_print(to_connections)

        keys = list(to_connections.keys())
        random.shuffle(keys)
        for key in keys:
            required_abilities = to_connections[key]
            if isinstance(required_abilities[0], list):
                debug_print(required_abilities)
                for inner_required_abilities in required_abilities:
                    debug_print(inner_required_abilities)
                    debug_print(gained_abilities)
                    if can_go_to_next(inner_required_abilities, gained_abilities):
                        print("You can go to " + key)
                        nodes_to_go.append(key)
                    else:
                        print("There is a road which requires multiple abilities: " + str(inner_required_abilities))
            else:
                for req_ability in required_abilities:
                    if can_go_to_next([req_ability], gained_abilities):
                        print("You can go to " + key)
                        nodes_to_go.append(key)
                    else:
                        print("There is a road which requires ability: " + str(req_ability))

        print("What you want to do?")
        print("""
                Select one of the actions:
                    gain <ability>  (ex: gain 1)
                    go <room>       (ex: go N1)   
                    quit            (ex: quit)
            """)

        try:
            action = input("action:")
            actionIndex = int(actionIndex)
            actionIndex = actionIndex + 1
            actionIndex = str(actionIndex)
            historyOfActions[actionIndex] = {}
            historyOfActions[actionIndex]['action'] = action
            historyOfActions[actionIndex]['isOkayAction'] = False
            historyOfActions[actionIndex]['message'] = None
            historyOfActions[actionIndex]['startTime'] = time.time()

            action_split = action.split()

            if action_split[0] == "quit":
                break

            if action_split[0] == "go":
                if action_split[1] in nodes_to_go:
                    current_node = action_split[1]

                    message = "You went to " + action_split[1]
                    print(message)

                    historyOfActions[actionIndex]['isOkayAction'] = True
                    historyOfActions[actionIndex]['message'] = message

                else:
                    message = "You can not go to " + action_split[1]
                    print(message)
                    historyOfActions[actionIndex]['message'] = message


            if action_split[0] == "gain":
                ability = int(action_split[1])
                if ability in abilities_to_gain:
                    gained_abilities.append(ability)

                    message = "You gained " + action_split[1] + " ability."
                    print(message)

                    historyOfActions[actionIndex]['isOkayAction'] = True
                    historyOfActions[actionIndex]['message'] = message

                elif ability in gained_abilities:
                    message = "You already have this."
                    print(message)
                    historyOfActions[actionIndex]['message'] = message

                else:
                    message = "This ability is not available in this room."
                    print(message)
                    historyOfActions[actionIndex]['message'] = message

        except Exception as e:
            message = f"Unexpected Error: {e}"
            historyOfActions[actionIndex]['message'] = message
            continue

    print()
    if current_node == nodes["end"]:
        print("You won")
        historyOfActions["isWin"] = True

    print("Game ended")
    return historyOfActions

scenario_data = {}
email = input("Enter your email:")
name = input("Enter your name:")
surname = input("Enter your surname:")
scenario_data["email"] = email
scenario_data["name"] = name
scenario_data["surname"] = surname

while True:
    scenario_index = input("Select scenario(q for quit):")
    if scenario_index == 'q':
        break

    all_dicts = []
    elapsedTimes = {}
    print("Scenario: " + str(scenario_index))
    start_time = time.time()  # Record start time
    historyOfActions = scenario(Constants.create_file_name(scenario_index, Constants.CONNECTIONS_FILE_NAME),
             Constants.create_file_name(scenario_index, Constants.NODES_FILE_NAME))
    end_time = time.time()  # Record end time

    scenario_data["elapsedTime"] = end_time - start_time
    scenario_data["historyOfActions"] = historyOfActions

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(Constants.create_file_name(scenario_index, Constants.SCENARIO_RESULTS, current_time), 'w') as file:
        json.dump(scenario_data, file, indent=4)
