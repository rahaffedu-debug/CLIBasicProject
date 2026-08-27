class Task:
    def __init__(self, task_id, description, completed=False):
        self.task_id = task_id
        self.description = description
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.task_number = 0

    def add_task(self, description):
        self.task_number += 1
        new_task = Task(self.task_number, description)
        self.tasks.append(new_task)

    def find_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def list_tasks(self):
        return self.tasks

    def update_task_status(self, task_id, status):
        task = self.find_task(task_id)
        if task is None:
            return False

        if status == "completed":
            task.mark_completed()
        else:
            task.mark_pending()
        return True

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True

class TaskManagerApp:
    def __init__(self):
        self.manager = TaskManager()
        self.menu_actions = {
            "1": self.handle_add_task,
            "2": self.handle_list_tasks,
            "3": self.handle_delete_task,
            "4": self.handle_update_status,
        }

    def start(self):
        print("Welcome to the Task Manager:")
        while True:
            print("1. Add new task")
            print("2. List all tasks")
            print("3. Delete task")
            print("4. Update task status")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "5":
                print("Goodbye!")
                break

            action = self.menu_actions.get(choice)
            if action:
                action()
            else:
                print("Invalid option, please try again")

    def handle_add_task(self):
        description = input("Add new task: ").strip()
        if not description:
            print("Task description cannot be empty")
            return

        self.manager.add_task(description)
        print("Task added")

    def handle_list_tasks(self):
        tasks = self.manager.list_tasks()

        if not tasks:
            print("No tasks found")
            return
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            print(
                f"Task ID: {task.task_id}, "
                f"Description: {task.description}, "
                f"Status: {status}"
            )

    def handle_delete_task(self):
        if not self.manager.tasks:
            print("No tasks found")
            return

        task_id = self.get_valid_task_id()
        if task_id is None:
            return

        success = self.manager.delete_task(task_id)
        if success:
            print("Task deleted\n")
        else:
            print("Task not found")

    def handle_update_status(self):
        if not self.manager.tasks:
            print("No tasks found")
            return

        task_id = self.get_valid_task_id()
        if task_id is None:
            return

        status = input("Update status (Completed/Pending): ").strip().lower()
        if status not in ["completed", "pending"]:
            print("Invalid status. Please choose either 'Completed' or 'Pending'\n")
            return

        success = self.manager.update_task_status(task_id, status)
        if success:
            print(f"Task status updated to: {status}\n")
        else:
            print("Task not found")

    def get_valid_task_id(self):
        task_id = input("Task ID: ").strip()
        if not task_id.isdigit() or int(task_id) <= 0:
            print("Invalid task ID")
            return None
        return int(task_id)

if __name__ == "__main__":
    app = TaskManagerApp()
    app.start()
