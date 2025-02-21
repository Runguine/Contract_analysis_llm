import argparse
import time
from src.ethereum.bytecode_fetcher import get_bytecode
from src.ethereum.decompiler.gigahorse_wrapper import decompile_bytecode
from src.database import get_db
from src.database.crud import update_bytecode
from src.ethereum.abi_fetcher import get_contract_addresses

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_block', type=int)
    parser.add_argument('end_block', type=int)
    args = parser.parse_args()

    db = next(get_db())
    
    for block_num in range(args.start_block, args.end_block + 1):
        addresses = get_contract_addresses(block_num)
        for addr in addresses:
            bytecode = get_bytecode(addr)
            if bytecode:
                # 获取字节码成功，进行反编译
                decompiled_code = decompile_bytecode(bytecode, addr)
                if decompiled_code:
                    # 反编译成功，更新数据库
                    update_bytecode(db, addr, bytecode)
            time.sleep(0.2)

if __name__ == "__main__":
    main()
