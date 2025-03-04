import sys
import os
import pandas as pd
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from scripts.fetch_llm import request_ds
from config.settings import settings

COMPARE_PROMPT = "You are an expert in blockchain smart contracts and code review. I will provide you with two explanations: one for the source code and one for the decompiled code of the same smart contract. Your task is to determine whether these two explanations are consistent. Respond with only “Consistent” or “Inconsistent” without any additional explanation. Note that your result should focus more on the overall contract explanation."

data = pd.read_csv('contract_explanations_compare_result_v2.csv')

results = []

for index, row in data.iterrows():
    source_explanation = row['explanation_sourcecode']
    decompiled_explanation = row['explanation_decompiled']

    explanation = f"Explanation of source code: {source_explanation} Explanation of decompiled code: {decompiled_explanation}"

    try:
        result = request_ds(COMPARE_PROMPT, explanation)
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        result = "Error"

    results.append(result)
    
    # time.sleep(1)

data['result_openai'] = results

data.to_csv('contract_explanations_compare_result_v3.csv', index=False)

print("Processing complete. Results saved.")