# Plot2Code Benchmark

Plot2Code benchmark is now open-sourced at [huggingface (ARC Lab)](https://huggingface.co/TencentARC) and [GitHub](https://github.com/TencentARC/Plot2Code). More information can be found in our [paper](https://arxiv.org/abs/2405.07990). 


This repository contains the code for an evaluation pipeline that generates Python code from reference plots, executes the generated code to draw plots, and then calculates various evaluation metrics to assess the quality of the generated code.

## Why we need [Plot2Code](https://huggingface.co/datasets/TencentARC/Plot2Code)?
* 🧐 While MLLMs have demonstrated potential in visual contexts, their capabilities in visual coding tasks have not been thoroughly evaluated. Plot2Code offers a platform for comprehensive assessment of these models.

* 🤗 To enable individuals to ascertain the proficiency of AI assistants in generating code that renders into plots given reference plots, we initiated the Plot2Code project. This ensures evaluations are pertinent to real-world applications.

* 💻 Plot2Code accommodates all modalities (text and images) for both input and output, facilitating an exploration of the influence of each modality.

## Supported Tasks

Plot2Code is primarily designed as a benchmark for code generation from scientific plots. Specifically, it supports the following settings:

* Text2Image: We provide instructions to the assistant, requesting it to generate pyplot code and subsequently render the plots.
* Image2Image: Referred to as the Direct Asking setting in our paper, we input the reference plot directly and ask the assistant to generate pyplot code to render similar plots.
* I+T 2 Image: Combining both instructions and reference plots as input, this is called the Conditional Asking setting in our paper.

By employing these settings, we can investigate the impact of each input modality on the quality of the final rendered plots.

## Requirements

- NumPy
- Matplotlib==3.8.4
- Pillow
- Levenshtein
- openai>1.12.0

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## How to Download
You can use following codes to download the dataset：
```shell
git lfs install
mkdir data
cd data
git clone https://huggingface.co/datasets/TencentARC/Plot2Code
```

## Usage

1. Generate code from reference plots. Add --instruction for the conditional setting.
``` bash
export OPENAI_API_KEY=[API_KEY]
export OPENAI_API_BASE=[API_BASE]

# GPT-4V generate code (direct asking)
python -m plot2code.gpt4v_generate_code --prompt_strategy default

# GPT-4V generate code (conditional asking)
python -m plot2code.gpt4v_generate_code --prompt_strategy default --instruct

# GPT-4V generate code (conditional asking with CoT)
python -m plot2code.gpt4v_generate_code --prompt_strategy CoT --instruct
```
2. Execute the generated code to render the plots.
``` bash
python -m plot2code.execute_generated_code --model_name "$model_name" --prompt_strategy $prompt_strategy

```
3. Evaluate the similarity between the generated plots and the grond truth plots.

``` bash
echo "Calculating text match score..."
python -m plot2code.eval.text_match_score  --model_name "$model_name"  --prompt_strategy $prompt_strategy

echo "Calculating gpt-4v evaluation score..."
python -m plot2code.eval.gpt4v_evaluations_score  --model_name "$model_name"  --prompt_strategy $prompt_strategy

echo "Combining evaluation results..."
python -m plot2code.eval.combine_evaluation_results  --model_name "$model_name"  --prompt_strategy $prompt_strategy
```

See [scripts](scripts) for more details.

# News
* 🔥[2024/08] We futther update the Python and R's plotly plot-code pairs with instruction for evaluation!🔥
* 🔥[2024/05] We open source the [Plot2Code benchmark](https://huggingface.co/datasets/TencentARC/Plot2Code).
Stay tuned for this project! 😆

# License

In this study, we crawled every website link listed in the Matplotlib gallery and Plotly documentation to collect data for our analysis. Both Matplotlib and Plotly libraries are distributed under permissive open-source licenses. We have taken the following steps to ensure compliance with the respective license terms:

1. Acknowledgment of Licenses: We acknowledge that the Matplotlib library and its gallery are distributed under the BSD 3-Clause License, and the Plotly library and its documentation are distributed under the MIT License.
2. Retention of Copyright Notices: We have retained all copyright notices and license information from the original Matplotlib gallery content and Plotly documentation, as required by their respective licenses.
3. Usage and Distribution: Our use of the Matplotlib gallery and Plotly documentation content is solely for academic and research purposes. We have not modified the original content from the Matplotlib gallery or Plotly documentation, and any distribution of our work will include proper attribution to the Matplotlib and Plotly projects.

By adhering to these guidelines, we ensure that our use of the Matplotlib and Plotly content is fully compliant with their respective licenses.

This project is open-sourced under the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0). These evaluation code and datasets are fully open for academic research and can be used for commercial purposes with official written permission. Check our [dataset sheet](dataset_sheet.pdf) for more information.

# Citation
The code and model in this repository is mostly developed for or derived from the paper below. Please cite it if you find the repository helpful.
```
@misc{wu2024plot2code,
      title={Plot2Code: A Comprehensive Benchmark for Evaluating Multi-modal Large Language Models in Code Generation from Scientific Plots}, 
      author={Chengyue Wu and Yixiao Ge and Qiushan Guo and Jiahao Wang and Zhixuan Liang and Zeyu Lu and Ying Shan and Ping Luo},
      year={2024},
      eprint={2405.07990},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
