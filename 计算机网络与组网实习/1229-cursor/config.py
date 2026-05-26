"""
配置文件
"""
import socket

# 服务器配置
SERVER_HOST = '0.0.0.0'  # 服务器监听所有接口
SERVER_PORT = 8888

# UDP广播配置（局域网发现）
BROADCAST_PORT = 9999
BROADCAST_INTERVAL = 5  # 广播间隔（秒）

# 消息类型
MSG_TYPE_FRIEND_REQUEST = 'friend_request'
MSG_TYPE_FRIEND_RESPONSE = 'friend_response'
MSG_TYPE_MESSAGE = 'message'
MSG_TYPE_IMAGE = 'image'
MSG_TYPE_ONLINE = 'online'
MSG_TYPE_OFFLINE = 'offline'
MSG_TYPE_BROADCAST = 'broadcast'
MSG_TYPE_REGISTER = 'register'
MSG_TYPE_LOGIN = 'login'
MSG_TYPE_USER_INFO = 'user_info'

# 数据目录
DATA_DIR = 'chat_data'
CONTACTS_FILE = f'{DATA_DIR}/contacts.json'
MESSAGES_DIR = f'{DATA_DIR}/messages'

# 缓冲区大小
BUFFER_SIZE = 4096
IMAGE_BUFFER_SIZE = 65536

