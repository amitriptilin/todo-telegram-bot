from db.db import PIDORAS


_tasks = []

class To_Do(PIDORAS):    
    def _delete_to_task(self, task_id) -> str:
        tasks = self.read_tasks()
        self.delete_task(task_id)
        return "Задача успешно удалена"
    
    def _delete_all_tasks(self) -> str:
        tasks = self.read_tasks()
        self.holy_hand_grenade()
        return "HOLY HAND GRENADE"
    
    def _change_to_bool(self, task_id) -> str:
        self.done_task(task_id)
        return "Состояние задачи изменено"

    def _dick_Balls(self, data) -> str:
        _tasks = data
        return
    
    def _edit_to_Name(self, task_id, title = None) -> str:
        self.edit_name(task_id = task_id, name = title)
        
    def _edit_to_Desc(self, task_id, desc = None) -> str:
        self.edit_desc(task_id = task_id, desc = desc)

    def _edit_to_Task(self, task_id, title = None, desc = None) -> str:
        tasks = self.read_tasks()
        if title:
            self._edit_to_Name(task_id = task_id, title = title)
        if desc:
            self._edit_to_Desc(task_id = task_id, desc = desc)
        return 'Задача успешно обновлена'
        
    def is_tasks(self, task_id):
        try:
            tasks = self.read_tasks()
            tasks[int(task_id)]
            return {'text': 'Такой номер есть', 'Error': False}
        except ValueError:
            return {'text': 'Введите число', 'Error': True}
        except IndexError:
            return {'text': 'Задачи под таким номером не существует', 'Error': True}
        
    def _write_to_tasks(self, data, user_id) -> str:
        self.add_task(name=data["title"], desc=data["desc"], user_id=user_id)
        return "Задача успешно добавлена"
            
    def log_To_Screen(self) -> str:
        tasks = self.read_tasks()
        output = ""

        def bool_Check(done):
            if done:
                return "Выполнено"
            else:
                return "Не выполнено"
        output += "================\n"
        if tasks:
            for item in range(len(tasks)):
                if item:
                    output += "---------------\n"
                output += f'№ {tasks[item]["task_id"]}\n'
                output += f'Название задачи: {tasks[item]["title"]}\n'
                output += f'Суть задачи: {tasks[item]["desc"]}\n'
                output += f'Состояние задачи: {
                    bool_Check(tasks[item]["done"])}\n'
        else:
            output += "Задач нет\n"

        output += "================\n"
        return output
    
    def create_New_Task(self, new_Task, user_id) -> str:
        output = self._write_to_tasks(new_Task, user_id)
        return output

    def return_arr_len(self) -> int:
        return len(self.read_tasks())
    
    def delete_Task(self, task_id) -> str:
        try:
            output = self._delete_to_task(int(task_id['task_id']))
            return {'text': output, 'Error': False}
        except ValueError:
            return {'text': 'Введите число', 'Error': True}
        except IndexError:
            return {'text': 'Задачи под таким номером не существует', 'Error': True}
        
    def change_Bool(self, task_id) -> str:
        try:
            output = self._change_to_bool(int(task_id['task_id']))
            return {'text': output, 'Error': False}
        except ValueError:
            return {'text': 'Введите число', 'Error': True}
        except IndexError:
            return {'text': 'Задачи под таким номером не существует', 'Error': True}
        
    def edit_Task(self, task_id, title = None, desc = None) -> str:
        try:
            output = self._edit_to_Task(task_id, title, desc)
            return {'text': output, 'Error': False}
        except IndexError:
            return {'text': 'Задачи под таким номером не существует', 'Error': True}