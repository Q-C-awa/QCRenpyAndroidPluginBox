import os
import hashlib

# 设置固定密钥  # magicaluvwintertree1234567890
# 一定一定一定要和游戏里面的解密函数一样！！！！！

def encrypt_image(image_path, hashed_key):
    """加密单个图片文件并添加.enc后缀"""
    try:
        # 读取图片
        with open(image_path, "rb") as f:
            data = f.read()
        # 使用XOR加密
        encrypted = bytes(b ^ hashed_key[i % len(hashed_key)] 
                          for i, b in enumerate(data))
        # 创建加密后的文件（添加.enc后缀）
        encrypted_path = image_path + ".enc"
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)
        # 删除原始文件
        os.remove(image_path)
        return True
    except Exception as e:
        print(f"加密失败 {image_path}: {str(e)}")
        return False
def main():
    # 设置固定密钥
    FIXED_KEY = input("输入密钥: ").encode()
    # 生成密钥
    hashed_key = hashlib.sha256(FIXED_KEY).digest()
    while True:
        target_dir = input("请输入加密目录(输入'quit'退出): ")  
        if target_dir.lower() == 'quit':
            break
        # 检查目录是否存在
        if not os.path.exists(target_dir):
            print(f"错误: 目录 '{target_dir}' 不存在")
            continue
        encrypted_count = 0
        failed_count = 0  
        # 遍历目录并加密图片
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".webp", ".gif")):
                    full_path = os.path.join(root, file)
                    if encrypt_image(full_path, hashed_key):
                        encrypted_count += 1
                        print(f"已加密: {full_path} -> {full_path}.enc")
                    else:
                        failed_count += 1
        print(f"\n加密完成!")
        print(f"成功加密: {encrypted_count} 个文件")
        print(f"加密失败: {failed_count} 个文件")
        print(f"使用的密钥: {FIXED_KEY.decode()}")
        print("-" * 50)
if __name__ == "__main__":
    main()

# magicaluvwintertree1234567890
# D:\Renpy_project\MemoriesoftheWinterTree\game\images\char