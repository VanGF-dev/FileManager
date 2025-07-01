from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os


engine = create_engine("sqlite:///vandata.db")
Session = sessionmaker(bind=engine)
Base = DeclarativeBase()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    file: Mapped[List["File"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="file")



class FileManager:
    def __init__(self):
        self.session = Session()
        self.current_user: Optional[User] = None

    def create_user(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        exiting_user = self.session.query(User).filter_by(username=username).first()

        if exiting_user is not None:
            raise ValueError(f"用户{username}已存在")
        
        if username is None or username.strip() == "":
            raise ValueError("用户名不能为空")
        
        if password is None or password.strip() == "":
            raise ValueError("密码不能为空")
        

        repeat_password = input("请确认密码: ").strip()
        if repeat_password != password:
            raise ValueError("两次输入的密码不一致")
        
        self.session.add(user)
        self.session.commit()
        print(f"用户{username}已创建")
        return user
    
    def login(self, username: str, password: str) -> Optional[User]:
        user = self.session.query(User).filter_by(username=username, password=password).first()
        if user is None:
            print("用户名或密码错误")
        self.current_user = user
        print(f"用户{username}登录成功")
        return user
    
    def logout(self):
        self.current_user = None
        print("已登出当前用户")

    def create_file(self, username: str, file_name: str, content: str, auto=False) -> File:
        if not self.current_user:
            raise ValueError("请先登录")
        
        user = self.session.query(User).filter_by(username=username).first()
        if user is None:
            raise ValueError(f"用户{username}不存在")
        
        

        existing_file = self.session.query(File).filter_by(file_name=file_name).first()
        if existing_file is not None:
            if not auto:
                response = input(f"文件{existing_file}已存在，是否替换原有文件？(y/n)").strip().lower()
                if response != "y":
                    print("文件创建已取消")
                    return None
                
            if os.path.exists(existing_file.file_path):
                os.remove(existing_file.file_path)
                self.session.delete(existing_file)
                self.session.commit()
        
        filepath = os.path.join(f"user_files_{user.id}", file_name)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if content is not None:
            with open(filepath, "w") as f:
                f.write(content)

                user_file = File(file_name=file_name, file_path=filepath, user_id=user.id)
                self.session.add(user_file)
                self.session.commit()
                print(f"文件{file_name}已创建并保存到{filepath}")
                return user_file
            
    def close(self):
        self.session.close()

if __name__ == "__main__":

    fm = FileManager()
    try:
        # fm.create_user("testuser", "testpassword")
        fm.login("testuser","testpassword")
        fm.create_file("testuser", "testfile", "helloworld")
        
    except ValueError as e:
        print(e)
    finally:
        fm.close()  




        

