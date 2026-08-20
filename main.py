class Task:
    def __init__(self, task_id, description, completed):
        self.task_id = task_id
        self.description = description
        self.completed = completed

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.task_number = 0

    def add_task(self):
        description = input("Add new task: ").strip()

        if not description:
            print("Task description cannot be empty")
            return

        self.task_number += 1

        new_task = Task (
            self.task_number,
            description,
            completed = False
        )

        self.tasks.append(new_task)
        print("Task added")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found")
            return

        for task in self.tasks:
            status = "completed" if task.completed else "Pending"
            print(
                f"task number: {task.task_id}, "
                f"description: {task.description}, "
                f"status: {status}"
            )
        print(" ")

    def update_task_status(self):
        task_id = input("Enter task id: ").strip()

        if not task_id.isdigit():
            print("please enter a valid task id")
            return
        task_id = int(task_id)

        for task in self.tasks:
            if task.task_id == task_id:
                status = input("enter status (completed/pending): ").strip().lower()

                if status == "completed":
                    task.completed = True
                    print("Task marked as completed")
                    return

                elif status == "pending":
                    task.completed = False
                    print("Task marked as pending")
                    return

                else:
                    print("Invalid status. Please choose either 'completed' or 'pending")
                    return
        print("Task not found")

    def delete_task(self):
        task_id = input("Enter task id: ").strip()
        if not task_id.isdigit():
            print("please enter a valid task id")
            return
        task_id = int(task_id)

        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                print("Task deleted\n")
                return
        print("Task not found")

class Main():
    def __init__(self):
        self.manager = TaskManager()

    def start(self):
        print("Welcome to the Task Manager:")

        while True:
            print("1. Add new task")
            print("2. List all tasks")
            print("3. Delete task")
            print("4. Update task status")
            print("5. Exit")

            choice = input("choose an option: ").strip()

            if choice == "1":
                self.manager.add_task()

            elif choice == "2":
                self.manager.list_tasks()

            elif choice == "3":
                self.manager.delete_task()

            elif choice == "4":
                self.manager.update_task_status()

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option, please try again")


if __name__ == "__main__":
    main = Main()
    main.start()
