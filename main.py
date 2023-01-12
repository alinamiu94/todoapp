import psycopg2


class Task:
    def __init__(self, id, title, description, due_date, priority, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.created_at = created_at

    def __str__(self):
        return self.title + " " + str(self.id)


class TaskRepository:

    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        self.cursor = self.conn.cursor()

    def get_all_tasks(self):
        self.cursor.execute("SELECT *  from Task")
        rows = self.cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(row[0], row[1], row[2], row[3], row[4], row[5])
            tasks.append(task)
        return tasks

    def get_task_by_id(self, id):
        self.cursor.execute("SELECT * FROM task WHERE id = " + str(id))
        rows = self.cursor.fetchall()
        row = rows[0]
        task = Task(row[0], row[1], row[2], row[3], row[4], row[5])
        return task

    def insert_task(self, task):
        self.cursor.execute("INSERT INTO task (id,title,description,due_date,priority,created_at) "
                            "VALUES ({},'{}','{}', '{}', {}, '{}');".format(task.id, task.title, task.description,
                                                                            task.due_date, task.priority,
                                                                            task.created_at))
        self.conn.commit()

    def delete_task_by_id(self, id):
        self.cursor.execute("delete from task where id = {}".format(id))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


taskrepository = TaskRepository("localhost", "todoapp", "postgres", "root")

while True:
    command = input("# ")
    if command == "view_tasks":
        tasks = taskrepository.get_all_tasks()
        for task in tasks:
            print(task)
    if command.startswith("view_task "):
        id = command.split(" ")[1]
        task = taskrepository.get_task_by_id(id)
        print(task)
    if command.startswith("insert_task "):
        details = command.split(" ")
        task = Task(details[1], details[2], details[3], details[4], details[5], details[6])
        taskrepository.insert_task(task)

