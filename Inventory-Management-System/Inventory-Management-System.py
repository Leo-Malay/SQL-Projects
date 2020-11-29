import mysql.connector
import datetime


class inventory_management:
    def __init__(self, host, user, password):
        try:
            self.__db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database="inventory"
            )
            self.__myc = self.__db.cursor()
            print("[SUCCESS]: Connected successfully")
        except:
            print("[ERROR]: Failed to connect")
            exit(1)

    def date(self):
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d"))

    def end(self):
        self.__db.commit()
        self.__db.close()

    def add_item(self, code, name, price, qpp):
        # To add a new kind of item.
        query = "INSERT INTO item_data (code, name, price, qpp) VALUES ('" + \
            str(code)+"','"+name+"','"+str(price)+"','"+str(qpp)+"');"
        query1 = "INSERT INTO stock_data (code, qty) VALUES ('" + \
            str(code)+"',"+str(0)+");"
        try:
            self.__myc.execute(query)
            self.__myc.execute(query1)
            self.__db.commit()
            print("[SUCCESS]: Item added successfully")
            return 1
        except:
            print("[ERROR]: Unable to add the item")
            return -1

    def rm_item(self, code):
        # To remove the item.
        query = "DELETE FROM item_data WHERE code='"+str(code)+"';"
        query1 = "DELETE FROM stock_data WHERE code='"+str(code)+"';"
        try:
            self.__myc.execute(query)
            self.__myc.execute(query1)
            self.__db.commit()
            print("[SUCCESS]: Item removed successfully")
            return 1
        except:
            print("[ERROR]: Unable to remove the item")
            return -1

    def search_item(self, name=-1):
        # Search item code from name.
        query = "SELECT * FROM item_data WHERE name LIKE '"+name+"%';"
        self.__myc.execute(query)
        self.__result = self.__myc.fetchall()
        return self.__result

    def refill_stock(self, code, qty):
        # Refill the stock.
        query0 = "SELECT qty FROM stock_data WHERE code='"+str(code)+"';"
        query1 = "INSERT INTO refill_data (code, qty, refill_date) VALUES ('" + \
            str(code)+"',"+str(qty)+",'"+self.date()+"');"
        try:
            self.__myc.execute(query0)
            self.__result = self.__myc.fetchone()
            query = "UPDATE stock_data SET qty=" + \
                str(qty+self.__result[0])+" WHERE code='"+str(code)+"';"
            self.__myc.execute(query)
            self.__myc.execute(query1)
            self.__db.commit()
            print("[SUCCESS]: Refill successfull")
            return 1
        except:
            print("[ERROR]: Refill Unsuccessfull")
            return -1

    def use_stock(self, code, qty):
        # Use from the stock.
        query = "SELECT qty FROM stock_data WHERE code='"+str(code)+"';"
        query1 = "UPDATE stock_data SET qty=" + \
            str(qty)+" WHERE code='"+str(code)+"';"
        query2 = "INSERT INTO use_data (code, qty, use_date) VALUES ('" + \
            str(code)+"',"+str(qty)+",'"+self.date()+"');"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchone()
            if int(self.__result[0]) >= int(qty):
                qty = self.__result[0] - qty
                query1 = "UPDATE stock_data SET qty=" + \
                    str(qty)+" WHERE code='"+str(code)+"';"
                query2 = "INSERT INTO use_data (code, qty, use_date) VALUES ('" + \
                    str(code)+"',"+str(qty)+",'"+self.date()+"');"
                self.__myc.execute(query1)
                self.__myc.execute(query2)
                self.__db.commit()
                print("[SUCCESS]: Use successfull")
                return 1
            else:
                print("[ERROR]: Not enough qty to complete task")
                return -1
        except:
            print("[ERROR]: Use Unsuccessfull")
            return -1


# TEST code.
# inv = inventory_management("localhost", "username", "password")
# inv.add_item("code", "name", price, quantity_per_piece)
# inv.rm_item("code")
# print(inv.search_item("name"))
# inv.refill_stock("code", quantity)
# inv.use_stock("code", quantity)
# inv.end()
