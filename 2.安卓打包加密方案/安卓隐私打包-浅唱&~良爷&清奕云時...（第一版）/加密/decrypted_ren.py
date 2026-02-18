"""renpy

python early:

"""

# # 解密单个文件
# $ xor_manager.decrypt_file("images/11.png")

# # 解密整个目录(递归)(会解密所有包括子目录)
# $ xor_manager.decrypt_directory("images/")

# 导入模块
import os
import hashlib

class XORResourceManager:
    def __init__(self, secret_key):
        # 用原始方法生成密钥
        self.hashed_key = hashlib.sha256(secret_key.encode()).digest()
    def _get_absolute_path(self, path):
        """相对路径转成绝对路径"""
        if not os.path.isabs(path):
            return os.path.join(config.gamedir, path)
        return path
    def _xor_data(self, data):
        """这里是XOR解密的核心"""
        key_length = len(self.hashed_key)
        return bytes(b ^ self.hashed_key[i % key_length] for i, b in enumerate(data))
    def decrypt_file(self, file_path):
        """文件解密处理核心"""
        # 路径处理
        abs_path = self._get_absolute_path(file_path)    
        # 检查文件是否存在
        if not os.path.exists(abs_path):
            renpy.notify(f"找不到文件: {file_path}")
            return False 
        if not abs_path.endswith('.enc'):
            return False   
        try:
            # 读取文件
            with open(abs_path, "rb") as f:
                file_data = f.read()        
            # 解密数据
            decrypted_data = self._xor_data(file_data)        
            # 写回文件
            with open(abs_path, "wb") as f:
                f.write(decrypted_data)        
            # 移除 .enc 后缀，恢复原始文件名
            original_path = abs_path[:-4]  # 去掉 .enc 后缀
            os.rename(abs_path, original_path)        
            return True        
        except Exception as e:
            renpy.notify(f"解密文件 {os.path.basename(file_path)} 时出错: {str(e)}")
            return False
    def decrypt_directory(self, directory_path):
        """解密整个目录的文件，只处理 .enc 结尾的文件"""
        abs_path = self._get_absolute_path(directory_path)    
        if not os.path.exists(abs_path):
            renpy.notify(f"目录不存在: {directory_path}")
            return False    
        if not os.path.isdir(abs_path):
            renpy.notify(f"这不是一个目录: {directory_path}")
            return False
        try:
            count = 0 # 解压文件的计数器（其实没啥用可以删）     
            for root, dirs, files in os.walk(abs_path):
                for file in files:
                    if file.endswith('.enc'): 
                        file_path = os.path.join(root, file)
                        if self.decrypt_file(file_path):
                            count += 1  
            if count > 0: 
                renpy.notify(f"完成了 {count} 个加密文件的解密")
            else:
                renpy.notify(f"在目录中未找到 .enc 加密文件")
            return True        
        except Exception as e:
            renpy.notify(f"解密目录时出了点问题: {str(e)}")
            return False
# 初始化资源管理器（保持原始密钥不变）
xor_manager = XORResourceManager(secret_key="1145")
