tasks= []
taskNumber =0

def addTasks():
    global taskNumber
    taskNumber+=1
    description= input("Add new task: ")
    answer=input("did you complete it? y/n: ").strip().lower()
    completed=answer=="y"
    newTask= {"id":taskNumber, "description": description, "completed": completed}
    tasks.append(newTask)
    return newTask

def listTasks():
    for task in tasks:
        status = "completed" if task["completed"] else "Pending"
        print(f"task number: {task['id']}, description: {task['description']}, status: {status}")
    print(" ")
    return tasks

def deleteTask(taskId):
    for task in tasks:
        if task["id"] == taskId:
            tasks.remove(task)
            return
    print("Task deleted")

def main():
    while True:
        print("Welcome to the Task Manager:")
        print("1. Add new task")
        print("2. List all tasks")
        print("3. Delete task")
        print("4. Exit")
        choice = input("choose an option: ")
        if choice == "1": addTasks()
        elif choice == "2": listTasks()
        elif choice == "3": deleteTask(int(input("Enter task number: ")))
        elif choice == "4": break

main()
