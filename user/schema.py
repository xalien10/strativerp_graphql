import graphene

from graphene_django.types import DjangoObjectType

from user.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):
    all_users = graphene.List(UserType)
    all_superusers = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_superusers(self, info, **kwargs):

        return User.objects.filter(is_superuser=True)
