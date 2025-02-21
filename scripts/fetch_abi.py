import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import argparse
import time
from src.ethereum.abi_fetcher import get_contract_addresses, get_abi
from src.database import get_db
from src.database.crud import upsert_contract


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_block', type=int)
    parser.add_argument('end_block', type=int)
    args = parser.parse_args()

    db = next(get_db())
    
    for block_num in range(args.start_block, args.end_block + 1):
        addresses = get_contract_addresses(block_num)
        
        if not addresses:
            print(f"区块 {block_num} 中没有找到合约地址，跳过该区块")
            continue
        
        for addr in addresses:
            abi = get_abi(addr)
            if abi:
                upsert_contract(db, {
                    "address": addr.lower(),
                    "abi": abi,
                    "block_number": block_num
                })
            time.sleep(0.2)

if __name__ == "__main__":           
    main()