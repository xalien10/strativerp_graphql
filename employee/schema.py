import graphene

from graphene_django.types import DjangoObjectType

from employee.models import Employee


class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee


class Query(object):
    all_employees = graphene.List(EmployeeType)
    all_admins = graphene.List(EmployeeType)
    all_non_admins = graphene.List(EmployeeType)

    def resolve_all_employees(self, info, **kwargs):
        return Employee.objects.all()
