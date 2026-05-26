"""
客户端GUI
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import socket
import threading
import json
import os
from datetime import datetime
from config import *
from network import NetworkProtocol, UDPBroadcaster
from contacts import ContactsManager

# 尝试导入图片和视频处理库
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("警告: PIL/Pillow未安装，图片预览功能将不可用")

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("警告: OpenCV未安装，视频预览功能将不可用")

class ChatClient:
    """聊天客户端"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("简易聊天系统")
        self.root.geometry("800x600")
        
        self.username = None
        self.server_sock = None
        self.server_thread = None
        self.server_connected = False
        self.client_port = 7777  # 客户端监听端口
        self.client_sock = None
        self.contacts_manager = ContactsManager()
        self.broadcaster = None
        self.discovered_users = {}  # {username: {'ip': ip, 'port': port}}
        
        self.current_chat_user = None
        self.chat_windows = {}  # {username: chat_window}
        self.lan_discovery_running = False  # 初始化局域网发现标志
        
        self._create_login_ui()
        self._setup_client_server()
    
    def _create_login_ui(self):
        """创建登录界面"""
        # 清除现有组件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill='both')
        
        title_label = ttk.Label(frame, text="简易聊天系统", font=('Arial', 20, 'bold'))
        title_label.pack(pady=20)
        
        # 用户名
        ttk.Label(frame, text="用户名:").pack(pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack(pady=5)
        
        # 密码
        ttk.Label(frame, text="密码:").pack(pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show='*')
        self.password_entry.pack(pady=5)
        
        # 服务器地址
        ttk.Label(frame, text="服务器地址:").pack(pady=5)
        self.server_entry = ttk.Entry(frame, width=30)
        self.server_entry.insert(0, "10.14.76.123")
        self.server_entry.pack(pady=5)
        
        # 按钮框架
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="登录", command=self._login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="注册", command=self._register).pack(side=tk.LEFT, padx=5)
    
    def _setup_client_server(self):
        """设置客户端服务器（用于接收消息）"""
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_sock.bind(('0.0.0.0', self.client_port))
            self.client_sock.listen(5)
            
            # 启动接收线程
            thread = threading.Thread(target=self._accept_connections, daemon=True)
            thread.start()
        except Exception as e:
            print(f"设置客户端服务器失败: {e}")
    
    def _accept_connections(self):
        """接受连接（用于临时会话）"""
        while True:
            try:
                sock, addr = self.client_sock.accept()
                thread = threading.Thread(
                    target=self._handle_direct_connection,
                    args=(sock, addr),
                    daemon=True
                )
                thread.start()
            except:
                break
    
    def _handle_direct_connection(self, sock, addr):
        """处理直接连接（临时会话）"""
        from_user = None
        try:
            # 首先接收发送者信息
            msg_type, data = NetworkProtocol.receive_data(sock)
            if msg_type == 'sender_info':
                from_user = data.get('from_user', f"用户_{addr[0]}")
            else:
                # 如果没有发送者信息，使用消息中的from_user
                from_user = data.get('from_user', f"用户_{addr[0]}")
                # 处理第一条消息
                if msg_type == MSG_TYPE_MESSAGE:
                    message = data.get('message')
                    if from_user:
                        self.root.after(0, self._show_message, from_user, message, False)
                elif msg_type == MSG_TYPE_IMAGE:
                    # 接收图片
                    save_dir = f'{DATA_DIR}/received_images'
                    image_path = NetworkProtocol.receive_image(sock, save_dir)
                    if image_path:
                        self.root.after(0, self._show_image, from_user, image_path)
            
            # 继续接收后续消息
            if msg_type == 'sender_info':
                while True:
                    msg_type, data = NetworkProtocol.receive_data(sock)
                    if not msg_type:
                        break
                    
                    if msg_type == MSG_TYPE_MESSAGE:
                        message = data.get('message')
                        if from_user:
                            self.root.after(0, self._show_message, from_user, message, False)
                    
                    elif msg_type == MSG_TYPE_IMAGE:
                        # 接收图片
                        save_dir = f'{DATA_DIR}/received_images'
                        image_path = NetworkProtocol.receive_image(sock, save_dir)
                        if image_path:
                            # 尝试接收附加信息
                            try:
                                info_type, info_data = NetworkProtocol.receive_data(sock)
                                if info_type == 'image_info':
                                    img_from_user = info_data.get('from_user', from_user)
                                else:
                                    img_from_user = from_user
                            except:
                                img_from_user = from_user
                            
                            self.root.after(0, self._show_image, img_from_user, image_path)
        except Exception as e:
            print(f"处理直接连接错误: {e}")
        finally:
            sock.close()
    
    def _connect_server(self, server_ip, show_error=True):
        """连接服务器"""
        try:
            # 处理可能包含端口号的服务器地址
            if ':' in server_ip:
                server_ip, _ = server_ip.split(':', 1)
            
            print(f"正在连接到服务器: {server_ip}:{SERVER_PORT}")  # 调试信息
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.settimeout(5.0)  # 设置连接超时
            self.server_sock.connect((server_ip, SERVER_PORT))
            self.server_sock.settimeout(None)  # 取消超时
            self.server_connected = True
            print(f"成功连接到服务器: {server_ip}:{SERVER_PORT}")  # 调试信息
            
            # 启动服务器消息接收线程
            self.server_thread = threading.Thread(target=self._receive_server_messages, daemon=True)
            self.server_thread.start()
            return True
        except Exception as e:
            error_msg = f"连接服务器失败: {e}"
            print(error_msg)  # 调试信息
            if show_error:
                # 如果在GUI线程中调用，直接显示错误
                # 如果在后台线程中调用，需要通过root.after显示
                try:
                    messagebox.showerror("错误", error_msg)
                except:
                    self.root.after(0, messagebox.showerror, "错误", error_msg)
            return False
    
    def _receive_server_messages(self):
        """接收服务器消息"""
        while self.server_connected:
            try:
                msg_type, data = NetworkProtocol.receive_data(self.server_sock)
                if not msg_type:
                    break
                
                if msg_type == MSG_TYPE_FRIEND_REQUEST:
                    # 收到好友请求
                    from_user = data.get('from_user')
                    message = data.get('message', '')
                    self.root.after(0, self._handle_friend_request, from_user, message)
                
                elif msg_type == MSG_TYPE_FRIEND_RESPONSE:
                    # 收到好友响应
                    from_user = data.get('from_user')
                    accepted = data.get('accepted', False)
                    self.root.after(0, self._handle_friend_response, from_user, accepted)
                
                elif msg_type == MSG_TYPE_MESSAGE:
                    # 收到消息
                    from_user = data.get('from_user')
                    message = data.get('message')
                    self.root.after(0, self._show_message, from_user, message, True)
                
                elif msg_type == 'message_sent':
                    # 消息发送结果
                    success = data.get('success')
                    if not success:
                        message = data.get('message', '发送失败')
                        to_user = data.get('to_user')
                        self.root.after(0, messagebox.showerror, "发送失败", f"向 {to_user} 发送消息失败: {message}")
                
                elif msg_type == 'user_status':
                    # 用户状态变化
                    username = data.get('username')
                    status = data.get('status')
                    self.root.after(0, self._update_contact_status, username, status)
                    
            except Exception as e:
                if self.server_connected:
                    print(f"接收服务器消息错误: {e}")
                break
    
    def _register(self):
        """注册"""
        print("注册按钮被点击")  # 调试信息
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        server_ip = self.server_entry.get().strip()
        
        print(f"注册信息 - 用户名: {username}, 服务器: {server_ip}")  # 调试信息
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        if not server_ip:
            messagebox.showerror("错误", "请输入服务器地址")
            return
        
        # 在单独的线程中执行注册，避免阻塞GUI
        def register_thread():
            try:
                print(f"注册线程启动，服务器地址: {server_ip}")  # 调试信息
                if not self._connect_server(server_ip, show_error=False):
                    self.root.after(0, messagebox.showerror, "错误", f"连接服务器失败，请检查服务器地址是否正确：{server_ip}")
                    return
                
                # 发送注册请求
                NetworkProtocol.send_data(
                    self.server_sock,
                    MSG_TYPE_REGISTER,
                    {
                        'username': username,
                        'password': password,
                        'port': self.client_port
                    }
                )
                
                # 接收响应
                msg_type, data = NetworkProtocol.receive_data(self.server_sock)
                if msg_type == 'register_response':
                    if data.get('success'):
                        self.root.after(0, messagebox.showinfo, "成功", "注册成功，请登录")
                    else:
                        self.root.after(0, messagebox.showerror, "错误", data.get('message', '注册失败'))
                else:
                    self.root.after(0, messagebox.showerror, "错误", "注册失败：服务器响应异常")
                
                self.server_sock.close()
                self.server_connected = False
            except Exception as e:
                self.root.after(0, messagebox.showerror, "错误", f"注册失败：{str(e)}")
                if self.server_sock:
                    try:
                        self.server_sock.close()
                    except:
                        pass
                self.server_connected = False
        
        threading.Thread(target=register_thread, daemon=True).start()
    
    def _login(self):
        """登录"""
        print("登录按钮被点击")  # 调试信息
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        server_ip = self.server_entry.get().strip()
        
        print(f"登录信息 - 用户名: {username}, 服务器: {server_ip}")  # 调试信息
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        if not server_ip:
            messagebox.showerror("错误", "请输入服务器地址")
            return
        
        # 在单独的线程中执行登录，避免阻塞GUI
        def login_thread():
            try:
                print(f"登录线程启动，服务器地址: {server_ip}")  # 调试信息
                if not self._connect_server(server_ip, show_error=False):
                    self.root.after(0, messagebox.showerror, "错误", f"连接服务器失败，请检查服务器地址是否正确：{server_ip}")
                    return
                
                # 发送登录请求
                NetworkProtocol.send_data(
                    self.server_sock,
                    MSG_TYPE_LOGIN,
                    {
                        'username': username,
                        'password': password,
                        'port': self.client_port
                    }
                )
                
                # 接收响应
                msg_type, data = NetworkProtocol.receive_data(self.server_sock)
                print(f"登录响应: msg_type={msg_type}, data={data}")  # 调试信息
                
                if msg_type == 'login_response':
                    if data and data.get('success'):
                        self.username = username
                        # 在主线程中创建主界面
                        self.root.after(0, lambda: self._create_main_ui())
                        # 启动局域网广播
                        self.broadcaster = UDPBroadcaster(username, self.client_port)
                        self.broadcaster.start()
                        # 启动局域网发现监听
                        self._start_lan_discovery()
                    else:
                        error_msg = data.get('message', '登录失败') if data else '登录失败：服务器返回空数据'
                        self.root.after(0, messagebox.showerror, "错误", error_msg)
                        if self.server_sock:
                            self.server_sock.close()
                        self.server_connected = False
                else:
                    error_detail = f"服务器响应类型: {msg_type}" if msg_type else "服务器无响应"
                    self.root.after(0, messagebox.showerror, "错误", f"登录失败：{error_detail}")
                    if self.server_sock:
                        self.server_sock.close()
                    self.server_connected = False
            except Exception as e:
                import traceback
                traceback.print_exc()  # 打印完整错误信息
                self.root.after(0, messagebox.showerror, "错误", f"登录失败：{str(e)}")
                if self.server_sock:
                    try:
                        self.server_sock.close()
                    except:
                        pass
                self.server_connected = False
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def _start_lan_discovery(self):
        """启动局域网发现"""
        self.lan_discovery_running = True
        
        def on_discovered(username, ip, port):
            if username != self.username:
                self.discovered_users[username] = {'ip': ip, 'port': port}
                self.root.after(0, self._update_discovered_users)
        
        def should_run():
            return getattr(self, 'lan_discovery_running', False)
        
        thread = threading.Thread(
            target=UDPBroadcaster.listen_broadcast,
            args=(on_discovered, should_run),
            daemon=True
        )
        thread.start()
    
    def _update_discovered_users(self):
        """更新发现的用户列表"""
        # 在主界面中更新
        if hasattr(self, 'discovered_listbox'):
            self.discovered_listbox.delete(0, tk.END)
            for username in sorted(self.discovered_users.keys()):
                self.discovered_listbox.insert(tk.END, username)
    
    def _create_main_ui(self):
        """创建主界面"""
        # 清除现有组件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧：通讯录
        left_frame = ttk.Frame(main_frame, width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # 标题
        title_label = ttk.Label(left_frame, text=f"用户: {self.username}", font=('Arial', 12, 'bold'))
        title_label.pack(pady=10)
        
        # 添加好友按钮
        ttk.Button(left_frame, text="添加好友", command=self._show_add_friend_dialog).pack(pady=5)
        
        # 通讯录列表
        ttk.Label(left_frame, text="通讯录:", font=('Arial', 10)).pack(pady=(10, 5))
        contacts_frame = ttk.Frame(left_frame)
        contacts_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar1 = ttk.Scrollbar(contacts_frame)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contacts_listbox = tk.Listbox(contacts_frame, yscrollcommand=scrollbar1.set)
        self.contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.config(command=self.contacts_listbox.yview)
        self.contacts_listbox.bind('<Double-Button-1>', self._open_chat)
        
        # 局域网发现
        ttk.Label(left_frame, text="局域网用户:", font=('Arial', 10)).pack(pady=(10, 5))
        discovered_frame = ttk.Frame(left_frame)
        discovered_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar2 = ttk.Scrollbar(discovered_frame)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.discovered_listbox = tk.Listbox(discovered_frame, yscrollcommand=scrollbar2.set)
        self.discovered_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.config(command=self.discovered_listbox.yview)
        self.discovered_listbox.bind('<Double-Button-1>', self._start_temp_chat)
        
        # 右侧：聊天区域（初始为空）
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.chat_frame = right_frame
        
        # 菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 更新通讯录列表
        self._update_contacts_list()
        self._update_discovered_users()
    
    def _update_contacts_list(self):
        """更新通讯录列表"""
        self.contacts_listbox.delete(0, tk.END)
        contacts = self.contacts_manager.get_sorted_contacts()
        for contact in contacts:
            status = "●" if contact.get('status') == 'online' else "○"
            display_name = f"{status} {contact['username']}"
            self.contacts_listbox.insert(tk.END, display_name)
    
    def _show_add_friend_dialog(self):
        """显示添加好友对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加好友")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="用户名:").pack(pady=5)
        username_entry = ttk.Entry(frame, width=30)
        username_entry.pack(pady=5)
        
        ttk.Label(frame, text="验证信息:").pack(pady=5)
        message_entry = ttk.Entry(frame, width=30)
        message_entry.pack(pady=5)
        message_entry.insert(0, f"我是 {self.username}，想添加您为好友")
        
        def add_friend():
            target_username = username_entry.get().strip()
            verify_message = message_entry.get().strip()
            
            if not target_username:
                messagebox.showerror("错误", "请输入用户名")
                return
            
            if target_username == self.username:
                messagebox.showerror("错误", "不能添加自己为好友")
                return
            
            if self.contacts_manager.contact_exists(target_username):
                messagebox.showerror("错误", "该用户已在通讯录中")
                return
            
            # 查询用户信息
            NetworkProtocol.send_data(
                self.server_sock,
                MSG_TYPE_USER_INFO,
                {'username': target_username}
            )
            
            # 接收响应
            msg_type, data = NetworkProtocol.receive_data(self.server_sock)
            if msg_type == 'user_info_response' and data.get('success'):
                user_info = data.get('user_info')
                # 发送好友请求
                NetworkProtocol.send_data(
                    self.server_sock,
                    MSG_TYPE_FRIEND_REQUEST,
                    {
                        'from_user': self.username,
                        'to_user': target_username,
                        'message': verify_message
                    }
                )
                messagebox.showinfo("提示", "好友请求已发送，等待对方确认")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "用户不存在")
        
        ttk.Button(frame, text="发送请求", command=add_friend).pack(pady=10)
        ttk.Button(frame, text="取消", command=dialog.destroy).pack()
    
    def _handle_friend_request(self, from_user, message):
        """处理好友请求"""
        result = messagebox.askyesno(
            "好友请求",
            f"{from_user} 请求添加您为好友\n验证信息: {message}\n\n是否同意？"
        )
        
        # 发送响应
        NetworkProtocol.send_data(
            self.server_sock,
            MSG_TYPE_FRIEND_RESPONSE,
            {
                'from_user': self.username,
                'to_user': from_user,
                'accepted': result
            }
        )
    
    def _handle_friend_response(self, from_user, accepted):
        """处理好友响应"""
        if accepted:
            messagebox.showinfo("成功", f"{from_user} 已同意您的好友请求")
            # 查询用户信息并添加到通讯录
            NetworkProtocol.send_data(
                self.server_sock,
                MSG_TYPE_USER_INFO,
                {'username': from_user}
            )
            
            msg_type, data = NetworkProtocol.receive_data(self.server_sock)
            if msg_type == 'user_info_response' and data.get('success'):
                user_info = data.get('user_info')
                self.contacts_manager.add_contact(
                    from_user,
                    user_info.get('ip', ''),
                    user_info.get('port', 0),
                    'online'
                )
                self._update_contacts_list()
        else:
            messagebox.showinfo("提示", f"{from_user} 拒绝了您的好友请求")
    
    def _update_contact_status(self, username, status):
        """更新联系人状态"""
        self.contacts_manager.update_contact_status(username, status)
        self._update_contacts_list()
    
    def _open_chat(self, event):
        """打开聊天窗口"""
        selection = self.contacts_listbox.curselection()
        if not selection:
            return
        
        item = self.contacts_listbox.get(selection[0])
        # 提取用户名（去除状态符号）
        username = item.split(' ', 1)[1] if ' ' in item else item
        
        if username not in self.chat_windows:
            self._create_chat_window(username)
        else:
            self.chat_windows[username].lift()
    
    def _start_temp_chat(self, event):
        """开始临时会话（局域网）"""
        selection = self.discovered_listbox.curselection()
        if not selection:
            return
        
        username = self.discovered_listbox.get(selection[0])
        user_info = self.discovered_users.get(username)
        
        if not user_info:
            return
        
        # 创建临时聊天窗口
        if username not in self.chat_windows:
            self._create_chat_window(username, temp=True, ip=user_info['ip'], port=user_info['port'])
        else:
            self.chat_windows[username].lift()
    
    def _create_chat_window(self, username, temp=False, ip=None, port=None):
        """创建聊天窗口"""
        chat_window = tk.Toplevel(self.root)
        chat_window.title(f"与 {username} 的对话")
        chat_window.geometry("600x500")
        
        # 存储窗口信息
        self.chat_windows[username] = chat_window
        chat_window.is_temp = temp
        chat_window.direct_ip = ip
        chat_window.direct_port = port
        
        # 聊天消息区域
        messages_frame = ttk.Frame(chat_window)
        messages_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(messages_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        messages_text = scrolledtext.ScrolledText(
            messages_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED
        )
        messages_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=messages_text.yview)
        
        chat_window.messages_text = messages_text
        
        # 输入区域
        input_frame = ttk.Frame(chat_window)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        message_entry = ttk.Entry(input_frame)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        def send_message():
            message = message_entry.get().strip()
            if message:
                self._send_message(username, message, temp=temp, ip=ip, port=port)
                message_entry.delete(0, tk.END)
        
        def send_file():
            file_path = filedialog.askopenfilename(
                title="选择图片或视频",
                filetypes=[
                    ("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                    ("视频文件", "*.mp4 *.avi *.mov *.wmv *.flv *.mkv"),
                    ("所有支持的文件", "*.jpg *.jpeg *.png *.gif *.bmp *.webp *.mp4 *.avi *.mov *.wmv *.flv *.mkv"),
                    ("所有文件", "*.*")
                ]
            )
            if file_path:
                self._send_image(username, file_path, temp=temp, ip=ip, port=port)
        
        ttk.Button(input_frame, text="发送", command=send_message).pack(side=tk.LEFT, padx=2)
        ttk.Button(input_frame, text="图片/视频", command=send_file).pack(side=tk.LEFT, padx=2)
        
        message_entry.bind('<Return>', lambda e: send_message())
        
        def on_closing():
            if username in self.chat_windows:
                del self.chat_windows[username]
            chat_window.destroy()
        
        chat_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    def _send_message(self, to_user, message, temp=False, ip=None, port=None):
        """发送消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if temp and ip and port:
            # 临时会话，直接连接
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5.0)  # 设置超时
                sock.connect((ip, port))
                # 先发送发送者信息（便于接收方识别）
                NetworkProtocol.send_data(
                    sock,
                    'sender_info',
                    {'from_user': self.username}
                )
                # 发送消息
                NetworkProtocol.send_data(
                    sock,
                    MSG_TYPE_MESSAGE,
                    {
                        'from_user': self.username,
                        'to_user': to_user,
                        'message': message,
                        'timestamp': timestamp
                    }
                )
                sock.close()
                # 显示消息
                self._show_message_in_window(to_user, f"[我] {timestamp}\n{message}\n\n")
            except socket.timeout:
                messagebox.showerror("错误", f"连接超时，无法发送消息给 {to_user}")
            except Exception as e:
                messagebox.showerror("错误", f"发送消息失败: {e}")
        else:
            # 通过服务器发送
            NetworkProtocol.send_data(
                self.server_sock,
                MSG_TYPE_MESSAGE,
                {
                    'from_user': self.username,
                    'to_user': to_user,
                    'message': message,
                    'timestamp': timestamp
                }
            )
            # 显示消息
            self._show_message_in_window(to_user, f"[我] {timestamp}\n{message}\n\n")
    
    def _send_image(self, to_user, image_path, temp=False, ip=None, port=None):
        """发送图片"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if temp and ip and port:
            # 临时会话，直接连接
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                
                # 先发送发送者信息
                NetworkProtocol.send_data(
                    sock,
                    'sender_info',
                    {'from_user': self.username}
                )
                # 发送图片文件（send_image会处理完整的发送流程）
                if NetworkProtocol.send_image(sock, image_path):
                    # 发送图片后的附加信息
                    try:
                        NetworkProtocol.send_data(
                            sock,
                            'image_info',
                            {
                                'from_user': self.username,
                                'to_user': to_user,
                                'timestamp': timestamp
                            }
                        )
                    except:
                        pass  # 如果发送附加信息失败，不影响图片已发送的事实
                    
                    # 显示发送的图片/视频预览
                    file_type = self._get_file_type(image_path)
                    type_label = "图片" if file_type == 'image' else "视频"
                    header = f"[我] {timestamp}\n[{type_label}: {os.path.basename(image_path)}]\n"
                    self._show_message_in_window(to_user, header, file_path=image_path)
                else:
                    messagebox.showerror("错误", "发送图片失败")
                
                sock.close()
            except Exception as e:
                messagebox.showerror("错误", f"发送图片失败: {e}")
        else:
            # 通过服务器发送（简化处理，实际应该先上传到服务器）
            messagebox.showinfo("提示", "服务器转发图片功能暂未实现，请使用临时会话发送图片")
    
    def _show_message(self, from_user, message, from_server=False):
        """显示消息"""
        if from_user not in self.chat_windows:
            # 如果聊天窗口未打开，创建它
            contact = self.contacts_manager.get_contact(from_user)
            if contact:
                self._create_chat_window(from_user)
            else:
                # 临时会话
                if from_user in self.discovered_users:
                    user_info = self.discovered_users[from_user]
                    self._create_chat_window(from_user, temp=True, ip=user_info['ip'], port=user_info['port'])
                else:
                    return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._show_message_in_window(from_user, f"[{from_user}] {timestamp}\n{message}\n\n")
    
    def _get_file_type(self, file_path):
        """判断文件类型（图片或视频）"""
        ext = os.path.splitext(file_path)[1].lower()
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        video_exts = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
        
        if ext in image_exts:
            return 'image'
        elif ext in video_exts:
            return 'video'
        return 'unknown'
    
    def _create_thumbnail(self, file_path, max_size=(300, 300)):
        """创建图片或视频的缩略图"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return None
        
        file_type = self._get_file_type(file_path)
        
        if file_type == 'image' and PIL_AVAILABLE:
            try:
                img = Image.open(file_path)
                # 如果是GIF动画，只取第一帧
                if hasattr(img, 'is_animated') and img.is_animated:
                    img.seek(0)
                # 兼容新旧版本的PIL
                try:
                    resampling = Image.Resampling.LANCZOS
                except AttributeError:
                    resampling = Image.LANCZOS
                img.thumbnail(max_size, resampling)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"创建图片缩略图失败: {e}")
                return None
        elif file_type == 'video' and CV2_AVAILABLE and PIL_AVAILABLE:
            try:
                cap = cv2.VideoCapture(file_path)
                ret, frame = cap.read()
                cap.release()
                
                if ret:
                    # 将BGR转换为RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    # 兼容新旧版本的PIL
                    try:
                        resampling = Image.Resampling.LANCZOS
                    except AttributeError:
                        resampling = Image.LANCZOS
                    img.thumbnail(max_size, resampling)
                    return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"创建视频缩略图失败: {e}")
                return None
        
        return None
    
    def _show_image(self, from_user, image_path):
        """显示图片或视频（带预览）"""
        if from_user not in self.chat_windows:
            self._create_chat_window(from_user)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_type = self._get_file_type(image_path)
        file_name = os.path.basename(image_path)
        
        # 判断是图片还是视频
        type_label = "图片" if file_type == 'image' else "视频"
        
        # 显示消息头
        if from_user in self.chat_windows:
            chat_window = self.chat_windows[from_user]
            messages_text = chat_window.messages_text
            messages_text.config(state=tk.NORMAL)
            
            # 插入时间戳和用户信息
            header = f"[{from_user}] {timestamp}\n[{type_label}: {file_name}]\n"
            messages_text.insert(tk.END, header)
            
            # 尝试创建并插入缩略图
            thumbnail = self._create_thumbnail(image_path)
            if thumbnail:
                # 存储PhotoImage引用以防止被垃圾回收
                if not hasattr(chat_window, '_image_refs'):
                    chat_window._image_refs = []
                chat_window._image_refs.append(thumbnail)
                
                # 在Text widget中插入图片
                messages_text.image_create(tk.END, image=thumbnail)
                messages_text.insert(tk.END, "\n")
            else:
                # 如果无法创建缩略图，显示文件路径提示
                messages_text.insert(tk.END, f"[预览不可用，文件路径: {image_path}]\n")
            
            messages_text.insert(tk.END, "\n")
            messages_text.see(tk.END)
            messages_text.config(state=tk.DISABLED)
    
    def _show_message_in_window(self, username, message, file_path=None):
        """在聊天窗口中显示消息（可选：显示文件预览）"""
        if username in self.chat_windows:
            chat_window = self.chat_windows[username]
            messages_text = chat_window.messages_text
            messages_text.config(state=tk.NORMAL)
            
            # 如果有文件路径，尝试显示预览
            if file_path and os.path.exists(file_path):
                # 先插入文本消息
                messages_text.insert(tk.END, message)
                
                # 创建并插入缩略图
                thumbnail = self._create_thumbnail(file_path)
                if thumbnail:
                    # 存储PhotoImage引用以防止被垃圾回收
                    if not hasattr(chat_window, '_image_refs'):
                        chat_window._image_refs = []
                    chat_window._image_refs.append(thumbnail)
                    
                    # 插入换行和图片
                    messages_text.insert(tk.END, "\n")
                    messages_text.image_create(tk.END, image=thumbnail)
                    messages_text.insert(tk.END, "\n")
            else:
                # 普通文本消息
                messages_text.insert(tk.END, message)
            
            messages_text.see(tk.END)
            messages_text.config(state=tk.DISABLED)
    
    def run(self):
        """运行客户端"""
        self.root.mainloop()
        # 清理资源
        self.lan_discovery_running = False
        if self.server_connected and self.server_sock:
            self.server_sock.close()
        if self.broadcaster:
            self.broadcaster.stop()
        if self.client_sock:
            self.client_sock.close()


if __name__ == '__main__':
    # 创建数据目录
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(f'{DATA_DIR}/received_images', exist_ok=True)
    
    client = ChatClient()
    client.run()

