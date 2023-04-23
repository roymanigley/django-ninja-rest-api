# Django Ninja REST API

## Setup

    # set up the venv and add the dependencies
    python3 -m venv .env
    source .env/bin/activate
    pip install django django-ninja

    # initialize the project and the app
    django-admin startproject rest_api_project .
    python3 manage.py startapp rest_api_app

    # create requirements.txt
    pip freeze > requirements.txt

## Configurations

Add the `rest_api_app` to the `INSTALLED_APPS` array in the `rest_api_project/settings.xml` file  

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_api_app'
]
```

## Create Model

create the models in `rest_api_app/models.py`

```python
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return 'Department [name: {}]'.format(self.name)

class Employee(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'Department [first_name: {}, last_name: {}, department: {}]'\
            .format(self.first_name, self.last_name, self.department.name)
```
## Setup the database

setup the database by running `python3 ./manage.py migrate --run-syncdb`

## Link the models to the admin page

register the models in the `rest_api_app/admin.py` file


```python
from django.contrib import admin
from .models import Department, Employee

admin.site.register(Department)
admin.site.register(Employee)
```

## Add an admin user

    python3 manage.py createsuperuser 
    Username (leave blank to use 'user'): admin
    Email address: admin@admin.local
    Password: 
    Password (again):

## Create REST endpoints

define the schemas (dtos) and the rest endpoints in the `rest_api_app/views.py` file


```python
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from typing import List
from .models import Department, Employee

api = NinjaAPI()

class DepartmentSchemaOut(Schema):
    id: int = None
    name: str

class DepartmentSchemaIn(Schema):
    name: str

class EmployeeSchemaOut(Schema):
    id: int
    first_name: str
    last_name: str
    department: DepartmentSchemaOut = None

class EmployeeSchemaIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None

@api.get("department", response={ 200 : List[DepartmentSchemaOut] })
def get_departments(request):
    return Department.objects.all()

@api.get("department/{id}", response={ 200 : DepartmentSchemaOut })
def get_department_by_id(request, id):
    return get_object_or_404(Department, id=id)

@api.post("department", response={ 201: DepartmentSchemaOut })
def create_department(request, payload: DepartmentSchemaIn):
    department = Department.objects.create(**payload.dict())
    return department

@api.put("department/{id}", response={ 200: DepartmentSchemaOut })
def update_department(request, id: int, payload: DepartmentSchemaIn):
    department = get_object_or_404(Department, id=id)
    for attr, value in payload.dict().items():
        if attr != "id":
            setattr(department, attr, value)
    department.save()
    return department

@api.delete("department/{id}", response={203 : None})
def delete_department(request, id: int):
    department = get_object_or_404(Department, id=id)
    department.delete()
    return 203


@api.get("employee", response={ 200 : List[EmployeeSchemaOut] })
def get_employees(request):
    return Employee.objects.all()

@api.get("employee/{id}", response={ 200 : EmployeeSchemaOut })
def get_employee_by_id(request, id):
    return get_object_or_404(Employee, id=id)

@api.post("employee", response={ 201: EmployeeSchemaOut })
def create_employee(request, payload: EmployeeSchemaIn):
    employee = Employee.objects.create(**payload.dict())
    return employee

@api.put("employee/{id}", response={ 200: EmployeeSchemaOut })
def update_employee(request, id: int, payload: EmployeeSchemaIn):
    employee = get_object_or_404(Employee, id=id)
    for attr, value in payload.dict().items():
        if attr != "id":
            setattr(employee, attr, value)
    employee.save()
    return employee

@api.delete("employee/{id}", response={203 : None})
def deleteEmployee(request, id: int):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return 203
```

## Define the routes

define the route in `rest_api_project/urls.py`

```python
from django.contrib import admin
from django.urls import path
from rest_api_app.views import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
```

## Create tests

define the tests in the `rest_api_app/tests.py` file

```python
from django.test import TestCase
from django.test import Client
import json
from .models import Department

class DepartmentsTest(TestCase):
    def set_up(self):
        # Every test needs a client.
        self.client = Client()

    def test_get_departments(self):
        # Create record in DB
        Department.objects.create(**{ "name": "IT" })
        # Issue a GET request.
        response = self.client.get('/api/department')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json()[0].get("name"), "IT")

    def test_get_departments_should_return_empty_list(self):
        # Issue a GET request.
        response = self.client.get('/api/department')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json(), [])


    def test_get_department_by_id(self):
        # Create record in DB
        id = Department.objects.create(**{ "name": "IT" }).id
        # Issue a GET request.
        response = self.client.get('/api/department/{}'.format(id))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json().get("name"), "IT")
        self.assertEqual(response.json().get("id"), id)

    def test_create_department(self):
        # Issue a GET request.
        response = self.client.post('/api/department', json.dumps({ 'name': 'IT' }), content_type='application/json')
        # Check that the response is 201 Created.
        self.assertEqual(response.status_code, 201)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json().get("name"), "IT")
        id = response.json().get("id")
        self.assertIsNotNone(id)
        # check the value in the database
        department = Department.objects.filter(id=id).first()
        self.assertIsNotNone(department)
        self.assertEqual(getattr(department, "name"), "IT")


    def test_create_department_invalid(self):
        # Issue a GET request.
        response = self.client.post('/api/department', json.dumps({ 'name': None }), content_type='application/json')
        # Check that the response is 201 Created.
        self.assertEqual(response.status_code, 422)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json().get("detail")[0].get("msg"), "none is not an allowed value")

    def test_update_department(self):
        # Create record in DB
        id = Department.objects.create(**{ "name": "IT" }).id
        # Issue a GET request.
        response = self.client.put('/api/department/{}'.format(id), json.dumps({ 'name': 'HR' }), content_type='application/json')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json().get("name"), "HR")
        # check the value in the database
        department = Department.objects.filter(id=id).first()
        self.assertIsNotNone(department)
        self.assertEqual(getattr(department, "name"), "HR")

    def test_update_department_no_existing(self):
        # Define non existing id
        id = 999
        # Issue a GET request.
        response = self.client.put('/api/department/{}'.format(id), json.dumps({ 'name': 'HR' }), content_type='application/json')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 404)
        # Check that the rendered json contains expected data.
        self.assertEqual(response.content.decode(), '{"detail": "Not Found"}')

    def test_delete_department(self):
        # Create record in DB
        id = Department.objects.create(**{ "name": "IT" }).id
        # Issue a GET request.
        response = self.client.delete('/api/department/{}'.format(id))
        # Check that the response is 203 Accepted.
        self.assertEqual(response.status_code, 203)
        # check the value in the database
        department = Department.objects.filter(id=id).first()
        self.assertIsNone(department)

    def test_delete_department(self):
        # Define non existing id
        id = 999
        # Issue a GET request.
        response = self.client.delete('/api/department/{}'.format(id))
        # Check that the response is 203 Accepted.
        self.assertEqual(response.status_code, 404)
        # Check that the rendered json contains expected data.
        self.assertEqual(response.content.decode(), '{"detail": "Not Found"}')
```

## Run the Tests

    python3 ./manage.py test

## Run the App

    python3 ./manage.py runserver

## URLs:

- [Admin Panel](http://localhost:8000/admin/)
- [Swagger](http://localhost:8000/api/docs)
- [Departments API](http://localhost:8000/api/department)
- [Employees API](http://localhost:8000/api/employee)

## Sources

[django-ninja: CRUD tutorial](https://django-ninja.rest-framework.com/tutorial/other/crud/)