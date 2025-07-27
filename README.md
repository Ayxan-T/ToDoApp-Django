# RESTful API for ToDo App built with Django REST Framework (DRF)
ToDoList is a simple RESTful API built using Django REST Framework (DRF). It provides basic task management functionality through two separate Django apps: users and tasks.  
The users app handles:
- User registration
- User authentication
- JWT-based token management (login, refresh)

The tasks app allows authenticated users to:
- Create, read (with pagination), update, and delete their tasks
- Filter tasks by status
- Mark tasks as completed

Each app has its own model: User and Task, designed to interact cleanly through DRF's serializer and view layers.
## Database connection
The project is configured to use a PostgreSQL database by default, as defined in ToDoList/settings.py:  
    `DATABASES = {  "default": {  "ENGINE": "django.db.backends.postgresql",   ... `

For your convenience, an alternative SQLite3 configuration is also included but commented out in the same file. This enables easier local testing without the need for a PostgreSQL setup.

## How to run
Cloning the repository, installing dependencies (mentioned in requirements.txt), and applying migrations (building db tables)  
`git clone https://github.com/Ayxan-T/ToDoApp-Django.git`  
`cd ToDoApp-Django/ToDoList`  
`pip install -r requirements.txt`  
`python manage.py migrate`

And the server is ready to be started:  
`python manage.py runserver`

The API can be accessed at `http://localhost:8000/` (via web browser, Postman, etc.)

## 3 Implement CRUD (Create, Read, Update, Delete) operations for tasks
The requirement "Get a list of all tasks" did not specify whether this endpoint should be publicly accessible or restricted. I interpreted it as an administrative function. Since Django’s built-in admin panel already provides full access to all tasks for admin users, I opted to comment out the API endpoint for listing all tasks to avoid exposing data unnecessarily.

## 8. Configuring database connection to PostgreSQL database


## Future ideas
Adding logout functionality -> adding refresh token to blocklist
