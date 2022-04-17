import sqlite3

class sqlite_table_header:

    def __init__(self,data_in:dict):
        """
        initialization function
        """
        self.name       = str(data_in['name'])
        self.data_type  = str(data_in['type'])
        self.not_null   = bool(data_in['not_null'])
        self.pk         = bool(data_in['primary_key'])
        try:
            self.default_value = data_in['default_value']
        except:
            self.default_value = None
    
    def get_to_crate(self):
        """
        Returns the data used to create.
        """
        return_data = f'{self.name}\t{self.data_type}'
        if self.pk:
            return_data += f'\tPRIMARY KEY'
        if self.not_null:
            return_data += f'\tNOT NULL'
        return return_data + ",\n"
    
    def get_to_out(self):
        """
        Returns the data used to print.
        """
        return {
                "name"          : self.name,
                "type"          : self.data_type,
                "not_null"      : self.not_null,
                "default_value" : self.default_value,
                "primary_key"   : self.pk
            }

class core:

    # Main code

    def __init__(self,path:str="db.sqlite3") -> None:
        """
        initialization function.
        """
        self.path = path
        self.connect()
    
    def connect(self) -> None:
        """
        Connect to the database.
        """
        self.conn   = sqlite3.connect(self.path)
        self.cur    = self.conn.cursor()

    def command(self,sql_command:str,sql_param:list=[]) -> list:
        """
        Send command and return processing result.
        """
        self.cur.execute(sql_command,sql_param)
        return self.cur.fetchall()
    
    def execute(self,sql_command:str,sql_param:list=[]):
        """
        Send command without returning result.
        """
        self.cur.execute(sql_command,sql_param)
    
    def commit(self):
        """
        Submit to database.
        """
        self.conn.commit()
    
    def close(self):
        """
        close the connection.
        """
        self.conn.close()


    # Function

    def list_table(self) -> list:
        """
        List all table names.
        """
        table_list = []
        for table in self.command("select name from sqlite_master where type='table' order by name;"):
            table_list.append(table[0]) 
        return table_list
    
    def show_table_header(self,table_name:str) -> dict:
        """
        List header data for the selected table.
        """
        data_dict = {}
        for header_single in self.command(f"PRAGMA table_info({table_name});"):
            data_dict[header_single[0]]=sqlite_table_header({
                "name"          : header_single[1],
                "type"          : header_single[2],
                "not_null"      : header_single[3],
                "default_value" : header_single[4],
                "primary_key"   : header_single[5]
            }).get_to_out()
        return data_dict

    def show_table_body(self,table_name:str,column:list=["*"]) -> dict:
        """
        List body data for the selected table.
        """
        data_dict = []
        select_column = ",".join(column)
        if column == ["*"]:
            column = []
            for _,single_column in self.show_table_header(table_name).items():
                column.append(single_column["name"])
        for value in self.command(f"select {select_column} from {table_name}"):
            data_single = {}
            i=0
            for value_single in value:
                data_single[column[i]] = value_single
                i+=1
            data_dict.append(data_single)
        return data_dict
    
    def crate_table(self,table_name:str,header_list:list):
        """
        Crate table.
        """
        self.execute(f'CREATE TABLE {table_name}(\n{"".join([single.get_to_crate() for single in header_list])[:-2]}\n);')

    def delete_table(self,table_name:str):
        """
        delete table.
        """
        self.execute(f'DROP TABLE {table_name};')
    
    def insert_data(self,table_name:str,args:dict):
        """
        Insert data.
        """
        key_list = []
        value_list = []
        for key,value in args.items():
            key_list.append(str(key))
            if type(value) == str:
                value_list.append(f"'{value}'")
            elif type(value) == None:
                value_list.append("NULL")
            else:
                value_list.append(str(value))
        key_text = ",".join(key_list)
        value_text = ",".join(value_list)
        self.execute(f"INSERT INTO {table_name}({key_text}) VALUES ({value_text});")
    
    def update_data(self,table_name:str,update_key,update_data,pk_select,pk_name:str="id"):
        """
        Change the data.
        """
        if type(update_data) == str:
            update_data = f"'{update_data}'"
        elif type(update_data) == None:
            update_data = "NULL"
        else:
            update_data = str(update_data)
        self.execute(f"UPDATE {table_name} SET {update_key} = {update_data} WHERE {pk_name} = {pk_select};")

    def delete_data(self,table_name:str,pk_select,pk_name:str="id"):
        """
        Delete data
        """
        self.execute(f"DELETE FROM {table_name} WHERE {pk_name} = {pk_select};")