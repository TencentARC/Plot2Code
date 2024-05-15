import argparse
import base64
import os
import json
import re
import time

# Generate the argparse
def get_parser():
    parser = argparse.ArgumentParser(description='Generate code from images using GPT-4 Vision')
    parser.add_argument('--image_directory', type=str, default='data/Plot2Code/test', help='Directory containing the images')
    parser.add_argument('--output_file', type=str, default='generated_code.jsonl', help='Output file to store the generated code')
    parser.add_argument('--model_name', type=str, default='gpt-4-vision-preview', help='Model name to use for generating the code')
    parser.add_argument('--model_path', type=str, default='/group/40034/chengyuewu/deepseek-vl-7b-chat', help='Model path to use for generating the code')
    parser.add_argument('--max_tokens', type=int, default=1024, help='Maximum tokens to use for generating the code')
    parser.add_argument('--temperature', type=int, default=0, help='Temperature to use for generating the code')
    parser.add_argument('--save_dir', type=str, default='generated_results', help='Directory to save the generated code')
    parser.add_argument('--prompt_strategy', type=str, default='default', help='Prompt strategy to use for generating the code')
    parser.add_argument('--ground_truth_code_file', type=str, default='data/Plot2Code/test/metadata.jsonl', help='ground truth code file')
    parser.add_argument('--max_retries', type=int, default=5, help='the maximum number of retries')
    parser.add_argument('--eval_dir', default='evaluation_results', type=str, help='Directory to save the evaluation results')
    parser.add_argument("--text_match_score_results", type=str, default="text_match_score.jsonl", help="Path to the JSONL file containing the text match scores")
    parser.add_argument("--gpt4-vision-evaluation-results", type=str, default="gpt_4v_evaluation_results.jsonl", help="Path to the JSONL file containing the GPT-4 Vision evaluation results")
    parser.add_argument('--final_score_results', type=str, default='final_score_results.jsonl', help='Output file to store the final score results')
    parser.add_argument('--instruct', action='store_true', help='Whether to use instruction or not')
    return parser


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_save_path(args):
    if args.instruct:
        save_path = os.path.join(args.save_dir, args.model_name, 'instruct', args.prompt_strategy, args.output_file)
    else:
        save_path = os.path.join(args.save_dir, args.model_name, 'direct', args.prompt_strategy, args.output_file)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    return save_path

def get_img_path(args):
    if args.instruct:
        save_path = os.path.join(args.save_dir, args.model_name, 'instruct', args.prompt_strategy, "generated_images")
    else:
        save_path = os.path.join(args.save_dir, args.model_name, 'direct', args.prompt_strategy, "generated_images")
    os.makedirs(save_path, exist_ok=True)
    return save_path

def get_eval_path(args):
    if args.instruct:
        save_path = os.path.join(args.eval_dir, args.model_name, 'instruct', args.prompt_strategy)
    else:
        save_path = os.path.join(args.eval_dir, args.model_name, 'direct', args.prompt_strategy)
    os.makedirs(save_path, exist_ok=True)
    return save_path

def read_jsonl_file(file_path):
    with open(file_path, 'r') as json_file:
        return [json.loads(line) for line in json_file]

def extract_code(response_str):
    matches = re.findall(r'```python(.*?)```', response_str, re.DOTALL)
    if matches:
        return "\n".join(match.strip() for match in matches)
    else:
        return response_str
        
def get_api_response(client, messages, args, model_name=None):
    retry_cnt = 0
            
    while retry_cnt < args.max_retries:
        try:
            response = client.chat.completions.create(
                model=args.model_name if model_name is None else model_name,
                messages=messages,
                max_tokens=args.max_tokens,
                n=1, 
                temperature=args.temperature,
            )
            break
        except Exception as e:
            backoff = 2 ** retry_cnt
            time.sleep(backoff)
            retry_cnt += 1
            print(f"Retry count: {retry_cnt}")
    return response
                    
direct_prompt = "You are a helpful assistant that can generate Python code using matplotlib." + \
                "Generate the matplotlib code to create a plot that looks like the given image, as similar as possible." + \
                "The generated code should be surrounded by ```python and ```\n"

CoT_prompt = "Let us think step by step."
