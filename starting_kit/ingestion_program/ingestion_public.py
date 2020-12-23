# Usage: python ingestion.py ingestion_program_dir input_dir output_dir submission_program_dir
#
# AS A PARTICIPANT, DO NOT MODIFY THIS CODE.
# This is the "ingestion program" written by the organizers.
# This program also runs on the challenge platform to test your code.
#
# The input directory input_dir (e.g. sample_data/) contains the xes-logs
#
# The output directory output_dir (e.g. sample_result_submission/)
# will receive the results of ingestion (no subdirectories):
#     results.pkl - pickle file which contains {net, starting_marking. final_marking} in pm4py implementation.
#
# The code directory submission_program_dir (e.g. sample_code_submission/) should contain your
# code submission player.py (an possibly other functions it depends upon).

import os
from sys import argv, path
import logging
import json

# =========================== BEGIN OPTIONS ==============================
# Logging mode
logging.basicConfig(level=logging.INFO)  # recommended to output all logging messages


# If no arguments to run.py are provided, this is where the data will be found
# and the results written to. Change the root_dir to your local directory.
root_dir = "../"
default_input_dir = root_dir + "sample_data"
default_output_dir = root_dir + "sample_result_submission"
default_program_dir = root_dir + "ingestion_program"
default_submission_dir = root_dir + "sample_code_submission"

version = 1
# =========================== END OPTIONS ================================


def do_u_wanna_play_a_game(map_list):
    ways = []
    for m in map_list:
        g = Game(*m)
        agent(g)
        ways.append((m, g.steps))
    return ways


def save_result_file(result_file, results):
    with open(result_file, 'w', encoding='utf8') as f:
        f.write(json.dumps(steps, indent=4, sort_keys=True))


# =========================== BEGIN PROGRAM ================================

if __name__ == "__main__":
    program_dir = default_program_dir
    input_dir = default_input_dir
    output_dir = default_output_dir
    submission_dir = default_submission_dir

    logging.info('\n****** Ingestion program version ' + str(version) + ' ******\n\n')

    # INPUT/OUTPUT: Get input and output directory names
    if len(argv) != 1:  # Use the default input and output directories if no arguments are provided
        program_dir = os.path.abspath(argv[1])
        input_dir = os.path.abspath(argv[2])
        output_dir = os.path.abspath(argv[3])
        submission_dir = os.path.abspath(argv[4])

    logging.info(f"Using program_dir: {program_dir}")
    logging.info(f"Using input_dir: {input_dir}")
    logging.info(f"Using output_dir: {output_dir}")
    logging.info(f"Using submission_dir: {submission_dir}")

    # Our libraries
    path.append(program_dir)
    path.append(submission_dir)

    from core import Game
    from agent import *

    # Public scoring maps
    map_list = [
        (20, 20, 5),
        (20, 20, 7),
        (20, 20, 10)
    ]

    steps = do_u_wanna_play_a_game(map_list)

    os.makedirs(output_dir, exist_ok=True)
    save_result_file(os.path.join(output_dir, 'steps.json'), steps)

    logging.info(f"GOOD GAME!!!")