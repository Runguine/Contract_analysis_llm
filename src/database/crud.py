from sqlalchemy.orm import Session
from .models import Contract

from sqlalchemy import desc

def upsert_contract(db: Session, contract_data: dict):
    """插入或更新合约数据"""
    contract = db.query(Contract).filter(Contract.address == contract_data["address"]).first()
    if contract:
        # 更新已有记录（如追加bytecode）
        for key, value in contract_data.items():
            setattr(contract, key, value)
    else:
        # 插入新记录
        contract = Contract(**contract_data)
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
        .order_by(desc(Contract.created_at))  # 按创建时间降序排列
        .limit(1)  # 限制查询结果为最新的两条记录
        .all()  # 获取所有符合条件的记录
    )
    return [contract.abi for contract in contracts if contract.abi]  # 返回所有非空的 ABI