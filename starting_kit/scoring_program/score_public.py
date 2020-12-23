#!/usr/bin/env python

# Some libraries and options
import os
from sys import argv, path
import logging
import json

# =========================== BEGIN OPTIONS ==============================
# Logging mode
logging.basicConfig(level=logging.INFO)  # recommended to output all logging messages

# Default I/O directories:
root_dir = "../"
root_dir = ""
default_input_ref_dir = root_dir + "sample_reference_data"
default_input_res_dir = root_dir + "sample_result_submission"
default_output_dir = root_dir + "scoring_output"
default_program_dir = root_dir + "scoring_program"
res_file = 'steps.json'

# Version number
scoring_version = 1
# =========================== END OPTIONS ================================

def load_result_file(result_file):
    with open(result_file, 'r', encoding='utf8') as f:
        results = json.loads(f.read())
    return results


def get_scoring(results):
    score = []
    for r in results:
        g = Game(*r[0])
        score.append(g.run_game_emulation(r[1]))
    return score


# =========================== BEGIN PROGRAM ================================

if __name__ == "__main__":
    program_dir = default_program_dir
    input_ref_dir = default_input_ref_dir
    input_res_dir = default_input_res_dir
    output_dir = default_output_dir

    logging.info('\n****** Scoring program version ' + str(scoring_version) + ' ******\n\n')

    # INPUT/OUTPUT: Get input and output directory names
    if len(argv) != 1:
        input_dir = argv[1]
        output_dir = argv[2]
        input_ref_dir = os.path.join(input_dir, 'ref')
        input_res_dir = os.path.join(input_dir, 'res')

    logging.info(f"Using program_dir: {program_dir}")
    logging.info(f"Using output_dir: {output_dir}")
    logging.info(f"Using ref_dir: {input_ref_dir}")
    logging.info(f"Using res_dir: {input_res_dir}")

    path.append(default_program_dir)
    from core import Game

    results = load_result_file(os.path.join(input_res_dir, res_file))

    score = get_scoring(results)

    logging.info(f"Total score: {sum(score)}")

    # Create the output directory, if it does not already exist and open output files
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'scores.txt'), 'w') as score_file:
        score_file.write('SmallMapScore' + ": %0.4f\n" % score[0])
        score_file.write('MediumMapScore' + ": %0.4f\n" % score[1])
        score_file.write('LargeMapScore' + ": %0.4f\n" % score[2])
        score_file.write('TotalScore' + ": %0.4f\n" % sum(score))