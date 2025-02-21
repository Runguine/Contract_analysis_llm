import subprocess
import os

def decompile_bytecode(bytecode, address):
    """使用 Gigahorse 反编译合约字节码"""
    try:
        # 将字节码保存为 .hex 文件
        hex_filename = f"/root/contract_analysis/src/data/decompiled/{address}.hex"  # 使用绝对路径
        os.makedirs(os.path.dirname(hex_filename), exist_ok=True)  # 确保目录存在
        
        with open(hex_filename, 'w') as f:
            f.write(bytecode)
            print(f"成功写入{address}")
            return True
        
    except Exception as e:
        print(f"反编译过程中出错: {e}")
        return None


import subprocess
import os
import re

def clean_ansi_codes(text):
    """移除所有ANSI转义序列"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def decompile_bytecode(bytecode, address):
    """使用 Panoramix 反编译合约字节码并保存反编译结果"""
    try:
        # 保存字节码到一个临时文件
        hex_filename = f"/root/contract_analysis/src/data/bytecode/{address}.hex"  # 使用绝对路径
        os.makedirs(os.path.dirname(hex_filename), exist_ok=True)  # 确保目录存在
        
        with open(hex_filename, 'w') as f:
            f.write(bytecode)
            print(f"成功写入{address}")

        # 运行 panoramix 反编译命令
        result = subprocess.run(
            [
                "panoramix", bytecode # 直接传递字节码字符串给 panoramix
            ],
            capture_output=True,
            env={**os.environ, 'TERM': 'dumb'},
            text=True
        )

        if result.returncode == 0:
            # 反编译成功，保存反编译结果到文件
            decompiled_filename = f"/root/contract_analysis/src/data/decompiled/{address}.txt"
            decompiled_code = clean_ansi_codes(result.stdout)   #去掉ANSI码
            with open(decompiled_filename, 'w') as f:
                f.write(decompiled_code)

            print(f"反编译成功，结果已保存至: {decompiled_filename}")
            return decompiled_filename
        else:
            # 反编译失败，打印错误信息
            print(f"反编译失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"反编译过程中出错: {e}")
        return None
