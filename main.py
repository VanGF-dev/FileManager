from manager import FileManager

if __name__ == "__main__":

    fm = FileManager()
    
    try:
        while True:

            if fm.current_user is None:
                fm.main_menu()
                choice = input("请选择操作: ").strip()

                if choice == "1":
                    username = input("请输入用户名: ").strip()
                    password = input("请输入密码: ").strip()

                    try:
                        fm.create_user(username, password)
                    except ValueError as e:
                        print(f"创建用户失败: {e}")


                elif choice == "2":
                    username = input("请输入用户名: ").strip()
                    password = input("请输入密码: ").strip()

                    try:
                        fm.login(username, password)
                        
                    except ValueError as e:
                        print(f"登录失败: {e}")


                elif choice == "3":
                        break
                
                else:
                    print("无效的操作，请重新选择")

            else:
                fm.login_menu()
                choice = input("请选择操作: ").strip()

                if choice == "1":
                    file_name = input("请输入文件名: ").strip()
                    content = input("请输入文件内容: ").strip()

                    try:
                        fm.create_file(file_name, content)
                    except ValueError as e:
                        print(f"创建文件失败: {e}")

                elif choice == "2":
                    file_name = input("请输入文件名: ").strip()
                    try:
                        fm.delete_file(file_name)
                    except ValueError as e:
                        print(f"删除文件失败: {e}")

                elif choice == "3":
                    file_name = input("请输入文件名: ").strip()
                    content = input("请输入新内容: ").strip()
                    try:
                        fm.update_file(file_name, content)
                    except ValueError as e:
                        print(f"更新文件失败: {e}")

                elif choice == "4":
                    try:
                        fm.list_file()
                    except ValueError as e:
                        print(f"列出文件失败: {e}")

                elif choice == "5":
                    content = input("请输入搜索内容: ").strip()
                    try:
                        fm.find_file(content)
                    except ValueError as e:
                        print(f"搜索文件失败: {e}")

                elif choice == "6":
                    file_name = input("请输入文件名: ").strip()
                    try:
                        fm.read_file(file_name)
                    except ValueError as e:
                        print(f"读取文件失败: {e}")

                elif choice == "7":
                    try:
                        fm.logout()
                    except ValueError as e:
                        print(f"登出失败: {e}")

                else:
                    print("无效的操作，请重新选择")
        
    finally:
        print("感谢使用文件管理系统，再见！")
                    
                        


            
                    
                
        




        

