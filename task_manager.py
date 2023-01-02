#=====importing libraries===========
import datetime
import textwrap

users_dict = {}
tasks_list = []

def refresh_users_dict():
    # This will sort all the usernames and passwords in users.txt into a dictionary for easy access.
    with open('user.txt', 'r') as users_file:
        for line in users_file:
            username_and_password = line.split(', ')
            users_dict.update({username_and_password[0] : username_and_password[1].strip('\n')})

# This function will order all tasks into a list
def tasks_file_to_2d_list():
    tasks_list = []
    with open('tasks.txt', 'r') as tasks_file:
        for line in tasks_file:
            tasks_list.append(line.split(", "))
    return tasks_list

# This function will rewrite all the task_list back into the tasks file
def write_tasks_to_file(task_2d_list):
    with open('tasks.txt', 'w') as task_file:
        for task in task_2d_list:
            task_file.write(f"{task[0]}, {task[1]}, {task[2]}, {task[3]}, {task[4]}, {task[5]}")

# This will take a task as an input and display it to the screen in an easy to read format.
def task_list_to_output_format(task):
    # Each line will have 50 characters
    print("-" * 50)
    # If the title is above a certain amount of characters it will be printed to a new line to ensure the format stays neat
    if len(task[1]) <= 27:
        print(f"Task: {' '*17}{task[1]}")
    else:
        print(f"Task: \n{task[1]}\n")
    print(f"Assigned to: {' '*10}{task[0]}")
    print(f"Date assigned: {' '*8}{task[3]}")
    print(f"Due date: {' '*13}{task[4]}")
    completion_stripped = task[5].strip('\n')
    print(f"Task complete? {' '*8}{completion_stripped}")
    print(f"Task description: \n")
    # This will wrap the secription text so that it stay inside the box provided and the format remains clean.
    for line in (textwrap.wrap(task[2], width = 50)):
        print(line)
    print("-" * 50)

# Creates statistics on the tasks and writes them to a file.
def task_overview():
    # Refreshing the tasks_list to ensure the tasks are up to date in the programme
    tasks_list = tasks_file_to_2d_list()
    total_tasks = 0
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    # Loops through the tasks_list tallying up when the task is complete, incomplete or overdue.
    for task in tasks_list:
        total_tasks += 1
        if task[5].strip("\n").lower() == "yes":
            completed_tasks += 1
        if task[5].strip("\n").lower() == "no":
            incomplete_tasks += 1
            # This will convert the task due date to a datetime value and compare it to today.
            if datetime.datetime.strptime(task[4].lower(),'%d %b %Y') < datetime.datetime.today():
                overdue_tasks += 1
    
    # Calculates the percentages of overdue and incomplete tasks compared to the total amount of tasks.
    percent_incomplete = (incomplete_tasks / total_tasks) * 100
    percent_overdue = (overdue_tasks / incomplete_tasks) * 100
    
    # Writes the results to a file in an easy to read format
    with open('task_overview.txt', 'w+') as task_overview_file:
        task_overview_string = f"Total tasks: {'-' * 27} {total_tasks}\nCompleted tasks: {'-' * 23} {completed_tasks}\nIncomplete tasks: {'-' * 22} {incomplete_tasks}\nTasks overdue: {'-' * 25} {overdue_tasks}\nPercentage of overall tasks incomplete:- {percent_incomplete}%\nPercentage of incomplete tasks overdue:- {percent_overdue}%\n"
        task_overview_file.write(task_overview_string)

# This function creates statistics on each user and writes them to a file called user_overview.txt in an easy to read format.
def user_overview():
    # Calling the tasks_file_to_2d_list and users_statistics functions to make sure the list/dictionary is up to date.
    tasks_list = tasks_file_to_2d_list()
    refresh_users_dict()
    # This next block of code will collect data on each users tasks and add it all to a dictionary. 
    # Each user key will have a dictionary value with data type keys and values.
    users_statistics = {}
    for user in users_dict.keys():
        users_statistics[user] = {'total' : 0, 'complete' : 0, 'incomplete' : 0, 'overdue' : 0}
    for task in tasks_list:
        if task[0] not in users_statistics:
            users_statistics[task[0]]['total'] += 1
        else:
            users_statistics[task[0]]['total'] += 1
        if task[5].lower().strip('\n') == 'yes':
            users_statistics[task[0]]['complete'] += 1
        elif task[5].lower().strip('\n') == 'no':
            users_statistics[task[0]]['incomplete'] += 1
            if datetime.datetime.strptime(task[4].lower(),'%d %b %Y') < datetime.datetime.today():
                users_statistics[task[0]]['overdue'] += 1
    
    # This block of code will loop through each users dictionary value, calculate some percentages and write them to the user_overview file in an easy to read format.
    with open('user_overview.txt', 'w') as user_overview_file:
        for user in users_statistics:
            percent_of_total = (users_statistics[user]['total'] / len(tasks_list)) * 100
            if users_statistics[user]['total'] != 0:
                percent_complete = (users_statistics[user]['complete'] / users_statistics[user]['total']) * 100
                percent_incomplete = (users_statistics[user]['incomplete'] / users_statistics[user]['total']) * 100
                percent_overdue = (users_statistics[user]['overdue'] / users_statistics[user]['total']) * 100
            else:
                percent_complete = "0"
                percent_incomplete = "0"
                percent_overdue = "0"
            
            string = f"User: {user}"
            string += f"\nTasks assigned: -------------------------------------------- {users_statistics[user]['total']}"
            string += f"\nThe percentage of the overall tasks assigned to this user: - {percent_of_total}%"
            string += f"\nThe percentage of the users tasks completed: --------------- {percent_complete}%"
            string += f"\nThe percentage of the users tasks incomplete: -------------- {percent_incomplete}%"
            string += f"\nThe percentage of the users tasks overdue: ----------------- {percent_overdue}%\n"
            user_overview_file.write(string)

