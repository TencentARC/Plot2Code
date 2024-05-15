import json
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from matplotlib.pyplot import *
from .utils import get_parser, read_jsonl_file, get_save_path, get_img_path
from tqdm import tqdm
import matplotlib
parser = get_parser()

args = parser.parse_args()

import multiprocessing

def execute_code(code, success_flag, image_path):
    try:
        exec(code)
        fig = plt.gcf()
        # Save the generated image with the same size as the ground truth image
        fig.savefig(image_path)
        success_flag.value = True

    except Exception as e:
        # print(e)
        pass

def execute_code_and_save_image(code, ground_truth_path, image_path):
    # Get the ground truth image size
    ground_truth_image = Image.open(ground_truth_path)
    ground_truth_size = ground_truth_image.size

    success_flag = multiprocessing.Value("b", False)

    # create a process to execute the code
    code_process = multiprocessing.Process(target=execute_code, args=(code, success_flag, image_path))
    code_process.start()

    # set a timer of 30 seconds
    code_process.join(30)

    # if the process is still running, terminate it
    if code_process.is_alive():
        code_process.terminate()
        code_process.join()

    if success_flag.value:
        generated_image = Image.open(image_path)
    else:
        # Create a white image and save it
        generated_image = Image.fromarray(np.full((ground_truth_size), 255, dtype=np.uint8))

    # resized_image = generated_image.resize(ground_truth_size)s
    generated_image.save(image_path)

def main():
    # Read the ground truth code JSONL file
    ground_truth_code_list = read_jsonl_file(args.ground_truth_code_file)
    
    # Read the generated code JSONL file
    generated_code_file =  get_save_path(args)
    code_list = read_jsonl_file(generated_code_file)

    # Create the test_images folder if it doesn't exist
    test_images_folder = get_img_path(args)
    data = []
    for item in tqdm(code_list):
        # Execute the code and save the images to the test_images folder
        code = item['code']
        ground_truth_path = item['ground_truth_path']
        idx = int(ground_truth_path.rstrip('.png').split('ground_truth_image_')[-1])
        image_path = os.path.join(test_images_folder, f"test_image_{idx}.png")
        execute_code_and_save_image(code, ground_truth_path, image_path)
        plt.close()
        matplotlib.rcdefaults()
        plt.cla()
        plt.clf()
        plt.close("all")
        # Get the ground truth code for the current item
        ground_truth_code = ground_truth_code_list[idx]['code']

        data.append({'ground_truth_code': ground_truth_code, 'code': code, 'ground_truth_path': ground_truth_path, 'generated_image_path': image_path})


    # Open the JSONL file in write mode
    with open(generated_code_file, "w") as jsonl_file:
        # Append the generated image path to the JSONL file
        for item in data:
            jsonl_file.write(json.dumps(item) + "\n")
            jsonl_file.flush()
        
if __name__ == '__main__':
    main()