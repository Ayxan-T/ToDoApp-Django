# RESTful API for ToDo App built with Django REST Framework (DRF)
## How to run?
Cloning the repository, installing dependencies (mentioned in requirements.txt), and applying migrations (building db tables)
`git clone https://github.com/Ayxan-T/ToDoApp-Django.git  
cd ToDoApp-Django/ToDoList`  
`pip install -r requirements.txt`  
`python manage.py migrate`

And the server is ready to be started:  
`python manage.py runserver`

The API can be accessed at `http://localhost:8000/` (via web browser, Postman, etc.)

## 3 Implement CRUD (Create, Read, Update, Delete) operations for tasks
The requirement "Get a list of all tasks" did not specify whether this endpoint should be publicly accessible or restricted. I interpreted it as an administrative function. Since Django’s built-in admin panel already provides full access to all tasks for admin users, I opted to comment out the API endpoint for listing all tasks to avoid exposing data unnecessarily.

## 8. Configuring database connection to PostgreSQL database
The corresponding code from ToDoList/settings.py:
    `DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "todo_db",
            "USER": "postgres",
            "PASSWORD": "admin",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }`

## Future ideas
Adding logout functionality -> adding refresh token to blocklist
