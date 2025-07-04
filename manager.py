from typing import Optional
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
        
            if username.strip() == "":
                raise ValueError("用户名不能为空")
        
            if password is None or password.strip() == "":
                raise ValueError("密码不能为空")
            
            
            repeat_password = input("请确认密码: ").strip()
            if repeat_password != password:
                raise ValueError("两次输入的密码不一致")
            
            session.add(user)
            session.commit()
            print(f"用户{username}已创建")
            return user
    
    def login(self, username: str, password: str) -> Optional[User]:
        with Session() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user is None:
                print("用户名或密码错误")
            self.current_user = user
            print(f"用户{username}登录成功")
            return user
    
    def logout(self):
        self.current_user = None
        print("已登出当前用户")

    def create_file(self, username: str, file_name: str, content: str, auto=False) -> File:
        with Session() as session:
            if not self.current_user:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()
            if user is None:
                raise ValueError(f"用户{username}不存在")
            
            

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
            if not self.current_user:
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
            if not self.current_user:
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

    def list_files(self) -> list[File]:

        with Session() as session:
            if not self.current_user:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()
            if user is None:
                raise ValueError(f"用户{self.current_user.username}不存在")
            
            files = session.query(File).filter_by(user_id=user.id).all()
            
            for file in files:
                print(f"文件名: {file.file_name}, 路径: {file.file_path}")
            return files
        
    def find_file(self, file_name: str) -> Optional[File]:
            
            with Session() as session:
                if not self.current_user:
                    raise ValueError("请先登录")
                
                user = session.query(User).filter_by(username=self.current_user.username).first()
                
                if user is None:
                    raise ValueError(f"用户{self.current_user.username}不存在")
                
                file = session.query(File).filter_by(file_name=file_name, user_id=user.id).first()
                if file is None:
                    print(f"文件{file_name}不存在")
                    return None
                
                print(f"找到文件: {file.file_name}, 路径: {file.file_path}")
                return file 

    def read_file(self, file_name: str) -> Optional[str]:
        with Session() as session:
            if not self.current_user:
                raise ValueError("请先登录")
            
            user = session.query(User).filter_by(username=self.current_user.username).first()
            if user is None:
                raise ValueError(f"用户{self.current_user.username}不存在")
            
            file = session.query(File).filter_by(file_name=file_name, user_id=user.id).first()
            if file is None:
                raise ValueError(f"文件{file_name}不存在")
            
            with open(file.file_path, "r") as f:
                content = f.read()
                print(f"文件内容: {content}")
                return content