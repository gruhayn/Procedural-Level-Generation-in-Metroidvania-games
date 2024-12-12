import json
import time
import tracemalloc
import random

from mapGen import generate_map


def measure_performance(seed, min_path_count, room_count, skill_count, sliding_count, neighbor_distance,
                        backward_step_count, required_skills, output_file):
    input_params = {
        "Seed": seed,
        "Minimum Winning Path Count": min_path_count,
        "Room Count": room_count,
        "Skill Count": skill_count,
        "Sliding Count": sliding_count,
        "Neighbor Distance": neighbor_distance,
        "Backward Step Count": backward_step_count,
        "Required Skills to Win": required_skills
    }

    tracemalloc.start()
    start_time = time.perf_counter()  # Using perf_counter for both elapsed and CPU-like measurement

    # Run the generate_map function
    graph = generate_map(
        seed,
        min_path_count,
        room_count,
        skill_count,
        sliding_count,
        neighbor_distance,
        backward_step_count,
        required_skills,
        input_params
    )

    # Stop the timer and tracemalloc
    end_time = time.perf_counter()
    memory_used, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_time = end_time - start_time
    cpu_time = elapsed_time  # As an approximation for both CPU and elapsed time
    memory_used = memory_used / (1024 * 1024)  # Convert to MB
    peak_memory = peak_memory / (1024 * 1024)  # Convert to MB

    result = {
        "input_params": input_params,
        "elapsed_time": elapsed_time,
        "cpu_time": cpu_time,
        "memory_used": memory_used,
        "peak_memory": peak_memory
    }

    # Write result to file
    with open(output_file, "a") as file:
        json.dump(result, file, indent=4)
        file.write(",\n")  # Add comma for JSON array format

    print(f"Test complete for seed {seed}. Results saved to {output_file}")


room_count_range = [10, 20, 30]           # Three representative values for room counts
skill_count_range = [3, 8, 13]           # Three values for skill counts to cover low, medium, and high
min_path_count_range = [1, 3, 5]          # Three values for minimum path counts
sliding_count_range = [1, 3, 5]              # Two values for sliding counts to limit complexity
neighbor_distance_range = [1, 3, 5]          # Two values for neighbor distance to capture adjacency variation
backward_step_count_range = [1, 3, 5]    # Three values for backward steps to test low, medium, and high


output_file = "comprehensive_performance_results.json"

# Initialize the file with an open JSON array
with open(output_file, "w") as file:
    file.write("[\n")

# Run tests for 100 scenarios
test_count = 0
for room_count in room_count_range:
    for skill_count in skill_count_range:
        for min_path_count in min_path_count_range:
            for sliding_count in sliding_count_range:
                for neighbor_distance in neighbor_distance_range:
                    for backward_step_count in backward_step_count_range:
                        print(f'room_count {room_count} skill_count {skill_count} min_path_count {min_path_count} sliding_count {sliding_count} neighbor_distance {neighbor_distance} backward_step_count {backward_step_count}')
                        print(test_count)
                        # if test_count >= 100:
                        #     break
                        seed = random.randint(0, 1_000_000)
                        required_skills = [i for i in range(min(skill_count, 10))]  # Limit required skills to available skills
                        measure_performance(
                            seed,
                            min_path_count,
                            room_count,
                            skill_count,
                            sliding_count,
                            neighbor_distance,
                            backward_step_count,
                            required_skills,
                            output_file
                        )
                        test_count += 1

# Close the JSON array in the file
with open(output_file, "a") as file:
    file.write("]\n")

print(f"All tests complete. Results for {test_count} scenarios saved to {output_file}.")
