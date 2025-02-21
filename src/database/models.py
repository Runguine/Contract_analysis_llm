from sqlalchemy import Column, String, JSON, BigInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contract(Base):
    __tablename__ = "contracts"

    address = Column(String(42), primary_key=True)
    abi = Column(JSON)
    bytecode = Column(String)
    block_number = Column(BigInteger)
    created_at = Column(TIMESTAMP, server_default='NOW()')