# This function will read the user adn task overview files and print them to screen.
def display_statistics():
    print("\nTask report:\n")
    with open('task_overview.txt', 'r') as task_overview_file:
        for line in task_overview_file:
            print(line)
    print("\nUsers overview:\n")
    with open('user_overview.txt', 'r') as user_overview_file:
        for line in user_overview_file:
            print(line)

# This function will ask the admin to enter a username and password, then it will add the new user profile to the user file.
def reg_user():
    username = input("\nPlease enter a username for the new user: ")
    # This will check if a user already has that username.
    if username in users_dict:
        return print("\nThe user already exists, please enter a different username if you want to add someone new.\n")
    # Checks for a comma to prevent any bugs occuring in the program
    elif "," in username:
        return print("\nYou are not allowed to have a comma in the username, please try again.\n")
    password = input("\nPlease enter a new password for the new user: ")
    password_check = input("Please re-enter the password for confirmation: ")
    # This will check the users passwords against each other, if they are the same, the new username password combination will be added to users.txt. 
    # Otherwise an appropriate error will be printed and the user will have the chance to try again.
    if password != password_check:
        print("\nSorry, it seems you have typed in two different passwords, user has not been added to the system. You will be redirected to the menu.\n")
    # Checks for a comma to prevent any bugs occuring in the program
    elif "," in password:
        print("\nYou are not allowed to have a comma in the password, please try again.\n")
    else:
        with open('user.txt', 'a') as user_file:
            user_file.write(f'\n{username}, {password}')
        print('\nUser has successfully been added to the system.\n')
        refresh_users_dict()

# This function takes in the users inputs and adds it to the tasks file.
def add_task():
    user_assigned = input("Who is this task going to be assigned to? Please enter a username: ")
    # Checking if the inputted username exists in the system:
    refresh_users_dict()
    if user_assigned not in users_dict:
        return print("\nUser does not exist in our system. Please try again.\n")
    task_title = input("Please enter a title for the task: ")
    if "," in task_title:
        return print("\nYou are not allowed to use a comma, please try again.\n")
    task_description = input("Please describe the task:\n")
    if "," in task_description:
        return print("\nYou are not allowed to use a comma, please try again.\n")
    due_date = input("Enter the task due date: ")
    #This will tes the users entered due date to see if it is in the correct format and whther the due date is in the past.
    try:
        if datetime.datetime.strptime(due_date, '%d %b %Y') < datetime.datetime.today():
            return print('\nIt seems the due date you entered is in the past. Please try again.\n')
    except:
        print('\nIt seems you have entered a date in the wrong format. Try again.\n')
        return
    if "," in due_date:
        return print("\nYou are not allowed to use a comma, please try again.\n")
        
    # Using the datetime module to acquire the current date then formatting that date inline with the other tasks in tasks.txt
    task_assigned_date = datetime.datetime.today()
    task_assigned_date_list = f"{task_assigned_date:%d, %b, %Y}".split(",")
    task_assigned_date_formatted = ""
    for date_object in task_assigned_date_list:
        task_assigned_date_formatted += date_object
    # Writing the task and the current date into tasks.txt
    with open('tasks.txt', 'a') as tasks:
        tasks.write(f"\n{user_assigned}, {task_title}, {task_description}, {task_assigned_date_formatted}, {due_date}, No")
    print("\nTask has successfully been added to the system.\n")

# This will output all the tasks in the tasks file to the screen in an easy to read format.
def view_all():
    tasks_list = tasks_file_to_2d_list()
    # Loops through each task in tasks.txt and formats it appropriately for the output to the screen.
    for task in tasks_list:
        task_list_to_output_format(task)
    print("")

