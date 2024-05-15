import sys
from openai import OpenAI
import os
import json
from tqdm import tqdm
from .utils import get_parser, get_save_path, direct_prompt, read_jsonl_file, get_api_response, extract_code, CoT_prompt, encode_image
# Function to encode the image

parser = get_parser()

args = parser.parse_args()
# Directory containing your images
image_directory = args.image_directory

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE"), 
)

# Get current execute path
current_path = sys.path[0]

save_path = get_save_path(args)

previous_results = None
previous_filename = []

# check if the save_path is empty. if it is not empty, load the already generated results
if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
    previous_results = read_jsonl_file(save_path)
    previous_filename = [result['question_id'] for result in previous_results]

if args.instruct:
    instructions = read_jsonl_file('data/ground_truth_code_with_instruction.jsonl')
    
# Iterate through all the PNG files in the ground_truth folder
# Open the JSONL file
if __name__ == '__main__':
    
    with open(save_path, "w") as jsonl_file:

        # write the previous results to the file
        if previous_results is not None:
            for result in previous_results:
                jsonl_file.write(json.dumps(result) + '\n')
                jsonl_file.flush()
            
        for filename in tqdm(os.listdir(image_directory)):
            
            if filename in previous_filename:
                continue 
            
            if filename.endswith(".png"):
                image_path = os.path.join(current_path, image_directory, filename)

            # Getting the base64 string
            base64_image = encode_image(image_path)

            if args.instruct:
                prompt = instructions[int(filename.rstrip('.png').lstrip('ground_truth_image_'))]['instruction'] + '\n' + direct_prompt
            else:
                prompt = direct_prompt

            messages =  [
                            {
                                "role": "system",
                                "content": "You are a helpful assistant."
                            }, 
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}" if 'gpt' in args.model_name else image_path
                                        },
                                    },
                                ],
                            }
                        ]
            
            if args.prompt_strategy == 'CoT':
                messages.append(
                    {
                        "role": "assistant",
                        "content": CoT_prompt
                    }
                ) 
                response = get_api_response(client, messages, args)
            elif args.prompt_strategy == 'Plan-and-Solve':   
                step1_prompt = 'Let us first describe the plot and make a detailed plan step by step.'
                step2_prompt = ' Based on the above description, now we are prepared to generate the code. The generated code is surrounded by ```python and ``` to make it easier to be extracted by regular expressions. Therefore, the code is:'
                  
                messages.append(
                    {
                        "role": "assistant",
                        "content": step1_prompt
                    }
                )
                response = get_api_response(client, messages, args)
                tmp_result = extract_code(response.choices[0].message.content.strip())
                if tmp_result != response.choices[0].message.content.strip():
                    print('step1')
                    jsonl_file.write(json.dumps({'code': tmp_result, 'question_id': filename, 'ground_truth_path': image_path}) + "\n")
                    jsonl_file.flush()
                    continue
                print('steps2')
                messages.append(
                    {
                        "role": "assistant", 
                        "content": response.choices[0].message.content.strip() + step2_prompt
                    }
                )
                response = get_api_response(client, messages, args) 
            else:
                response = get_api_response(client, messages, args)
                
            generated_code = extract_code(response.choices[0].message.content.strip())
                
            jsonl_file.write(json.dumps({'code': generated_code, 'question_id': filename, 'ground_truth_path': image_path}) + "\n")
            jsonl_file.flush()