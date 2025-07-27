# RESTful API for ToDo App built with Django REST Framework (DRF)
## How to run?
### 1. Clone the repository
`git clone https://github.com/Ayxan-T/ToDoApp-Django.git
cd ToDoApp-Django/ToDoList`
### 2. Install dependencies
`pip install -r requirements.txt`
### 3. Apply migrations
`python manage.py migrate`
### 4. Start the server
`python manage.py runserver`

And the API is accessible at `http://localhost:8000/` (via web browser, Postman, etc.)

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