# This will output all the tasks assigned to the current user in an easy to read format.
def view_mine():
    tasks_list = tasks_file_to_2d_list()
    # The code here will format the output just as it was with the view all tasks option
    user_task_count = 1
    overall_task_index = 0
    users_tasks_indexes = {}
    for task in tasks_list:
        # This will check each task to see if it corresponds to the current user logged in, if it does it will be printed to the screen.
        if task[0] == user:
            if user_task_count == 1:
                print("\nThese are the tasks assigned to you: \n")
            print(f"Task {user_task_count}:")
            task_list_to_output_format(task)
            print()
            users_tasks_indexes.update({str(user_task_count):overall_task_index})
            user_task_count += 1
        overall_task_index += 1
    if user_task_count == 1:
        return print("\nIt seems that you have no tasks assigned to you. Sending you back to main menu.\n")
    # This will loop until the user enters either a 1 or a number corresponding to an existing task.
    while True:
        task_for_edit = input("If you would like to edit a task, please enter the number corresponding to that task. If you do not want to edit a task, enter -1 to exit: ")
        print()
        if task_for_edit == "-1":
            return
        elif int(task_for_edit) > 0 and int(task_for_edit) < user_task_count:
            if tasks_list[users_tasks_indexes[task_for_edit]][5].lower().strip("\n") == "yes":
                print("It seems that task has already been completed, you may only edit incomplete tasks.")
                break
            print("What would you like to change about this task? ")
            task_list_to_output_format(tasks_list[users_tasks_indexes[task_for_edit]])
            edit_options = input("If you would like to mark the task as complete, type \'yes\' here. \nIf you would like to change the due date of the task, type \'dd\'. \nIf you would like to change the user the task is assigned to, type \'user\'. \nType here:  ")
            # Determines the which piece of the task the user would like to edit and when appropriate asks to user to enter the value they would like to change the section to.
            if edit_options.lower() == "yes":
                tasks_list[users_tasks_indexes[task_for_edit]][5] = "Yes"
            elif edit_options.lower() == "dd":
                # This asks the user to enter a value to update the due date with. If the entered value is not in the correct datetime format it will output the appropriate error.
                new_due_date = input("Enter the due date you would like to change the task to: ")
                try:
                    datetime.datetime.strptime(new_due_date, '%d %b %Y')
                except:
                    print('\nIt seems you have entered a date in the wrong format. Try again.\n')
                    continue
                tasks_list[users_tasks_indexes[task_for_edit]][4] = new_due_date
            elif edit_options.lower() == "user":
                reassign_user = input("Enter the username of the user you would like to reassign the task to: ")
                # Checks if the user exists in the system
                refresh_users_dict()
                if reassign_user in users_dict:
                    tasks_list[users_tasks_indexes[task_for_edit]][0] = reassign_user
                else:
                    print("\nIt seems you have entered a non existent user, try again.\n")
                    continue
            else:
                print("\nIt seems you have not entered one of the options given, you may try again.\n")
                continue
            # Rewrites the edited task to the tasks file.
            write_tasks_to_file(tasks_list)
            print("\nTask has been successfully edited\n")
            break
        else:
            print("It seems you have made a mistake somewhere, please try again.\n")


#====Login Section====

# Updates the users_dict with the current usernames and passwords in the user file.
refresh_users_dict()

# This will check the users input against the usernames and passwords that exist, if the user enters incorrectly, the program will output an appropriate error and will ask the user to try again. 
# If the user enters correctly, the program will assign the variable user to the username entered.
while True:
    entered_username = input('Enter the username here: ')
    entered_password = input('Enter the password here: ')

    try:
        if users_dict[entered_username] == entered_password:
            user = entered_username
            print(f'{user} has been successfully logged in.')
            break
        else:
            print('You entered an incorrect password. Please try again: ')
    except:
        print('You entered an invalid username. Please try again: ')



while True:
    # Presenting a different menu to the user depending on whether they are the admin or not.
    if user == "admin":
        # Making sure that the user input is converted to lower case.
        menu = input('''Select one of the following options below:
    r - Registering a user (admin only)
    a - Adding a task
    va - View all tasks
    vm - View my tasks/Edit my tasks
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following options below:
    a - Adding a task
    va - View all tasks
    vm - View my tasks/Edit my tasks
    e - Exit
    : ''').lower()

    if menu == 'r':
        # Checks if it is the admin accessing this function.
        if user == "admin":
            reg_user()
        else:
            print("Unfortunately, only the admin user can register new users. Please restart the program and log in as admin if you want to register someone new.")
        pass

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()
        pass

    elif menu == 'vm':
        view_mine()
        pass

    elif menu == 'ds':
        # This will check if the logged in user is the admin or not.
        if user == 'admin':
            task_overview()
            user_overview()
            display_statistics()
        else:
            print("Only the admin has access to this feature. Please pick another option: ")
    
    elif menu =='gr':
        # Checks if it is the admin accessing this function.
        if user == "admin":
            task_overview()
            user_overview()
        else:
            print("Unfortunately, only the admin user can generate a report. Please restart the program and log in as admin if you want to perform this function.")

    
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again\n")