from flask import Flask, jsonify
from web3 import Web3
from src.ethereum.bytecode_fetcher import get_bytecode
from src.ethereum.decompiler.gigahorse_wrapper_api import decompile_bytecode

app = Flask(__name__)

@app.route('/decompile/<address>', methods=['GET'])
def get_decompiled_code(address):
    """反编译接口"""
    # 地址格式验证
    if not Web3.is_address(address):
        return jsonify({"error": "Invalid Ethereum address"}), 400


    # 情况2：需要实时反编译
    bytecode = get_bytecode(address)
    if not bytecode:
        return jsonify({"error": "Contract bytecode not found"}), 404

    # 执行反编译
    decompiled_path = decompile_bytecode(bytecode, address)
    if not decompiled_path:
        return jsonify({"error": "Decompilation failed"}), 500
    
    # 返回结果
    with open(decompiled_path, 'r') as f:
        return jsonify({
            "address": address,
            "decompiled_code": f.read()
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)