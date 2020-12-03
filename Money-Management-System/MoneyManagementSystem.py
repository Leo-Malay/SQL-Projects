import mysql.connector
import datetime


class money_management_system:
    def __init__(self, host, user, password):
        # This function tries to connect to the server
        try:
            self.__db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database="money_manager"
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

    def add_user(self, uid):
        query = "INSERT INTO balance (uid, amount, last_dt) VALUES (" + \
            str(uid)+",0.00,'"+self.__datetime()+"');"
        try:
            self.__myc.execute(query)
            self.__db.commit()
            print("[SUCCESS]: Account created successfully")
            return 1
        except:
            print("[ERROR]: Unable to complete your request")
            return 0

    def rm_user(self, uid):
        query = "DELETE FROM balance WHERE uid="+str(uid)+";"
        query1 = "DELETE FROM record WHERE uid="+str(uid)+";"
        try:
            self.__myc.execute(query)
            self.__myc.execute(query1)
            self.__db.commit()
            print("[SUCCESS]: Account removed successfully")
            return 1
        except:
            print("[ERROR]: Unable to complete your request")
            return 0

    def add_amount(self, uid, amount, purpose):
        query = "INSERT INTO record (uid, type, amount, purpose, dt) VALUES ("+str(uid) + \
            ",'DEPOSIT',"+str(amount)+",'"+str(purpose) + \
            "','"+self.__datetime()+"');"
        query1 = "SELECT amount FROM balance WHERE uid="+str(uid)+";"
        try:
            self.__myc.execute(query1)
            self.__result = self.__myc.fetchone()
            if self.__result != None:
                acc_amount = self.__result[0] + amount
                query2 = "UPDATE balance SET amount="+str(acc_amount)+",last_dt='" + \
                    self.__datetime()+"' WHERE uid="+str(uid)+";"
                self.__myc.execute(query2)
                self.__myc.execute(query)
                self.__db.commit()
                print("[SUCCESS]: Money added successfully")
                return 1
            else:
                print("[ERROR]: No such account found.")
                return -1
        except:
            print("[ERROR]: Something went wrong")
            return -1

    def spend_amount(self, uid, amount, purpose):
        query = "INSERT INTO record (uid, type, amount, purpose, dt) VALUES ("+str(uid) + \
            ",'WITHDRAW',"+str(amount)+",'"+str(purpose) + \
            "','"+self.__datetime()+"');"
        query1 = "SELECT amount FROM balance WHERE uid="+str(uid)+";"
        try:
            self.__myc.execute(query1)
            self.__result = self.__myc.fetchone()
            if self.__result != None:
                if self.__result[0] >= amount:
                    acc_amount = self.__result[0] - amount
                    query2 = "UPDATE balance SET amount="+str(acc_amount)+",last_dt='" + \
                        self.__datetime()+"' WHERE uid="+str(uid)+";"
                    self.__myc.execute(query2)
                    self.__myc.execute(query)
                    self.__db.commit()
                    print("[SUCCESS]: Money added successfully")
                    return 1
                else:
                    print("[ERROR]: Insufficient balance")
                    return 0
            else:
                print("[ERROR]: No such account found.")
                return -1
        except:
            print("[ERROR]: Something went wrong")
            return -1

    def show_record(self, uid):
        query = "SELECT * FROM record WHERE uid="+str(uid)+";"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchall()
            print("[SUCCESS]: Account found")
            return self.__result
        except:
            print("[ERROR]: No such account found")
            return -1

    def check_balance(self, uid):
        query = "SELECT amount, last_dt FROM balance WHERE uid="+str(uid)+";"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchone()
            print("[SUCCESS]: Account found")
            return self.__result
        except:
            print("[ERROR]: No such account found")
            return -1

    def __datetime(self):
        # Date & time stamp for the system.
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S"))


# Test code
# db_username = "db_user"
# db_password = "db_pass"
# db = money_management_system("localhost", db_username, db_password)
# db.add_user(1)
# db.add_amount(1, 1000.00, "Fun is Fun")
# print(db.check_balance(1))
# db.spend_amount(1, 500.00, "Eating")
# print(db.check_balance(1))
# print(db.show_record(1))
# db.end()
