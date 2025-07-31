# RESTful API for ToDo App built with Django REST Framework (DRF)
ToDoList is a simple RESTful API built using Django REST Framework (DRF). It provides basic task management functionality through two separate Django apps: `users` and `tasks`.  
The `users` app handles:
- User registration
- User authentication
- JWT-based token management (login, refresh)

The `tasks` app allows authenticated users to:
- Create, read (with pagination), update, and delete their tasks
- Filter tasks by status
- Mark tasks as completed

Each app has its own model: User and Task, designed to interact cleanly through DRF's serializer and view layers.

## Database connection
The project is configured to use a PostgreSQL database by default, as defined in ToDoList/settings.py:  
    `DATABASES = {  "default": {  "ENGINE": "django.db.backends.postgresql",   ... `

For your convenience, an alternative SQLite3 configuration is also included but commented out in the same file. This enables easier local testing without the need for a PostgreSQL setup.

## How to Run
1. Clone the repository  
   `git clone https://github.com/Ayxan-T/ToDoApp-Django.git`
2. Navigate to the project directory  
   `cd ToDoApp-Django/ToDoList`
3. Install dependencies  
   `pip install -r requirements.txt`
4. Apply migrations  
   `python manage.py migrate`
5. Start the server  
   `python manage.py runserver`

The API can be accessed at `http://localhost:8000/` (via web browser, Postman, etc.)

## API Endpoints Overview

### User Endpoints
- `POST /api/users/register/` – Register a new user (required fields: first_name, username, password (Refer to users.models.User))
- `POST /api/users/login/` – Obtain JWT token pair (access & refresh) (required fields: username, password)
- `POST /api/users/token/refresh/` – Refresh access token (required fields: refresh (the refresh token))

### Task CRUD Endpoints 
- `GET /api/tasks/user-tasks/?page=1` – List your tasks (supports pagination, default: page=1)
- `POST /api/tasks/create-task/` – Create a new task
- `GET /api/tasks/<id>/` – Retrieve a specific task
- `PATCH /api/tasks/update-task/<id>/` – Update a task
- `DELETE /api/tasks/delete-task/<id>/` – Delete a task
- `GET /api/tasks/` - List all tasks in db
> The requirement "Get a list of all tasks" did not specify whether this endpoint should be publicly accessible or restricted. I assumed it as an administrative function. Since Django’s built-in admin panel already provides full access to all tasks for admin users, I opted to comment out the API endpoint for listing all tasks to avoid exposing data unnecessarily.

### Additional task endpoints
- Filter tasks by status (new, completed, in_progress):  
    `GET /api/tasks/filter-by-status/<status>`
- Mark a task as completed
    `GET /api/tasks/mark-completed/<id>`

### Authentication
All task endpoints require JWT authentication. Include the access token in the `Authorization` header:
```
Authorization: Bearer <your_access_token>
```

## Serializer Usage
This project uses Django REST Framework serializers to convert Django model instances into native Python datatypes for easy JSON rendering. Each app has its own serializer:

- **UserSerializer**
- **TaskSerializer**

Serializers are located in `users/serializers.py` and `tasks/serializers.py`. They enforce validation rules and control which fields are exposed via the API.

## Decorator Usage
A custom decorator, **@check_authorization**, is used to ensure that only authorized users can access or modify specific resources, such as tasks they own. This decorator encapsulates repeated authorization logic, helping keep views clean and enforcing security rules consistently across the API.

## Running Tests
This project includes unit tests for key API functionality using Django's built-in testing tools and `rest_framework.test.APIClient`.

To run the test suite:  
```
python manage.py test
```

## Future ideas
Adding logout functionality -> adding refresh token to blocklist?

## Updates after Feedback
- Passwords were stored in plain text, which was a security risk.

User model was refactored to inherit from AbstractBaseUser and implement its password hashing functionality

- Pagination in user tasks retrieval was manual.

PageNumberPagination replaced manual pagination.

- Filtering was done via a dedicated endpoint.  

Endpoint for filtering was removed. Filtering is now done thorugh query parameter 'status' of 'get_user_tasks' endpoint.

