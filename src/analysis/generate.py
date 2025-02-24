# 读数据库
# 对每条记录 生成解释
# 存csv文件

import sys
import os
import json  # 导入 json 模块

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.database import get_db
from src.database.crud import get_all_contract_abis_by_block, get_latest_two_contract_abis, get_limit_contracts_source_code
from scripts.fetch_llm import request_ds
from config.settings import settings

db = next(get_db())
# 获取 abis，转换为 JSON 格式
abis = get_latest_two_contract_abis(db)
abis_json = json.dumps(abis)
abis_object = json.loads(abis_json)

print(len(abis_object))

for abi in abis_object:
    print(abi)

# PROMPT = settings.PROMPT

# response = request_ds(PROMPT, abis_json)
# print(response)