from tabulate import tabulate
from datetime import datetime
import sys

tasks = []
completed = []

def main():
    options = [['Add Task', '1'], ['Complete Task', '2'], ['Show Tasks', '3'], ['View Completed Tasks', '4'], ['Exit Program', '5']]
    print('◾◾' * 32)
    print("Automated To Do list Specially Programmed to Improve your Productivity: \nMade By: Johnson Y.")
    print('◾◾' * 32)
    print(' ')
    print('             Main Menu')
    tries = 0
    while True:
        print(tabulate(options, headers=['Choices: ', 'Actions'], tablefmt="grid"))
        choice = input("Action (1, 2, 3, 4 or 5): ")
        print('\n\n')
        if choice == '1':
            add_task()
        elif choice == '2':

            complete_task()
        elif choice == '3':
            print("*" * 36)
            print("Showing Tasks")
            print("-" * 36)
            show_tasks()
            print("*" * 36)
            action_ = input('Return to Menu? (y/n): ')
            if action_ in ['Y', 'y', 'yes', 'Yes']:
                print("\n" * 19)
                print('Main Menu')
            else:
                print('Exiting Program...')
                sys.exit()
        elif choice == '4':
            view_completed()
        elif choice == '5':
            print("Exiting Program...")
            sys.exit()
        elif choice == '69':
            print("Skibidi rizzllleer")
            sys.exit()
        else:
            if tries == 3:
                print('Exiting Program...')
                break
            print('Please input an existing choice (1, 2, 3, 4 or 5): ')
            tries += 1

def add_task():
    print("\n"*30)
    print("*" * 36)
    print("Add Tasks")
    print("-" * 36)
    inputs = 0
    inputs2 = 0
    input3 = 0
    while True:
        description = input("Task Description: ")
        if not description:
            if inputs > 2:
                print("*" * 36)
                print("\n" * 20)
                print('Main Menu')
                return
            print('Description Required\n')
            inputs += 1
            continue

        time_needed = input("\nTime Needed for Task (eg. 20 minutes, 1 hour etc.): ")
        if not time_needed:
            time_needed = 'N/A'

        priority = input("\nTask Priority (1 as most urgent, 2 as urgent, and 3 as not urgent): ")
        if not priority.isdigit() or priority not in ['1', '2', '3']:
            if inputs2 > 2:
                print("*" * 36)
                print("\n" * 29)
                print('Main Menu')
                return
            print('Please input 1, 2, or 3.')
            inputs2 += 1
            continue
        priority = int(priority)

        date = input("\nTask Due Date (MM/DD format): ")
        try:
            current_year = datetime.today().year
            due_date = datetime.strptime(f"{date}/{current_year}", "%m/%d/%Y").date()
            today = datetime.today().date()
            if today > due_date:
                print('Invalid Date (That date is in the past)')
                input3 += 1
                continue
        except ValueError:
            print('Please input the due date in the format of MM/DD')
            input3 += 1
            continue

        task_dict = {'description': description, 'time': time_needed, 'priority': priority, 'date': due_date, 'completed': 'no'}
        tasks.append(task_dict)
        print('\nSuccessfully Added Task to your To Do list.')
        print("*" * 36)
        action_ = input('Return to Menu? (y/n): ')
        if action_ in ['Y', 'y', 'yes', 'Yes']:
            print("\n" * 10)
            print('Main Menu')
            break
        else:
            print('Exiting Program...')
            sys.exit()

def complete_task():
    print("\n"*15)
    print("*" * 36)
    print("Updating Tasks")
    print("-" * 36)

    if not tasks:
        print("No tasks to complete.")
        return

    show_list = []
    show_list.append(['Task Number','Task Description','Time Needed', 'Task Due Date', 'Task Priority'])
    for i, task in enumerate(tasks, start=1):
        show_list.append([str(i), task['description'], task['time'], task['date'].strftime('%m/%d'), str(task['priority'])])
    print(tabulate(show_list, headers='firstrow', tablefmt="grid"))

    while True:
        try:
            task_number = int(input("Enter the number of the task you completed: "))
            if 1 <= task_number <= len(tasks):
                break
            else:
                print(f"Please enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("Please enter a valid number.")

    completed_task = tasks.pop(task_number - 1)
    completed_task['completed'] = 'yes'

    now = datetime.today()
    formatted_date = now.strftime('%-m/%-d %-I:%M%p').lower()
    completed_task['date'] = formatted_date

    with open("completed_tasks.txt", "a") as file:
        file.write(f'Description: "{completed_task["description"]}", Time Spent: {completed_task["time"]}, Priority: {completed_task["priority"]}, Date Finished: {completed_task["date"]}, Completed: ✅\n')

    completed.append(completed_task)
    print(f"Task '{completed_task['description']}' marked as completed.")
    print("*" * 36)
    action_ = input('Return to Menu? (y/n): ')
    if action_ in ['Y', 'y', 'yes', 'Yes']:
        print("\n" * 10)
        print('Main Menu')
    else:
        print('Exiting Program...')
        sys.exit()

def view_completed():
    print("🎉✨💯" * 12)
    print("View Completed Tasks")
    print("-" * 36)
    if completed:
        complete_list = []
        complete_list.append(['Task Description', 'Time Spent', 'Date Finished', 'Task Priority', 'Completed'])
        for task in completed:
            complete_list.append([task['description'], task['time'], task['date'], str(task['priority']), '✅'])
        print(tabulate(complete_list, headers='firstrow', tablefmt="grid"))
        print("🎉✨💯" * 12)
    else:
        print("There are currently no tasks completed.")
    action_ = input('Return to Menu? (y/n): ')
    if action_ in ['Y', 'y', 'yes', 'Yes']:
        print("\n" * 20)
        print('Main Menu')
    else:
        print('Exiting Program...')
        sys.exit()

def show_tasks():
    sorted_tasks = sorted(tasks, key=lambda x: (x['date'], x['priority']))

    tasks_by_date = {}
    for task in sorted_tasks:
        date_str = task['date'].strftime("%m/%d/%Y")
        if date_str not in tasks_by_date:
            tasks_by_date[date_str] = []
        tasks_by_date[date_str].append([task['description'], task['time'], task['priority'], date_str, task['completed']])

    combined_table_data = [['Description', 'Time Needed', 'Priority', 'Due Date', 'Completed']]
    for date, tasks_list in tasks_by_date.items():
        combined_table_data.extend(tasks_list)

    print(tabulate(combined_table_data, headers='firstrow', tablefmt="grid"))

if __name__ == "__main__":
    main()