from typing import Optional
from sqlalchemy import select
from sqlalchemy import func
from user import User
from file import File
from base import Session
import os

class FileManager:
    def __init__(self):
        self.current_user: Optional[User] = None

    def create_user(self, username: str, password: str) -> User:
        with Session() as session:
            user = User(username=username, password=password)
            exiting_user = session.query(User).filter_by(username=username).first()

            if exiting_user is not None:
                raise ValueError(f"用户{username}已存在")
        
            if username == "":
                raise ValueError("用户名不能为空")
        
            if password == "":
                raise ValueError("密码不能为空")
            
            
            repeat_password = input("请确认密码: ").strip()
            if repeat_password != password:
                raise ValueError("两次输入的密码不一致")
            
            session.add(user)
            print(f"用户{username}已创建")
            session.commit()
            return user
    
    def login(self, username: str, password: str) -> Optional[User]:
        with Session() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user is None:
                print("用户名或密码错误")
            else: 
                self.current_user = user
                print(f"用户{username}登录成功")
            return user
    
    def logout(self):
        if self.current_user is None:
            print("没有用户登录")
            return
        self.current_user = None
        print("已登出当前用户")

    def create_file(self, file_name: str, content, auto=False) -> File:
        with Session() as session:
            if not self.current_user:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()
            

            existing_file = session.query(File).filter_by(file_name=file_name).first()
            if existing_file is not None:
                if not auto:
                    response = input(f"文件{existing_file.file_name}已存在，是否替换原有文件？(y/n)").strip().lower()
                    if response != "y":
                        print("文件创建已取消")
                        return None
                    
                if os.path.exists(existing_file.file_path):
                    os.remove(existing_file.file_path)
                    session.delete(existing_file)
                    session.commit()
            
            filepath = os.path.join(f"user_files_{user.id}", file_name)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            if content is not None:
                with open(filepath, "w") as f:
                    f.write(content)

                user_file = File(file_name=file_name, file_path=filepath, user_id=user.id)
                session.add(user_file)
                session.commit()
                print(f"文件{file_name}已创建并保存到{filepath}")
                return user_file
            
    def delete_file(self, file_name:str):
        with Session() as session:
            if self.current_user is None:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()
            if user is None:
                raise ValueError(f"用户{self.current_user.username}不存在")
            
            file = session.query(File).filter_by(file_name=file_name, user_id=user.id).first()
            if file is None:
                raise ValueError(f"文件{file_name}不存在")
            
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            
            session.delete(file)
            session.commit()
            print(f"文件{file_name}已删除")

    def update_file(self, file_name: str, new_content: str):
        with Session() as session:
            if self.current_user is None:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()
            if user is None:
                raise ValueError(f"用户{self.current_user.username}不存在")
            
            file = session.query(File).filter_by(file_name=file_name, user_id=user.id).first()
            if file is None:
                raise ValueError(f"文件{file_name}不存在")
            
            with open(file.file_path, "w") as f:
                f.write(new_content)
            
            print(f"文件{file_name}已更新")

    def list_file(self):

        with Session() as session:
            if self.current_user is None:
                raise ValueError("请先登录")
            
            user_id = session.query(User).filter_by(username=self.current_user.username).first().id
            count = select(func.count()).select_from(File).where(File.user_id == self.current_user.id)
            total = session.execute(count).scalar()
            page_size = 2
            
            for offset in range(0, total, page_size):
                files = session.query(File
                                ).filter_by(user_id=user_id
                                ).order_by(File.id
                                ).offset(offset
                                ).limit(page_size
                                ).all()

                for file in files:
                    print(f"文件名: {file.file_name}, 路径: {file.file_path}")
            
        
    def find_file(self, content: str) -> Optional[File]:
            
            with Session() as session:
                if self.current_user is None:
                    raise ValueError("请先登录")
                
                user = session.query(User).filter_by(username=self.current_user.username).first()
                files = session.query(File).filter_by(user_id=user.id).filter(File.file_name.like(f"%{content}%")).all()
                 
                if files is None:
                    print("没有找到匹配的文件")
                    return None
                
                for file in files:
                    print(f"找到文件: {file.file_name}，路径: {file.file_path}")
                

    def read_file(self, file_name: str) -> Optional[str]:
        with Session() as session:
            if self.current_user is None:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()

            file = session.query(File).filter_by(file_name=file_name, user_id=user.id).first()
            if file is None:
                raise ValueError(f"文件{file_name}不存在")
            
            with open(file.file_path, "r") as f:
                content = f.read()
                print(f"文件内容: {content}")
                return content

            
    def main_menu(self):
        print("欢迎使用文件管理系统")
        print("1. 注册")
        print("2. 登录")
        print("3. 退出")

    def login_menu(self):
        print("1. 创建文件")
        print("2. 删除文件")
        print("3. 更新文件")
        print("4. 列出文件")
        print("5. 查找文件")
        print("6. 读取文件")
        print("7. 登出")
    