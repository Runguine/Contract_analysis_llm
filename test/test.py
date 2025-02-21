import argparse
import requests
import json
import time
from web3 import Web3
import os

# ... existing code ...

# 添加新的常量
ETHERSCAN_ENDPOINT = 'https://api.etherscan.io/api'
ENDPOINT = 'https://eth-mainnet.g.alchemy.com/v2/Hmjf_IZrZoQ5t1xxSAtVlZVTxq9htQia'  # 替换为你想使用的服务
w3 = Web3(Web3.HTTPProvider(ENDPOINT))
API_KEY = '62Y48QX8M7ZHMCBNPH86I2J8ESFYG3SY76'

def get_contract_addresses_from_block(block_number):
    """获取指定区块中的所有合约地址"""
    try:
        # 获取区块信息
        block = w3.eth.get_block(block_number, full_transactions=True)
        contract_addresses = set()

        # 遍历区块中的所有交易
        for tx in block.transactions:
            # 如果交易有 'to' 地址且创建了合约
            if tx.to is None and tx.creates:
                contract_addresses.add(tx.creates)
            # 如果交易有合约交互
            elif tx.to:
                # 检查地址是否是合约
                if w3.eth.get_code(tx.to).hex() != '0x':
                    contract_addresses.add(tx.to)

        return list(contract_addresses)
    except Exception as e:
        print(f"获取区块合约地址时出错: {e}")
        return []

def get_contract_abi(contract_address):
    """获取合约ABI"""
    url = f"{ETHERSCAN_ENDPOINT}?module=contract&action=getabi&address={contract_address}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == '1' and response_json['message'] == 'OK':
                return json.loads(response_json['result'])
        return None
    except Exception as e:
        print(f"获取ABI时出错 {contract_address}: {e}")
        return None

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_block', type=int, help='起始区块号')
    parser.add_argument('end_block', type=int, help='结束区块号')
    parser.add_argument('-o', '--output', type=str, help="输出目录路径", required=True)
    
    args = parser.parse_args()
    
    # 添加创建输出目录的代码
    os.makedirs(args.output, exist_ok=True)
    
    for block_num in range(args.start_block, args.end_block + 1):
        print(f"处理区块 {block_num}")
        contract_addresses = get_contract_addresses_from_block(block_num)
        
        for addr in contract_addresses:
            print(f"处理合约地址: {addr}")
            abi = get_contract_abi(addr)
            
            if abi:
                # 为每个合约创建单独的文件
                output_file = f"{args.output}/contract_{addr}.json"
                with open(output_file, 'w') as f:
                    json.dump({"address": addr, "abi": abi}, f, indent=4)
                print(f"已保存ABI到 {output_file}")
            
            # 添加延迟以避免API限制
            time.sleep(0.2)

if __name__ == '__main__':
    __main__()