from rest_framework import serializers
from xtrm_drest.serializers import (
    DynamicModelSerializer,
    DynamicRelationField
)
# from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
# from .models import User, GroupOptions
from .models import GroupOptions
from django.contrib.auth import get_user_model
User=get_user_model()
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


class ContenttypeSerializer(DynamicModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'

class GroupSerializer(DynamicModelSerializer):
    permissions = DynamicRelationField("PermissionSerializer", many=True)
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(DynamicModelSerializer):
    groups = DynamicRelationField(GroupSerializer,many=True)
    class Meta:

        model = User
        exclude=('user_permissions','password',)

class PermissionSerializer(DynamicModelSerializer):
    content_type = DynamicRelationField("ContenttypeSerializer")
    class Meta:
        model = Permission
        fields = '__all__'

class GroupOptionsSerializer(DynamicModelSerializer):
    groups=DynamicRelationField(GroupSerializer, writable=True)
    class Meta:
        model = GroupOptions
        fields = '__all__'

class CUserSerializer(serializers.ModelSerializer):
    group_id=serializers.CharField(write_only=True)

    class Meta:
        exclude = ('user_permissions',)
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_id = validated_data.pop('group_id', None)
        user = User.objects.create(**validated_data)
        user.is_active=True
        user.is_superuser = False
        if group_id=="2":
            user.is_staff=False
        else:
            user.is_staff=True
        user.set_password(validated_data['password'])
        user.groups.add(group_id)
        user.save()
        return user

    def update(self, instance, validated_data):
        group_id = validated_data.pop('group_id', None)
        user = super(CUserSerializer,self).update(instance, validated_data)
        user.is_superuser = False
        if group_id==2:
            user.is_staff=False
        else:
            user.is_staff=True
        user.groups.clear()
        user.groups.add(group_id)
        user.save()
        return user

class CGroupSerializer(serializers.ModelSerializer):
    privilege=serializers.CharField(source='groups.privilege',read_only=True)
    option=serializers.CharField(write_only=True)
    def associate_permission(self, permission, group):
        ct_obj=set(p.content_type.model_class() for p in permission if hasattr(p.content_type.model_class(),"xtrmMeta") and hasattr(p.content_type.model_class().xtrmMeta,"associate_model"))
        if ct_obj:
            asList=[]
            for mclass in ct_obj:
                pList=tuple(p.codename for p in permission if p.content_type.model_class()==mclass)
                for p in pList:
                    x=p.split('_')
                    for m in mclass.xtrmMeta.associate_model:
                        asList.append(x[0] + '_' + m.lower())
            if asList and len(asList)>0:
                permission.extend(list(Permission.objects.filter(codename__in=asList).values_list('id',flat=True)))
        group.permissions.set(permission)

    def create(self,validated_data):
        opts=validated_data.get('option')
        if opts:
            opts=validated_data.pop('option')
        perms=validated_data.get('permissions')
        if perms:
            perms=validated_data.pop('permissions')
        gp=Group.objects.create(**validated_data)
        if perms:
            self.associate_permission(perms, gp)
        if opts:
            GroupOptions.objects.create(groups=gp,privilege=opts)
        return gp

    def update(self,instance,validated_data):
        opts=validated_data.get('option')
        if opts:
            opts=validated_data.pop('option')
        perms=validated_data.get('permissions')
        if perms:
            perms=validated_data.pop('permissions')
        oinstance=super(CGroupSerializer,self).update(instance,validated_data)
        oinstance.permissions.clear()
        if perms:
            self.associate_permission(perms, oinstance)
        groupOption = GroupOptions.objects.get(groups=oinstance)
        if groupOption and opts:
            groupOption.privilege = opts
            groupOption.save()
        return oinstance

    class Meta:
        model = Group
        name = 'group'
        fields='__all__'

class CGroupOptionsSerializer(serializers.ModelSerializer):
    groups=GroupSerializer(required=False,read_only=False)
    class Meta:
        model = GroupOptions
        fields = '__all__'
