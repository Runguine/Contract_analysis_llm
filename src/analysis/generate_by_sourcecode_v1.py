import sys
import os
import json
import time  # 引入time模块

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.database import get_db
from src.database.crud import get_all_contract_abis_by_block, get_latest_two_contract_abis, get_limit_contracts_source_code
from scripts.fetch_llm import request_ds
from config.settings import settings

SOURCECODE_PROMPT = settings.SOURCECODE_PROMPT
DECOMPILED_PROMPT = settings.DECOMPILED_PROMPT

import pandas as pd
data = []

db = next(get_db())

abis = get_limit_contracts_source_code(db)

for abi in abis:
    source_code = abi['source_code']
    address = abi['address']
    bytecode = abi['bytecode']
    explanation_decompiled = None  # 初始化为空，以防文件不存在时仍能加入字典
    if source_code is not None:
        # print(explanation)

        # 根据address地址 查找绝对路径下的文件
        file_path = os.path.join('/root/contract_analysis/src/data/decompiled', f'{address}.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                decompiled_data = file.read()
            explanation_decompiled = request_ds(DECOMPILED_PROMPT, decompiled_data)
            explanation_sourcecode = request_ds(SOURCECODE_PROMPT, source_code)

            data.append(
                {
                    'address': address, 
                    'explanation_sourcecode': explanation_sourcecode, 
                    'explanation_decompiled': explanation_decompiled
                }
            )
        else:
            print(f"File not found: {file_path}")  # 打印文件未找到的消息
            continue  # 跳过当前记录，继续下一个循环

results = pd.DataFrame(data)

results.to_csv('contract_explanations_v2.csv', index=False)
print('Generated Dataset.')