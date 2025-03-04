import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.ethereum.abi_fetcher import get_contract_addresses, get_contract_metadata, process_contract_metadata


from src.ethereum.bytecode_fetcher import get_bytecode
from src.ethereum.decompiler.gigahorse_wrapper import decompile_bytecode
from src.ethereum.abi_fetcher import get_contract_addresses


def get_source_code(start_block, end_block):
    contract_list = []  # 用于存储所有合约地址和源代码信息
    
    for block_num in range(start_block, end_block + 1):
        addresses = get_contract_addresses(block_num)
        
        if not addresses:
            print(f"区块 {block_num} 中没有找到合约地址，跳过该区块")
            continue
        
        for addr in addresses:
            # 获取完整元数据
            metadata = get_contract_metadata(addr)
            if not metadata:
                continue
                
            processed = process_contract_metadata(metadata)
            contract_data = {
                "address": addr.lower(),
                "block_number": block_num,
                **processed  # 包含ABI和源代码等字段
            }
            source_code = contract_data.get('source_code', None)
            if source_code:
                contract_list.append({"address": addr.lower(), "source_code": source_code})
    
    df_source_code = pd.DataFrame(contract_list)
    df_source_code.to_csv('test_sc.csv', index=False)
    return df_source_code


def get_compiled_bytecode(start_block, end_block):
    contract_list = []  # 用于存储所有合约地址和源代码信息

    for block_num in range(start_block, end_block + 1):
        addresses = get_contract_addresses(block_num)
        for addr in addresses:
            bytecode = get_bytecode(addr)
            if bytecode:
                # 获取字节码成功，进行反编译
                decompiled_code = decompile_bytecode(bytecode, addr)
                if decompiled_code:
                    # 反编译成功，更新数据库
                    contract_list.append({"address": addr.lower(), "decompiled_code": decompiled_code})

    df_decompiled = pd.DataFrame(contract_list)
    df_decompiled.to_csv('test_de.csv', index=False)
    return df_decompiled

def aggregate(start_block, end_block):
    df_source_code = get_source_code(start_block, end_block)
    df_decompiled = get_compiled_bytecode(start_block, end_block)
    df = pd.merge(df_source_code, df_decompiled, on="address", how='inner')
    return df

# test
df = aggregate(21035981, 21035981)
df.to_csv('test1.csv', index=False)