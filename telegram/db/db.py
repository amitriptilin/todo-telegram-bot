import psycopg2

class PIDORAS():
    def __init__(self, dbname="yourdbname", user='yourusername', password='yourpasssword', host='yourhost', port='yourport'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def read_tasks(self):
        try:
            with self.connection.cursor() as cursor:
                insert_query = "SELECT * FROM tasks;"
                cursor.execute(insert_query)
                self.connection.commit()
                records = cursor.fetchall()
                return_array = []
                print("[PIDORAS] Data read successfully!")
                for i in records:
                    return_array.append({"task_id": i[0], "title": i[1], "desc": i[2], "done": i[3]})
                return return_array
                
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
            
            
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("[PIDORAS] Connection was successful!")
        except Exception as e:
            print(f"[PIDORAS] An error occurred while connecting to the database: {e}")
            
    def add_task(self, name, desc, user_id):
        try:
            okak = str(len(self.read_tasks())) 
            with self.connection.cursor() as cursor:
                insert_query = "INSERT INTO tasks (id, name_task, task_esse) VALUES (%s, %s, %s);"
                data_to_insert = [
                    (okak, name, desc),
                ]
                insert_shit_query = f"INSERT INTO users (users_tasks) VALUES ('{user_id}', ARRAY['{okak}'])"
                cursor.execute(insert_shit_query)
                self.connection.commit()
                cursor.executemany(insert_query, data_to_insert)
                self.connection.commit()

                print("[PIDORAS] Data inserted successfully!")

        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
            
    def delete_task(self, task_id):
        try:
            with self.connection.cursor() as cursor:
                delete_query = f"DELETE FROM tasks WHERE id = {task_id}"
                cursor.execute(delete_query)
                self.connection.commit()
                
                print("[PIDORAS] Data deleted successfully!")
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
            
    def holy_hand_grenade(self):
        try:
            with self.connection.cursor() as cursor:
                delete_all_query = "DELETE FROM tasks"
                cursor.execute(delete_all_query)
                self.connection.commit()
                
                print("[PIDORAS] HOLY HAND GRENADE")
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
            
    def done_task(self, task_id):
        try:
            with self.connection.cursor() as cursor:
                change_bool = f"UPDATE tasks SET task_done = NOT task_done WHERE id = {task_id}; "
                bool_to_insert = [
                    (task_id)
                ]
                cursor.executemany(change_bool, bool_to_insert)
                self.connection.commit()
                
                print("[PIDORAS] Done changed successfully")
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
                    
    def edit_name(self, name, task_id): 
        try:
            with self.connection.cursor() as cursor:
                old_name = f"SELECT name_task FROM tasks WHERE id = {task_id};"
                cursor.execute(old_name)
                self.connection.commit()
                records = cursor.fetchall()
                edit_name_query = f"UPDATE tasks SET name_task = REPLACE(name_task, '{records[0][0]}', '{name}') WHERE id = {task_id};"
                cursor.execute(edit_name_query)
                self.connection.commit()                     
                print("[PIDORAS] Name changed successfully")
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
                
                
    def edit_desc(self, task_id, desc):
        try:
            with self.connection.cursor() as cursor:
                old_desc = f"SELECT task_esse FROM tasks WHERE id = {task_id};"
                cursor.execute(old_desc)
                self.connection.commit()
                records = cursor.fetchall()
                edit_desc_query = f"UPDATE tasks SET task_esse = REPLACE(task_esse, '{records[0][0]}', '{desc}') WHERE id = {task_id};"
                cursor.execute(edit_desc_query)
                self.connection.commit()                     
                print("[PIDORAS] Description changed successfully")
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")
            
    
    def add_user(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                add_user_query = "INSERT INTO users VALUES ({})".format(user_id)
                cursor.execute(add_user_query)
                self.connection.commit()
                
                print("[PIDORAS] User added successfully!")
        except Exception as e:
            print(f"[PIDORAS] An error occurred: {e}")