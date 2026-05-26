"""
服务器端
"""
import socket
import threading
import json
import os
from config import *
from network import NetworkProtocol

class ChatServer:
    """聊天服务器"""
    
    def __init__(self):
        self.sock = None
        self.clients = {}  # {username: {'sock': socket, 'addr': addr, 'ip': ip, 'port': port}}
        self.user_info = {}  # {username: {'ip': ip, 'port': port, 'password': password}}
        self.running = False
        self._load_user_info()
    
    def _load_user_info(self):
        """加载用户信息"""
        user_file = f'{DATA_DIR}/users.json'
        if os.path.exists(user_file):
            try:
                with open(user_file, 'r', encoding='utf-8') as f:
                    self.user_info = json.load(f)
            except Exception as e:
                print(f"加载用户信息失败: {e}")
                self.user_info = {}
    
    def _save_user_info(self):
        """保存用户信息"""
        os.makedirs(DATA_DIR, exist_ok=True)
        user_file = f'{DATA_DIR}/users.json'
        try:
            with open(user_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_info, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存用户信息失败: {e}")
    
    def start(self):
        """启动服务器"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((SERVER_HOST, SERVER_PORT))
        self.sock.listen(10)
        self.running = True
        
        print(f"服务器启动，监听 {SERVER_HOST}:{SERVER_PORT}")
        
        while self.running:
            try:
                client_sock, addr = self.sock.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, addr),
                    daemon=True
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"接受连接失败: {e}")
    
    def stop(self):
        """停止服务器"""
        self.running = False
        if self.sock:
            self.sock.close()
        for username, client in list(self.clients.items()):
            if client['sock']:
                client['sock'].close()
    
    def _handle_client(self, client_sock, addr):
        """处理客户端连接"""
        username = None
        try:
            while True:
                msg_type, data = NetworkProtocol.receive_data(client_sock)
                if not msg_type:
                    break
                
                if msg_type == MSG_TYPE_REGISTER:
                    # 注册
                    username = data.get('username')
                    password = data.get('password')
                    if username and password:
                        if username not in self.user_info:
                            self.user_info[username] = {
                                'password': password,
                                'ip': addr[0],
                                'port': data.get('port', 0)
                            }
                            self._save_user_info()
                            NetworkProtocol.send_data(
                                client_sock, 
                                'register_response', 
                                {'success': True, 'message': '注册成功'}
                            )
                        else:
                            NetworkProtocol.send_data(
                                client_sock,
                                'register_response',
                                {'success': False, 'message': '用户名已存在'}
                            )
                
                elif msg_type == MSG_TYPE_LOGIN:
                    # 登录
                    username = data.get('username')
                    password = data.get('password')
                    client_port = data.get('port', 0)
                    
                    if username in self.user_info:
                        if self.user_info[username]['password'] == password:
                            # 登录成功
                            self.clients[username] = {
                                'sock': client_sock,
                                'addr': addr,
                                'ip': addr[0],
                                'port': client_port
                            }
                            self.user_info[username]['ip'] = addr[0]
                            self.user_info[username]['port'] = client_port
                            self._save_user_info()
                            
                            NetworkProtocol.send_data(
                                client_sock,
                                'login_response',
                                {'success': True, 'message': '登录成功'}
                            )
                            
                            # 通知其他用户
                            self._notify_user_status(username, 'online')
                        else:
                            NetworkProtocol.send_data(
                                client_sock,
                                'login_response',
                                {'success': False, 'message': '密码错误'}
                            )
                    else:
                        NetworkProtocol.send_data(
                            client_sock,
                            'login_response',
                            {'success': False, 'message': '用户不存在'}
                        )
                
                elif msg_type == MSG_TYPE_USER_INFO:
                    # 查询用户信息
                    query_username = data.get('username')
                    if query_username in self.user_info:
                        user_info = self.user_info[query_username].copy()
                        user_info.pop('password', None)  # 不发送密码
                        user_info['online'] = query_username in self.clients
                        NetworkProtocol.send_data(
                            client_sock,
                            'user_info_response',
                            {'success': True, 'user_info': user_info}
                        )
                    else:
                        NetworkProtocol.send_data(
                            client_sock,
                            'user_info_response',
                            {'success': False, 'message': '用户不存在'}
                        )
                
                elif msg_type == MSG_TYPE_FRIEND_REQUEST:
                    # 好友请求
                    from_user = data.get('from_user')
                    to_user = data.get('to_user')
                    message = data.get('message', '')
                    
                    if to_user in self.clients:
                        # 转发好友请求
                        to_sock = self.clients[to_user]['sock']
                        NetworkProtocol.send_data(
                            to_sock,
                            MSG_TYPE_FRIEND_REQUEST,
                            {
                                'from_user': from_user,
                                'to_user': to_user,
                                'message': message
                            }
                        )
                    else:
                        # 用户不在线，通知请求者
                        NetworkProtocol.send_data(
                            client_sock,
                            'friend_request_response',
                            {'success': False, 'message': '用户不在线'}
                        )
                
                elif msg_type == MSG_TYPE_FRIEND_RESPONSE:
                    # 好友响应
                    from_user = data.get('from_user')
                    to_user = data.get('to_user')
                    accepted = data.get('accepted', False)
                    
                    if to_user in self.clients:
                        to_sock = self.clients[to_user]['sock']
                        NetworkProtocol.send_data(
                            to_sock,
                            MSG_TYPE_FRIEND_RESPONSE,
                            {
                                'from_user': from_user,
                                'to_user': to_user,
                                'accepted': accepted
                            }
                        )
                
                elif msg_type == MSG_TYPE_MESSAGE:
                    # 消息转发
                    from_user = data.get('from_user')
                    to_user = data.get('to_user')
                    message = data.get('message', '')
                    
                    if to_user in self.clients:
                        to_sock = self.clients[to_user]['sock']
                        NetworkProtocol.send_data(
                            to_sock,
                            MSG_TYPE_MESSAGE,
                            {
                                'from_user': from_user,
                                'to_user': to_user,
                                'message': message,
                                'timestamp': data.get('timestamp')
                            }
                        )
                        # 通知发送者消息已送达
                        NetworkProtocol.send_data(
                            client_sock,
                            'message_sent',
                            {'success': True, 'to_user': to_user}
                        )
                    else:
                        # 用户不在线
                        NetworkProtocol.send_data(
                            client_sock,
                            'message_sent',
                            {'success': False, 'message': '用户不在线', 'to_user': to_user}
                        )
                
                elif msg_type == MSG_TYPE_IMAGE:
                    # 图片转发
                    from_user = data.get('from_user')
                    to_user = data.get('to_user')
                    
                    if to_user in self.clients:
                        to_sock = self.clients[to_user]['sock']
                        # 先转发图片信息
                        NetworkProtocol.send_data(
                            to_sock,
                            MSG_TYPE_IMAGE,
                            {
                                'from_user': from_user,
                                'to_user': to_user,
                                'timestamp': data.get('timestamp')
                            }
                        )
                        # 然后转发图片文件（这里简化处理，实际应该先接收完整图片再转发）
                        # 为了简化，我们通知客户端直接P2P传输
                        NetworkProtocol.send_data(
                            client_sock,
                            'image_sent',
                            {'success': True, 'to_user': to_user, 'direct': True}
                        )
                    else:
                        NetworkProtocol.send_data(
                            client_sock,
                            'image_sent',
                            {'success': False, 'message': '用户不在线', 'to_user': to_user}
                        )
        
        except Exception as e:
            print(f"处理客户端错误: {e}")
        finally:
            if username and username in self.clients:
                del self.clients[username]
                self._notify_user_status(username, 'offline')
            client_sock.close()
    
    def _notify_user_status(self, username, status):
        """通知其他用户状态变化"""
        for other_username, client in list(self.clients.items()):
            if other_username != username:
                try:
                    NetworkProtocol.send_data(
                        client['sock'],
                        'user_status',
                        {'username': username, 'status': status}
                    )
                except:
                    pass


if __name__ == '__main__':
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n服务器关闭中...")
        server.stop()

