import json
import os
import numpy as np
from ..utils import get_parser, get_eval_path, get_save_path

parser = get_parser()
args = parser.parse_args()
# Function to read the JSONL file and load the content into a list
def read_jsonl_file(jsonl_file):
    content_list = []
    with open(jsonl_file, "r") as file:
        for line in file:
            content_list.append(json.loads(line))
    return content_list

eval_dir = get_eval_path(args)
generated_code_file = get_save_path(args)

text_match_score_results_file = os.path.join(eval_dir, args.text_match_score_results)
gpt4v_evaluation_results_file = os.path.join(eval_dir, args.gpt4_vision_evaluation_results)
final_score_file = os.path.join(eval_dir, args.final_score_results)

# Read the JSONL files
generated_code_results = read_jsonl_file(generated_code_file)
text_match_score_results = read_jsonl_file(text_match_score_results_file)
evaluations_results = read_jsonl_file(gpt4v_evaluation_results_file)
# Initialize the list to store the final results
final_results = []

# Iterate over the items in the lists
for text_match, evaluation in zip(text_match_score_results, evaluations_results):
    # Create a new dictionary to store the final result for the current item
    final_result = {}

    # Add the evaluation results to the final result
    final_result.update(text_match)
    final_result.update(evaluation)

    # Append the final result to the list of final results
    final_results.append(final_result)

# Write the final results to a new JSONL file
with open(final_score_file, "w") as file:
    for final_result in final_results:
        file.write(json.dumps(final_result) + "\n")

    # Calculate the average of each evaluation metric
    average_text_match_score = np.mean([result['text_match_score'] for result in final_results])
    average_evaluation_score = np.mean([result['rating'] for result in final_results if result['rating'] is not None])

    file.write(f'Code pass rate: {(len(final_results)) / len(generated_code_results)}\n')
    file.write(f"Average text match score: {average_text_match_score}\n")
    file.write(f"Average gpt-4v evaluation score: {average_evaluation_score}\n")

print(f'Code pass rate: {(len(final_results)) / len(generated_code_results)}\n')
print(f"Average text match score: {average_text_match_score}\n")
print(f"Average gpt-4v evaluation score: {average_evaluation_score}\n")