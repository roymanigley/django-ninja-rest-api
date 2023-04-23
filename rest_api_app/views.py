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