import mysql.connector
import datetime
import random


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
        query = "SELECT uid,password FROM login_credential WHERE username='" + username + "';"
        self.__myc.execute(query)
        self.__result = self.__myc.fetchone()
        if self.__result[1] == password:
            token = self.__gen_token(username, password)
            query1 = "UPDATE curr_login_status SET token='"+str(token)+"',login_dt='" + \
                self.__datetime()+"',is_active=1 where uid='" + \
                str(self.__result[0])+"';"
            self.__myc.execute(query1)
            self.__db.commit()
            print("[SUCCESS]: Logged in successfully")
            return 1, token
        else:
            print("[ERROR]: Login failed")
            return -1, -1

    def new_user(self, name, username, password):
        query = "INSERT INTO login_credential (name, username, password) VALUES ('" + \
            name + "','" + username + "','" + password + "');"
        sup_query = "SELECT username FROM login_credential WHERE username='" + username + "';"
        sup_query1 = "SELECT uid FROM login_credential WHERE username='" + username + "';"
        try:
            self.__myc.execute(sup_query)
            self.__result = self.__myc.fetchone()
            if(self.__result == None):
                self.__myc.execute(query)
                self.__myc.execute(sup_query1)
                self.__result = self.__myc.fetchone()
                query1 = "INSERT INTO curr_login_status (uid,login_dt,logout_dt,is_active,token) VALUES ('" + \
                    str(self.__result[0])+"','" + self.__datetime()+"','" + \
                    self.__datetime() + "',0,'None');"
                self.__myc.execute(query1)
                self.__db.commit()
                print("[SUCCESS]: New Account successfully created")
                return 1
            else:
                print("[ERROR]: Username already exist")
                return -1
        except:
            print("[ERROR]: Account not created")
            return -1

    def __gen_token(self, username, password):
        # Preparing the randomizied Ref string.
        ref_str = "0A1z2B3y4C5x6D7w8E9v@F#u$G%t^H&s*I_r-J+q=K.p,L<o>M:n;N?m~O`l!P kQjRiShTgUfVeWdXcYbZa"
        ref_str = list(ref_str)
        random.shuffle(ref_str)
        ref_str = "".join(ref_str)
        # Preparing the raw token.
        raw_token = list(str(username) + str(password) + self.__datetime())
        random.shuffle(raw_token)
        # Generating the final token
        token = ''
        for ch in raw_token:
            token += str(ref_str.index(ch))
        return token

    def __datetime(self):
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S"))


# Test code
# db = login_system("localhost", "username", "password")
# db.new_user("name", "username", "password")
# res, token = db.login("username", "password")
# db.end()
