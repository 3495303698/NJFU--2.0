"""
网络通信模块
"""
import socket
import json
import threading
import struct
import os
from config import *

class NetworkProtocol:
    """网络协议处理类"""
    
    @staticmethod
    def send_data(sock, data_type, data):
        """发送数据（带类型和长度）"""
        try:
            message = {
                'type': data_type,
                'data': data
            }
            json_data = json.dumps(message, ensure_ascii=False).encode('utf-8')
            length = len(json_data)
            # 先发送长度（4字节）
            sock.sendall(struct.pack('!I', length))
            # 再发送数据
            sock.sendall(json_data)
            return True
        except Exception as e:
            print(f"发送数据失败: {e}")
            return False
    
    @staticmethod
    def receive_data(sock):
        """接收数据"""
        try:
            # 先接收长度（4字节）
            length_data = sock.recv(4)
            if len(length_data) < 4:
                return None, None
            length = struct.unpack('!I', length_data)[0]
            
            # 接收数据
            received = 0
            chunks = []
            while received < length:
                chunk = sock.recv(min(length - received, BUFFER_SIZE))
                if not chunk:
                    return None, None
                chunks.append(chunk)
                received += len(chunk)
            
            json_data = b''.join(chunks).decode('utf-8')
            message = json.loads(json_data)
            return message.get('type'), message.get('data')
        except Exception as e:
            print(f"接收数据失败: {e}")
            return None, None
    
    @staticmethod
    def send_image(sock, image_path):
        """发送图片文件"""
        try:
            if not os.path.exists(image_path):
                return False
            
            # 先发送文件信息
            file_size = os.path.getsize(image_path)
            file_name = os.path.basename(image_path)
            
            file_info = {
                'file_name': file_name,
                'file_size': file_size
            }
            
            # 发送文件信息
            if not NetworkProtocol.send_data(sock, MSG_TYPE_IMAGE, file_info):
                return False
            
            # 发送文件内容
            with open(image_path, 'rb') as f:
                sent = 0
                while sent < file_size:
                    chunk = f.read(IMAGE_BUFFER_SIZE)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    sent += len(chunk)
            
            return True
        except Exception as e:
            print(f"发送图片失败: {e}")
            return False
    
    @staticmethod
    def receive_image(sock, save_dir):
        """接收图片文件"""
        try:
            # 先接收文件信息
            msg_type, file_info = NetworkProtocol.receive_data(sock)
            if msg_type != MSG_TYPE_IMAGE or not file_info:
                return None
            
            file_name = file_info.get('file_name')
            file_size = file_info.get('file_size')
            
            if not file_name or not file_size:
                return None
            
            # 确保保存目录存在
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, file_name)
            
            # 接收文件内容
            received = 0
            with open(save_path, 'wb') as f:
                while received < file_size:
                    chunk = sock.recv(min(file_size - received, IMAGE_BUFFER_SIZE))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)
            
            if received == file_size:
                return save_path
            else:
                if os.path.exists(save_path):
                    os.remove(save_path)
                return None
        except Exception as e:
            print(f"接收图片失败: {e}")
            return None


class UDPBroadcaster:
    """UDP广播器（用于局域网发现）"""
    
    def __init__(self, username, port):
        self.username = username
        self.port = port
        self.running = False
        self.sock = None
        self.thread = None
    
    def start(self):
        """启动广播"""
        if self.running:
            return
        
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(1.0)
        
        self.thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """停止广播"""
        self.running = False
        if self.sock:
            self.sock.close()
    
    def _broadcast_loop(self):
        """广播循环"""
        broadcast_data = {
            'username': self.username,
            'port': self.port,
            'type': MSG_TYPE_BROADCAST
        }
        message = json.dumps(broadcast_data).encode('utf-8')
        
        while self.running:
            try:
                # 广播到局域网
                self.sock.sendto(message, ('255.255.255.255', BROADCAST_PORT))
            except Exception as e:
                print(f"广播失败: {e}")
            
            import time
            time.sleep(BROADCAST_INTERVAL)
    
    @staticmethod
    def listen_broadcast(callback, running_flag=None):
        """监听广播（静态方法）"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('', BROADCAST_PORT))
        except OSError:
            # 如果端口被占用，尝试使用其他端口
            try:
                sock.bind(('', BROADCAST_PORT + 1))
            except:
                sock.close()
                return
        
        sock.settimeout(1.0)
        
        discovered_users = set()
        
        while True:
            if running_flag is not None and not running_flag():
                break
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                if message.get('type') == MSG_TYPE_BROADCAST:
                    username = message.get('username')
                    port = message.get('port')
                    user_key = f"{username}_{addr[0]}_{port}"
                    
                    if user_key not in discovered_users:
                        discovered_users.add(user_key)
                        callback(username, addr[0], port)
            except socket.timeout:
                continue
            except Exception as e:
                if running_flag is None or running_flag():
                    print(f"监听广播失败: {e}")
                break
        
        sock.close()

