from manager import FileManager

if __name__ == "__main__":

    fm = FileManager()
    try:
        # fm.create_user("testuser", "testpassword")y

        fm.login("van", "van1234")
        fm.list_file()
        fm.logout()
    except ValueError as e:
        print(e)




        

