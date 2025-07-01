from manager import FileManager

if __name__ == "__main__":

    fm = FileManager()
    try:
        # fm.create_user("testuser", "testpassword")
        fm.login("testuser","testpassword")
        fm.create_file("testuser", "testfile", "helloworld")
        fm.logout()
    except ValueError as e:
        print(e)




        

