from manager import FileManager

if __name__ == "__main__":

    fm = FileManager()
    try:
        # fm.create_user("testuser", "testpassword")y

        fm.login("testuser","testpassword")
        fm.list_files()
        fm.read_file("testfile")
        fm.logout()
    except ValueError as e:
        print(e)




        

