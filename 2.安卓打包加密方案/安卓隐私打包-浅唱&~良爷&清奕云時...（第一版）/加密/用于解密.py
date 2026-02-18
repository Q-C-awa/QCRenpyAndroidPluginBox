import os
import hashlib

# 设置固定密钥  # magicaluvwintertree1234567890
# 一定一定一定要和游戏里面的解密函数一样！！！！！

import os
import hashlib

def decrypt_image(encrypted_path, hashed_key):
    """解密单个加密图片文件并移除.enc后缀"""
    try:
        # 检查文件是否有.enc后缀
        if not encrypted_path.endswith(".enc"):
            print(f"跳过: {encrypted_path} (不是.enc文件)")
            return False
        
        # 读取加密文件
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()
        
        # 使用XOR解密
        decrypted = bytes(b ^ hashed_key[i % len(hashed_key)] 
                          for i, b in enumerate(encrypted_data))
        
        # 创建解密后的文件（移除.enc后缀）
        original_path = encrypted_path[:-4]  # 移除.enc后缀
        with open(original_path, "wb") as f:
            f.write(decrypted)
        
        # 删除加密文件
        os.remove(encrypted_path)
        
        return True
    except Exception as e:
        print(f"解密失败 {encrypted_path}: {str(e)}")
        return False

def main():
    # 设置固定密钥
    FIXED_KEY = input("输入解密密钥: ").encode()
    
    # 生成密钥
    hashed_key = hashlib.sha256(FIXED_KEY).digest()
    
    while True:
        target_dir = input("请输入解密目录(输入'quit'退出): ")
        
        if target_dir.lower() == 'quit':
            break
            
        # 检查目录是否存在
        if not os.path.exists(target_dir):
            print(f"错误: 目录 '{target_dir}' 不存在")
            continue
        
        decrypted_count = 0
        failed_count = 0
        
        # 遍历目录并解密图片
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith(".enc"):
                    full_path = os.path.join(root, file)
                    if decrypt_image(full_path, hashed_key):
                        decrypted_count += 1
                        original_name = full_path[:-4]  # 移除.enc后缀
                        print(f"已解密: {full_path} -> {original_name}")
                    else:
                        failed_count += 1
        
        print(f"\n解密完成!")
        print(f"成功解密: {decrypted_count} 个文件")
        print(f"解密失败: {failed_count} 个文件")
        print(f"使用的密钥: {FIXED_KEY.decode()}")
        print("-" * 50)

if __name__ == "__main__":
    main()