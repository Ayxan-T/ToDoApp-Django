# ToDo Web Application built with Python Django

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