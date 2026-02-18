import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class DecryptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("(.enc文件专用)")
        self.root.geometry("1000x800")  # 增加高度以确保按钮可见
        self.root.resizable(True, True)  # 允许调整大小
        
        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("decrypt.ico")
        except:
            pass
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        self.style.configure("Header.TLabel", font=("Arial", 20, "italic"))
        self.style.configure("Subtitle.TLabel", font=("Arial", 20, "italic"))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(self.main_frame, text="图片解密工具", style="Header.TLabel")
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(self.main_frame, text="解密 .enc 后缀", style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 20))
        
        # 密钥输入区域
        key_frame = ttk.Frame(self.main_frame)
        key_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(key_frame, text="解密密钥:").pack(anchor=tk.W)
        
        key_help_frame = ttk.Frame(key_frame)
        key_help_frame.pack(fill=tk.X, pady=(2, 0))
        
        ttk.Label(key_help_frame, text="必须与加密时使用的密钥完全相同", foreground="gray").pack(anchor=tk.W)
        
        self.key_entry = ttk.Entry(key_frame, width=50, show="*")
        self.key_entry.pack(fill=tk.X, pady=(5, 0))
        
        # 显示/隐藏密钥按钮
        key_visibility_frame = ttk.Frame(key_frame)
        key_visibility_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.show_key = tk.BooleanVar(value=False)
        ttk.Checkbutton(key_visibility_frame, text="显示密钥", variable=self.show_key, 
                       command=self.toggle_key_visibility).pack(anchor=tk.W)
        
        # 目录选择区域
        dir_frame = ttk.Frame(self.main_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(dir_frame, text="目标目录:").pack(anchor=tk.W)
        
        dir_help_frame = ttk.Frame(dir_frame)
        dir_help_frame.pack(fill=tk.X, pady=(2, 0))
        
        ttk.Label(dir_help_frame, text="包含 .enc 加密文件的目录", foreground="gray").pack(anchor=tk.W)
        
        dir_select_frame = ttk.Frame(dir_frame)
        dir_select_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.dir_entry = ttk.Entry(dir_select_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(dir_select_frame, text="浏览...", command=self.browse_directory).pack(side=tk.RIGHT, padx=(5, 0))
        
        # 文件统计区域
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(stats_frame, text="文件统计:").pack(anchor=tk.W)
        
        self.stats_label = ttk.Label(stats_frame, text="尚未扫描目录")
        self.stats_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 进度区域
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(progress_frame, text="进度:").pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(anchor=tk.E, pady=(2, 0))
        
        # 日志区域
        log_frame = ttk.Frame(self.main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        log_header_frame = ttk.Frame(log_frame)
        log_header_frame.pack(fill=tk.X)
        
        ttk.Label(log_header_frame, text="操作日志:").pack(side=tk.LEFT)
        
        # 添加清空日志按钮到标题栏
        ttk.Button(log_header_frame, text="清空日志", command=self.clear_log, width=10).pack(side=tk.RIGHT)
        
        self.log_text = tk.Text(log_frame, height=12, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # 按钮区域 - 确保按钮可见
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))  # 添加上边距
        
        # 使用更明显的按钮
        self.scan_button = ttk.Button(button_frame, text="扫描目录", command=self.scan_directory, width=12)
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.decrypt_button = ttk.Button(button_frame, text="开始解密", command=self.start_decryption, width=12)
        self.decrypt_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_decryption, width=12)
        self.stop_button.pack(side=tk.LEFT)
        
        # 添加状态栏
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        # 初始化变量
        self.decryption_thread = None
        self.stop_flag = False
        self.enc_files = []
        
        # 绑定目录变更事件
        self.dir_entry.bind("<KeyRelease>", self.on_directory_changed)
        
        # 确保窗口可见
        self.root.update()
        self.root.minsize(700, 600)  # 设置最小大小
        
    def toggle_key_visibility(self):
        if self.show_key.get():
            self.key_entry.config(show="")
        else:
            self.key_entry.config(show="*")
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.scan_directory()
    
    def on_directory_changed(self, event):
        # 目录变更后自动扫描
        self.scan_directory()
    
    def scan_directory(self):
        self.status_label.config(text="正在扫描目录...")
        target_dir = self.dir_entry.get().strip()
        if not target_dir:
            self.stats_label.config(text="尚未扫描目录")
            self.status_label.config(text="就绪")
            return
        
        if not os.path.exists(target_dir):
            self.stats_label.config(text="目录不存在")
            self.status_label.config(text="就绪")
            return
        
        # 扫描.enc文件
        self.enc_files = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith(".enc"):
                    full_path = os.path.join(root, file)
                    self.enc_files.append(full_path)
        
        self.stats_label.config(text=f"找到 {len(self.enc_files)} 个加密文件")
        self.log_message(f"扫描完成: 找到 {len(self.enc_files)} 个 .enc 文件")
        self.status_label.config(text="就绪")
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def decrypt_image(self, encrypted_path, hashed_key):
        """解密单个加密图片文件并移除.enc后缀"""
        try:
            # 检查文件是否有.enc后缀
            if not encrypted_path.endswith(".enc"):
                self.log_message(f"跳过: {encrypted_path} (不是.enc文件)")
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
            self.log_message(f"解密失败 {encrypted_path}: {str(e)}")
            return False
    
    def update_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.progress['value'] = percentage
        self.progress_label.config(text=f"{percentage}% ({current}/{total})")
    
    def decryption_worker(self):
        # 获取密钥
        key = self.key_entry.get().strip()
        if not key:
            self.log_message("错误: 请输入解密密钥")
            self.status_label.config(text="错误: 请输入解密密钥")
            return
        
        # 获取目录
        target_dir = self.dir_entry.get().strip()
        if not target_dir:
            self.log_message("错误: 请选择目标目录")
            self.status_label.config(text="错误: 请选择目标目录")
            return
        
        # 检查目录是否存在
        if not os.path.exists(target_dir):
            self.log_message(f"错误: 目录 '{target_dir}' 不存在")
            self.status_label.config(text=f"错误: 目录 '{target_dir}' 不存在")
            return
        
        # 如果没有扫描过文件，先扫描
        if not self.enc_files:
            self.scan_directory()
            if not self.enc_files:
                self.log_message("错误: 未找到任何 .enc 文件")
                self.status_label.config(text="错误: 未找到任何 .enc 文件")
                return
        
        # 生成密钥哈希
        hashed_key = hashlib.sha256(key.encode()).digest()
        
        self.log_message(f"开始解密，密钥: {key}")
        self.log_message(f"目标目录: {target_dir}")
        self.log_message(f"找到 {len(self.enc_files)} 个加密文件")
        self.log_message("-" * 50)
        self.status_label.config(text="正在解密...")
        
        # 重置停止标志
        self.stop_flag = False
        
        # 遍历目录并解密图片
        decrypted_count = 0
        failed_count = 0
        total_files = len(self.enc_files)
        
        for i, encrypted_path in enumerate(self.enc_files):
            if self.stop_flag:
                self.log_message("用户请求停止解密")
                self.status_label.config(text="解密已停止")
                break
                
            # 更新进度
            self.update_progress(i, total_files)
            
            if self.decrypt_image(encrypted_path, hashed_key):
                decrypted_count += 1
                original_name = encrypted_path[:-4]  # 移除.enc后缀
                self.log_message(f"✓ 已解密: {encrypted_path} -> {original_name}")
            else:
                failed_count += 1
        
        # 完成进度
        self.update_progress(total_files, total_files)
        
        self.log_message("-" * 50)
        self.log_message(f"解密完成!")
        self.log_message(f"成功解密: {decrypted_count} 个文件")
        self.log_message(f"解密失败: {failed_count} 个文件")
        self.status_label.config(text="解密完成")
        
        # 重新扫描目录
        self.scan_directory()
        
        # 启用按钮
        self.toggle_buttons(True)
    
    def start_decryption(self):
        # 禁用按钮，防止重复点击
        self.toggle_buttons(False)
        
        # 启动进度条
        self.progress['value'] = 0
        self.progress_label.config(text="0%")
        
        # 在新线程中执行解密操作
        self.decryption_thread = threading.Thread(target=self.decryption_worker)
        self.decryption_thread.daemon = True
        self.decryption_thread.start()
        
        # 检查线程状态
        self.check_thread()
    
    def stop_decryption(self):
        self.stop_flag = True
        self.log_message("正在停止解密操作...")
        self.status_label.config(text="正在停止...")
    
    def check_thread(self):
        if self.decryption_thread and self.decryption_thread.is_alive():
            self.root.after(100, self.check_thread)
        else:
            self.toggle_buttons(True)
    
    def toggle_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.scan_button.config(state=state)
        self.decrypt_button.config(state=state)
        # 停止按钮在解密过程中应该可用
        self.stop_button.config(state=tk.NORMAL if not enabled else tk.NORMAL)
    
    def on_closing(self):
        if self.decryption_thread and self.decryption_thread.is_alive():
            self.stop_flag = True
            self.log_message("正在停止解密操作...")
            self.root.after(100, self.on_closing)
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = DecryptorGUI(root)
    
    # 设置关闭窗口时的处理
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()