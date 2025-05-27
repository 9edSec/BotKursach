import json

class UserTool:
    
    def __init__(self):
        self.msg_user = self.msg_load()['user']
        self.msg_admin = self.msg_load()['admin']

    
    def msg_load(self):
        with open('bot/message/user.json', 'r', encoding='utf-8') as file_msg:
            file_msg_read = json.load(file_msg)
        
        return file_msg_read
    

    @property
    def user_answer(self):
        return self.msg_user['text_answer']
    
    @property
    def user_keyboard(self):
        return self.msg_user['text_kb']

UserTools = UserTool()