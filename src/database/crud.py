from sqlalchemy.orm import Session
from .models import Contract

from sqlalchemy import desc

def upsert_contract(db: Session, contract_data: dict):
    """增强版插入/更新合约数据"""
    contract = db.query(Contract).filter(Contract.address == contract_data["address"]).first()
    
    update_data = {
        'abi': contract_data.get('abi', []),
        'source_code': contract_data.get('source_code', []),
        'contract_name': contract_data.get('contract_name', ''),
        'address': contract_data.get('address', ''),
        'block_number': contract_data.get('block_number', '')
    }
    
    if contract:
        for key, value in update_data.items():
            setattr(contract, key, value)
    else:
        contract = Contract(**{**contract_data, **update_data})
        db.add(contract)
    
    db.commit()
    return contract

def update_bytecode(db: Session, address: str, bytecode: str):
    contract = db.query(Contract).filter(Contract.address == address).first()
    if contract:
        contract.bytecode = bytecode
        db.commit()
    return contract

def get_all_contract_abis_by_block(db: Session, block_number: int):
    """
    查询特定区块中的所有合约记录，并返回它们的 ABI
    :param db: 数据库会话
    :param block_number: 区块号
    :return: 包含所有合约 ABI 的列表（JSON 格式），如果未找到则返回空列表
    """
    contracts = (
        db.query(Contract)
        # .filter(Contract.block_number == block_number)  # 过滤特定区块
        .order_by(desc(Contract.created_at))  # 按创建时间降序排列
        # .all()  # 获取所有记录
        .first()
    )
    return [contract.abi for contract in contracts if contract.abi]  # 返回所有非空的 ABI

def get_latest_two_contract_abis(db: Session):
    """
    查询数据库中最新创建的两条合约记录，并返回它们的 ABI
    :param db: 数据库会话
    :return: 包含最新两条合约 ABI 的列表（JSON 格式），如果未找到则返回空列表
    """
    contracts = (
        db.query(Contract)
        # .order_by(desc(Contract.created_at))  # 按创建时间降序排列
        .limit(1)  # 限制查询结果为最新的两条记录
        .all()  # 获取所有符合条件的记录
    )
    return [contract.abi for contract in contracts if contract.abi]  # 返回所有非空的 ABI

def get_limit_contracts_source_code(db: Session):
    """
    查询数据库中最新创建的两条合约记录，并返回它们的 ABI
    :param db: 数据库会话
    :return: 包含最新两条合约 ABI 的列表（JSON 格式），如果未找到则返回空列表
    """
    contracts = (
        db.query(Contract)
        # .order_by(desc(Contract.created_at))  # 按创建时间降序排列
        .limit(530)  # 限制查询结果为最新的两条记录
        .all()  # 获取所有符合条件的记录
    )
    # 将每个 Contract 对象转换为字典
    contracts_dict = [contract.__dict__ for contract in contracts]
    return contracts_dict  # 返回所有非空的 ABI