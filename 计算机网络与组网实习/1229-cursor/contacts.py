"""
通讯录管理模块
"""
import json
import os
from config import CONTACTS_FILE

class ContactsManager:
    """通讯录管理器"""
    
    def __init__(self):
        self.contacts = {}
        self._load_contacts()
    
    def _load_contacts(self):
        """加载通讯录"""
        if os.path.exists(CONTACTS_FILE):
            try:
                with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
                    self.contacts = json.load(f)
            except Exception as e:
                print(f"加载通讯录失败: {e}")
                self.contacts = {}
        else:
            self.contacts = {}
    
    def _save_contacts(self):
        """保存通讯录"""
        os.makedirs(os.path.dirname(CONTACTS_FILE), exist_ok=True)
        try:
            with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存通讯录失败: {e}")
            return False
    
    def add_contact(self, username, ip, port, status='online'):
        """添加联系人"""
        self.contacts[username] = {
            'username': username,
            'ip': ip,
            'port': port,
            'status': status
        }
        self._save_contacts()
    
    def remove_contact(self, username):
        """删除联系人"""
        if username in self.contacts:
            del self.contacts[username]
            self._save_contacts()
            return True
        return False
    
    def update_contact_status(self, username, status):
        """更新联系人状态"""
        if username in self.contacts:
            self.contacts[username]['status'] = status
            self._save_contacts()
            return True
        return False
    
    def get_contact(self, username):
        """获取联系人信息"""
        return self.contacts.get(username)
    
    def get_sorted_contacts(self):
        """获取按字母排序的联系人列表"""
        # 按照用户名（首字母）排序
        sorted_contacts = sorted(
            self.contacts.items(),
            key=lambda x: x[0].upper()
        )
        return [contact[1] for contact in sorted_contacts]
    
    def get_all_contacts(self):
        """获取所有联系人"""
        return self.contacts
    
    def contact_exists(self, username):
        """检查联系人是否存在"""
        return username in self.contacts

