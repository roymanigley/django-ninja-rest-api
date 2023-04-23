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