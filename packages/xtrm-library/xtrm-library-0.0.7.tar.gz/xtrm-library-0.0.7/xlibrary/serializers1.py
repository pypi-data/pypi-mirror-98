from rest_framework import serializers
from xtrm_drest.serializers import (
    DynamicModelSerializer,
    DynamicRelationField
)
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
#from datetime import date
class ExtraFieldsSerializer(serializers.ModelSerializer):
    # vdate=serializers.SerializerMethodField('getDate')
    # def getDate(self,*args,**kwargs):
    #     return date.today()
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ExtraFieldsSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
    class Meta:
        # extra_fields=['vdate']
        # read_only_fields=('vdate')
        abstract=True

class NumericField(serializers.DecimalField):
    """
    We wanted to be able to receive an empty string ('') for a decimal field
    and in that case turn it into a None number
    """
    def to_internal_value(self, data):
        if data == '':
            return None

        return super(NumericField, self).to_internal_value(data)


class ContenttypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    # permissions = DynamicRelationField("PermissionSerializer", many=True)

    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # groups = DynamicRelationField(GroupSerializer, writable=True, many=True)
    # user_permissions = DynamicRelationField("PermissionSerializer", writable=True, many=True)
    # user_permission=serializers.SerializerMethodField('get_group_permissions')
    # def get_group_permissions(user):
    #       if user.is_superuser:
    #           return Permission.objects.all()
    #       return user.get_group_permissions()
    class Meta:

        model = User
        exclude = ('password',)

class PermissionSerializer(serializers.ModelSerializer):
    # content_type = DynamicRelationField("ContenttypeSerializer")
    class Meta:
        model = Permission
        fields = '__all__'