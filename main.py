from datetime import date

#---------- classes for the task it self -------
class Task:
    def __init__(self, task_id, description, completed=False):
        self.task_id = task_id
        self.description = description
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def get_extra_display_info(self, today=None):
        return ""

    def get_warning_message(self, today=None):
        return None

class DeadlineTask(Task):
    def __init__(self, task_id, description, due_date, completed=False):
        super().__init__(task_id, description, completed)
        self.due_date = due_date

    def is_overdue(self, today=None):
        if self.completed:
            return False
        if today is None:
            today = date.today()
        return today > self.due_date

    def get_extra_display_info(self, today=None):
        overdue_label = " (OVERDUE)" if self.is_overdue(today) else ""
        return f", Due: {self.due_date.isoformat()}{overdue_label}"

    def get_warning_message(self, today=None):
        if self.is_overdue(today):
            return f"Warning: '{self.description}' due date is overdue"
        return None

#-----------------------------------------------

#---------- factory method classes -------------

class TaskFactory:
    extra_fields = []

    def create_task(self, task_id, description, **kwargs):
        raise NotImplementedError

class NormalTaskFactory(TaskFactory):
    extra_fields = []

    def create_task(self, task_id, description, **kwargs):
        return Task(task_id, description)

class DeadlineTaskFactory(TaskFactory):
    extra_fields = [
        {"name": "due_date", "prompt": "Due date (YYYY-MM-DD): ", "parse": date.fromisoformat},
    ]
    def create_task(self, task_id, description, due_date=None, **kwargs):
        if due_date is None:
            raise ValueError("DeadlineTask requires a due date")
        return DeadlineTask(task_id, description, due_date)

#---------------------------------------------

#---------- observer pattern classes ----------
class TaskObserver:
    def on_task_added(self, task):
        pass
    def on_task_status_changed(self, task, previous_status):
        pass
    def on_task_deleted(self, task):
        pass

class TaskLogger(TaskObserver):
    def __init__(self):
        self.events = []

    def on_task_added(self, task):
        self.events.append(f"Added task {task.task_id}")

    def on_task_status_changed(self, task, previous_status):
        self.events.append(f"Task {task.task_id} status changed from {previous_status}")

    def on_task_deleted(self, task):
        self.events.append(f"Deleted task {task.task_id}")

#----------------------------------------------

class TaskManager:
    def __init__(self):
        self.tasks = []
        self._next_task_id = 1
        self._task_factories = {
            "normal": NormalTaskFactory(),
            "deadline": DeadlineTaskFactory(),
        }
        self._observers = []

    def get_factory(self, task_type):
        factory = self._task_factories.get(task_type)
        if factory is None:
            raise ValueError(f"Unknown task type: {task_type}")
        return factory

    def add_observer(self, observer):
        self._observers.append(observer)

    def _notify_task_added(self, task):
        for observer in self._observers:
            observer.on_task_added(task)

    def _notify_task_status_changed(self, task, previous_status):
        for observer in self._observers:
            observer.on_task_status_changed(task, previous_status)

    def _notify_task_deleted(self, task):
        for observer in self._observers:
            observer.on_task_deleted(task)

    def add_task(self, description, task_type="normal", **kwargs):
        factory = self.get_factory(task_type)
        new_task = factory.create_task(self._next_task_id, description, **kwargs)
        self._next_task_id += 1
        self.tasks.append(new_task)
        self._notify_task_added(new_task)

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

        previous_status = "completed" if task.completed else "pending"
        if status == "completed":
            task.mark_completed()
        else:
            task.mark_pending()

        self._notify_task_status_changed(task, previous_status)
        return True

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self._notify_task_deleted(task)
        return True

class TaskManagerApp(TaskObserver):
    def __init__(self):
        self.manager = TaskManager()
        self.logger = TaskLogger()

        self.manager.add_observer(self)
        self.manager.add_observer(self.logger)

        self.menu_actions = {
            "1": self.handle_add_task,
            "2": self.handle_list_tasks,
            "3": self.handle_delete_task,
            "4": self.handle_update_status,
        }

    def _warn_if_overdue(self, task):
        warning = task.get_warning_message()
        if warning is not None:
            print(f"{warning}\n")

    def on_task_added(self, task):
        print("Task added\n")
        self._warn_if_overdue(task)

    def on_task_status_changed(self, task, previous_status):
        new_status = "Completed" if task.completed else "Pending"
        print(f"Task status updated: {previous_status.capitalize()} -> {new_status}\n")
        self._warn_if_overdue(task)

    def on_task_deleted(self, task):
        print("Task deleted\n")

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
            if action is not None:
                action()
            else:
                print("Invalid option, please try again\n")

    def handle_add_task(self):
        description = input("\nAdd new task: ").strip()
        if not description:
            print("Task description cannot be empty")
            return

        task_type = self.get_valid_task_type()
        if task_type is None:
            return

        try:
            factory = self.manager.get_factory(task_type)
        except ValueError as error:
            print(f"{error}\n")
            return

        extra_kwargs = self.collect_extra_fields(factory)
        if extra_kwargs is None:
            return

        try:
            self.manager.add_task(description, task_type=task_type, **extra_kwargs)
        except ValueError as error:
            print(f"{error}\n")

    def collect_extra_fields(self, factory):
        extra_kwargs = {}
        for field in factory.extra_fields:
            raw_value = input(field["prompt"]).strip()
            try:
                extra_kwargs[field["name"]] = field["parse"](raw_value)
            except ValueError:
                print("Invalid input format\n")
                return None
        return extra_kwargs

    def handle_list_tasks(self):
        tasks = self.manager.list_tasks()

        if not tasks:
            print("No tasks found")
            return
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            line = (
                f"Task ID: {task.task_id}, "
                f"Description: {task.description}, "
                f"Status: {status}"
            )
            line += task.get_extra_display_info()
            print(line)

    def handle_delete_task(self):
        if not self.manager.tasks:
            print("No tasks found")
            return

        task_id = self.get_valid_task_id()
        if task_id is None:
            return

        success = self.manager.delete_task(task_id)
        if not success:
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
        if not success:
            print("Task not found")

    def get_valid_task_id(self):
        task_id = input("Task ID: ").strip()
        if not task_id.isdigit() or int(task_id) <= 0:
            print("Invalid task ID\n")
            return None
        return int(task_id)

    def get_valid_task_type(self):
        task_type = input("Task type (normal/deadline): ").strip().lower()
        if task_type not in ["normal", "deadline"]:
            print("Invalid task type\n")
            return None
        return task_type


if __name__ == "__main__":
    app = TaskManagerApp()
    app.start()
