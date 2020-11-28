import mysql.connector


class login_system:
    def __init__(self, host, user, password):
        try:
            self.__db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database="login_system"
            )
            self.__myc = self.__db.cursor()
            print("[SUCCESS]: Connected successfully")
        except:
            print("[ERROR]: Failed to connect")
            exit(1)

    def end(self):
        self.__db.commit()
        self.__db.close()

    def login(self, username, password):
        query = "SELECT password FROM login_credential WHERE username='" + username + "';"
        self.__myc.execute(query)
        self.__result = self.__myc.fetchone()
        if self.__result[0] == password:
            print("[SUCCESS]: Logged in successfully")
            return 1
        else:
            print("[ERROR]: Login failed")
            return -1

    def new_user(self, name, username, password):
        query = "INSERT INTO login_credential (name, username, password) VALUES ('" + name + "','" + \
            username + "','" + password + "');"
        sup_query = "SELECT username FROM login_credential WHERE username='" + username + "';"
        try:
            self.__myc.execute(sup_query)
            self.__result = self.__myc.fetchone()
            print(self.__result)
            if(self.__result == None):
                self.__myc.execute(query)
                self.__db.commit()
                print("[SUCCESS]: New Account successfully created")
                return 1
            else:
                print("[ERROR]: Username already exist")
                return -1
        except:
            print("[ERROR]: Account not created")
            return -1


# Test code

# db = login_system("localhost", "username", "password")
# db.new_user("name", "username", "password")
# db.login("username", "password")
# db.end()
