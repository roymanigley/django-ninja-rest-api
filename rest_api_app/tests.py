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