tasks = []
task_number = 0

def add_task():
    global task_number

    description = input("Add new task: ").strip()
    if not description:
        print("Task description cannot be empty")
        return

    task_number += 1

    new_task = {
        "id":task_number,
        "description": description,
        "completed": False
    }

    tasks.append(new_task)
    print("Task added")

def list_tasks():
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        status = "completed" if task["completed"] else "Pending"
        print(
            f"task number: {task['id']}, "
            f"description: {task['description']}, "
            f"status: {status}"
        )
    print(" ")

def update_task_status():
    task_id = input("Enter task id: ").strip()

    if not task_id.isdigit():
        print("please enter a valid task id")
        return
    task_id = int(task_id)

    for task in tasks:
        if task["id"] == task_id:
            status = input("enter status (completed/pending): ").strip().lower()

            if status == "completed":
                task["completed"] = True
                print("Task marked as completed")
                return

            elif status == "pending":
                task["completed"] = False
                print("Task marked as pending")
                return

            else:
                print("Invalid status. Please choose completed or pending")
                return
    print("Task not found")

def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            print("Task deleted")
            return

    print("Task not found")

def main():
    print("Welcome to the Task Manager:")

    while True:
        print("1. Add new task")
        print("2. List all tasks")
        print("3. Delete task")
        print("4. Update task status")
        print("5. Exit")

        choice = input("choose an option: ").strip()

        if choice == "1":
            add_task()

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            task_id = input("Enter task id: ").strip()
            if not task_id.isdigit():
                print("please enter a valid task id")
                continue

            delete_task(int(task_id))

        elif choice == "4":
            update_task_status()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again")


if __name__ == "__main__":
    main()
