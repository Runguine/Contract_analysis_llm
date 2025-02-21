import requests
import json
from web3 import Web3
from config.settings import settings
import rlp
from eth_utils import to_checksum_address

w3 = Web3(Web3.HTTPProvider(settings.ALCHEMY_ENDPOINT))

def get_contract_addresses(block_number):
    """获取区块中的合约地址"""
    try:
        # 获取区块信息
        block = w3.eth.get_block(block_number, full_transactions=True)
        contract_addresses = set()

        # 遍历区块中的所有交易
        for tx in block.transactions:
            tx_dict = dict(tx)  # 转换为字典
    
            # 合约创建交易
            if not tx_dict.get('to'):
                sender = tx_dict['from']
                nonce = w3.eth.get_transaction_count(
                    sender, 
                    block_identifier=block_number
                )
                raw = rlp.encode([Web3.to_bytes(hexstr=sender), nonce])
                contract_address = to_checksum_address(Web3.keccak(raw)[12:].hex())
                contract_addresses.add(contract_address)
    
            # 合约调用交易
            else:
                to_address = tx_dict['to']
                if w3.eth.get_code(to_address, block_identifier=block_number).hex() != '0x':
                    contract_addresses.add(to_address)

        return list(contract_addresses)
    
    except Exception as e:
        print(f"获取区块合约地址时出错: {e}")
        return []  # 确保返回一个空列表

def get_abi(address):
    """获取合约ABI"""
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={settings.ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == '1' and response_json['message'] == 'OK':
                return json.loads(response_json['result'])
        return []
    except Exception as e:
        print(f"获取ABI时出错 {contract_addresses}: {e}")
        return []