from pathlib import Path

CONNECTIONS_FILE_NAME = "CONNECTIONS.json"
NODES_FILE_NAME = "NODES.json"
SCENARIO_PARAMS = "SCENARIO_PARAMS.json"
SCENARIO_RESULTS = "SCENARIO_RESULTS.json"

COMPLETED_SCENARIOS_FOLDER = "completedScenariosUnzippedDataRaw"
def create_file_name(scenario_index, filename, time = None):
    if time is None:
        path = Path(get_base_folder(scenario_index), filename)
    else:
        path = Path(get_base_folder(scenario_index), "T"+time+"T"+filename)

    return path


def get_base_folder(scenario_index):
    return Path("scenarios", str(scenario_index))
