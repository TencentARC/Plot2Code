# #!/bin/bash

model_name=$1
prompt_strategy=$2
 
echo "Executing generated code to draw images..."
python -m plot2code.execute_generated_code --model_name "$model_name" --prompt_strategy $prompt_strategy

echo "Calculating text match score..."
python -m plot2code.eval.text_match_score  --model_name "$model_name"  --prompt_strategy $prompt_strategy

echo "Calculating gpt-4v evaluation score..."
python -m plot2code.eval.gpt4v_evaluations_score  --model_name "$model_name"  --prompt_strategy $prompt_strategy

echo "Combining evaluation results..."
python -m plot2code.eval.combine_evaluation_results  --model_name "$model_name"  --prompt_strategy $prompt_strategy

echo "Done!"