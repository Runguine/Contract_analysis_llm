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

def get_contract_metadata(address):
    """获取合约元数据（包含ABI和源代码）"""
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={settings.ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1' and data['message'] == 'OK':
                return data['result'][0]
        return None
    except Exception as e:
        print(f"获取合约元数据失败 {address}: {e}")
        return None

def process_contract_metadata(metadata):
    """处理Etherscan返回的元数据"""
    processed = {
        'abi': json.loads(metadata.get('ABI', '[]')) if metadata.get('ABI') != 'Contract source code not verified' else [],
        'source_code': metadata.get('SourceCode', ''),
        'contract_name': metadata.get('ContractName', ''),
    }
    # 处理嵌套的源代码格式（Flattened和JSON格式）
    if processed['source_code'].startswith('{{'):
        try:
            sources = json.loads(processed['source_code'][1:-1])  # 去除外部花括号
            processed['source_code'] = "\n\n".join(
                f"// File: {name}\n{content['content']}" if isinstance(content, dict) and 'content' in content else f"// File: {name}\n{content}"
                for name, content in sources.get('sources', {}).items()
            )
        except json.JSONDecodeError:
            pass
    return processed