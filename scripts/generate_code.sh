# GPT-4V generate code (direct asking)
python -m plot2code.gpt4v_generate_code --prompt_strategy default

# GPT-4V generate code (conditional asking)
python -m plot2code.gpt4v_generate_code --prompt_strategy default --instruct

# GPT-4V generate code (conditional asking with CoT)
python -m plot2code.gpt4v_generate_code --prompt_strategy CoT --instruct