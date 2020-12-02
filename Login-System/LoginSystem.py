import mysql.connector
import datetime
import random


class login_system:
    def __init__(self, host, user, password):
        # This function tries to connect to the server
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
        # At the end of every connection calling this funtion will sve any changes.
        self.__db.commit()
        self.__db.close()

    def login(self, username, password):
        # To login to your account.
        query = "SELECT uid,password FROM login_credential WHERE username='" + username + "';"
        self.__myc.execute(query)
        self.__result = self.__myc.fetchone()
        if self.__result == None:
            print("[ERROR]: No such Account exist")
            return -1, -1
        elif self.__result[1] == password:
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

    def check_token(self, username, token):
        # Check token for that user.
        query = "SELECT username FROM (SELECT login_credential.username,curr_login_status.token FROM login_credential INNER JOIN curr_login_status ON login_credential.uid=curr_login_status.uid) AS a WHERE token='"+str(token)+"';"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchone()
            if self.__result[0] == username:
                print("[SUCCESS]: Token matched")
                return 1
            else:
                print("[ERROR]: Token not Matched")
                return -1
        except:
            print("[ERROR]: No such token found.")
            return -1

    def logout(self, token):
        # Logout from the account.
        query = "SELECT uid FROM curr_login_status where token='" + \
            str(token)+"' AND is_active=1;"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchone()
            if self.__result != None:
                query1 = "UPDATE curr_login_status SET is_active=0,logout_dt='" + \
                    self.__datetime()+"',token='0' WHERE uid=" + \
                    str(self.__result[0])+";"
                self.__myc.execute(query1)
                self.__db.commit()
                print("[SUCCESS]: Logged out successfully")
                return 1
            else:
                print("[ERROR]: No such Token found")
                return -1
        except:
            print("[ERROR]: Unable to Logout")
            return -1

    def new_user(self, name, username, password):
        # Register a new user to the system/
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

    def rm_user(self, username, token):
        # For removing the account.
        self.__result = self.check_token(username, token)
        if self.__result == 1:
            uid = str(self.__get_uid(username))
            query = "DELETE FROM login_credential WHERE uid=" + uid + ";"
            query1 = "DELETE FROM curr_login_status WHERE uid=" + uid + ";"
            self.__myc.execute(query)
            self.__myc.execute(query1)
            self.__db.commit()
            print("[SUCCESS]: Account removed successfully")
            return 1
        else:
            print("[ERROR]: You are not Authorized to delete the account")
            return -1

    def get_uid(self, token=-1):
        if token != -1:
            query = "SELECT uid FROM curr_login_status WHERE token='" + \
                str(token)+"';"
            try:
                self.__myc.execute(query)
                self.__result = self.__myc.fetchone()
                if self.__result == None:
                    print("[ERROR]: No such user found")
                    return -1
                else:
                    print("[SUCCESS]: User found")
                    return self.__result[0]
            except:
                print("[ERROR]: Ran into some problem")
                return -1
        else:
            print("[ERROR]: Argument is required")
            return -1

    def __get_uid(self, username=-1):
        if username != -1:
            query = "SELECT uid FROM login_credential WHERE username='" + \
                str(username)+"';"
            try:
                self.__myc.execute(query)
                self.__result = self.__myc.fetchone()
                if self.__result == None:
                    print("[ERROR]: No such user found")
                    return -1
                else:
                    print("[SUCCESS]: User found")
                    return self.__result[0]
            except:
                print("[ERROR]: Ran into some problem")
                return -1
        else:
            print("[ERROR]: Argument is required")
            return -1

    def __gen_token(self, username, password):
        # Generate a token for the user.
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
        # Date & time stamp for the system.
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S"))


# Test code
# db_username = "db_user"
# db_password = "db_pass"
# db = login_system("localhost", db_username, db_password)
# username = "username"
# password = "password"
# db.new_user("name", username111, password111)
# res, token = db.login(username, password)
# db.check_token(username, token)
# db.rm_user(username, token)
# db.logout(token)
# db.end()
