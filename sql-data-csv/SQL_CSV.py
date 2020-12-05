import mysql.connector


class sql_csv:
    def __init__(self, host, username, password):
        try:
            self.__db = mysql.connector.connect(
                host=host,
                user=username,
                password=password
            )
            self.__myc = self.__db.cursor()
            print("[SUCCESS]: Conneted to database")
        except:
            print("[ERROR]: Failed to connect to database")
            exit(1)

    def end(self):
        self.__myc.close()
        self.__db.commit()
        self.__db.close()

    def get_columns(self, table_name):
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + \
            table_name+"' ORDER BY ORDINAL_POSITION"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchall()
            col_list = []
            for ch in self.__result:
                col_list.append(ch[0])
            print("[SUCCESS]: List of column Obtained")
            return col_list
        except:
            print("[ERROR]: List of column not Obtained")
            return -1

    def get_data(self, database, table_name, col_list=-1):
        if col_list != -1:
            col_list = ",".join(col_list)
            query = "SELECT "+col_list+" FROM "+database+"."+table_name+";"
        else:
            query = "SELECT * FROM "+database+"."+table_name+";"
        try:
            self.__myc.execute(query)
            self.__result = self.__myc.fetchall()
            print("[SUCCESS]: Data fetched successfully")
            return self.__result
        except:
            print("[ERROR]: Unable to get data")
            return -1

    def write_to_csv(self, file_name, database, table_name):
        try:
            col_list = self.get_columns(table_name)
            data_list = self.get_data(database, table_name)
            file_data = open(f"{file_name}.csv", "w")
            file_data.write(",".join(col_list) + "\n")
            for ch in data_list:
                x = ""
                for ele in ch:
                    x += f'"{ele}",'
                file_data.write(x + "\n")
            file_data.close()
            print("[SUCCESS]: Data written to the file successfully")
            return 1
        except:
            print("[ERROR]: Some error occoured")
            return -1


# Testing
# db = sql_csv("localhost", "username", "password")
# db.get_columns("table_name")
# print(db.get_data("database_name", "table_name""))
# db.write_to_csv("file_name", "database_name", "table_name")
# db.end()
