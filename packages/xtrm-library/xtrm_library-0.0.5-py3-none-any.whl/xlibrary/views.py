# # from xlibrary.viewsets import ModelViewset as viewsets.ModelViewSet
# from rest_framework import viewsets
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from .serializers import UserSerializer, GroupSerializer, PermissionSerializer,ContenttypeSerializer
# from rest_auth.views import LoginView as RestAuthLoginView
# from django.conf import settings
# from rest_framework.response import Response
# from rest_framework import status

# def jwt_response_payload_handler(token, user=None, request=None):
#     return {
#         'token': token,
#         'user': UserSerializer(user, context={'request': request}).data
#     }

# class LoginView(RestAuthLoginView):
#     """
#     Overriden LoginView

#     get_response serializes the response according to the default serializer (as you already know)
#     which in turn, uses the default UserDetailsSeriazlizer (which we don't want)

#     What we can do is use our custom jwt_response_payload_handler as our serializer and return in directly
#     in the response
#     """
#     def get_response(self):
#         serializers_class = self.get_response_serializer()

#         if getattr(settings, 'REST_USE_JWT', False):

#             # Use jwt_response_payload_handler since we already have the token, user (optional) and the request (optional)
#             data = jwt_response_payload_handler(self.token, self.user, self.request)

#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             serializer = serializers_class(instance=self.token, context={'resquest': self.request})

#             return Response(serializer.data, status=status.HTTP_200_OK)


# class UserViewSet(viewsets.ModelViewSet):
# 	queryset=User.objects.all()
# 	serializer_class=UserSerializer
# 	reporttitle='Users'
# 	#orientation='landscape'
# 	options={'canAdd':1,'canPrint':1}
# 	filters=[
# 		{'title':'User Name','name':'filter{username}','url':'v1/rights/users/'},
# 		{'title':'Email','name':'filter{email}'}
# 	]
# 	columns=[
# 		{'title':'Id','name':'id','type':'numeric','searchable':False,'sortable':False,'visible':False},
# 		{'title':'User Name','name':'username','width':'20%'},
# 		{'title':'First Name','name':'first_name','width':'20%'},
# 		{'title':'Last Name','name':'last_name','width':'20%'},
# 		{'title':'Email','name':'email'}
# 	]

# class GroupViewSet(viewsets.ModelViewSet):
# 	queryset=Group.objects.all()
# 	serializer_class=GroupSerializer
# 	reporttitle='Groups'
# 	#orientation='landscape'
# 	options={'canAdd':1,'canPrint':1}
# 	filters=[
# 		{'title':'name','name':'filter{name}','url':'v1/rights/groups/'}
# 	]
# 	columns=[
# 		{'title':'Id','name':'id','alignment':'right','type':'numeric','searchable':False,'sortable':False,'visible':False},
# 		{'title':'Name','name':'name'}
# 	]

# class PermissionViewSet(viewsets.ModelViewSet):
# 	queryset=Permission.objects.all()
# 	serializer_class=PermissionSerializer
# 	reporttitle='Permissions'
# 	#orientation='landscape'
# 	options={'canAdd':1,'canPrint':1}
# 	filters=[
# 		{'title':'Name','name':'filter{name}','url':'v1/rights/permissions/'}
# 	]
# 	columns=[
# 		{'title':'Id','name':'id','alignment':'right','type':'numeric','searchable':False,'sortable':False,'visible':False},
# 		{'title':'Name','name':'name'},
# 		{'title':'Code Name','name':'codename'}
# 	]

# class ContenttypeViewSet(viewsets.ModelViewSet):
# 	queryset=ContentType.objects.all()
# 	serializer_class=ContenttypeSerializer
# 	reporttitle='Content Types'
# 	#orientation='landscape'
# 	options={'canAdd':1,'canPrint':1}
# 	filters=[
# 		{'title':'App Label','name':'filter{app_label}','url':'v1/rights/contenttypes/'}
# 	]
# 	columns=[
# 		{'title':'Id','name':'id','alignment':'right','type':'numeric','searchable':False,'sortable':False,'visible':False},
# 		{'title':'App Label','name':'app_label'},
# 		{'title':'Model','name':'model'}
# 	]

# after custom user
from xlibrary.viewsets import ModelViewset as xViewSet
from rest_framework import viewsets
# from .models import User,GroupOptions
from .models import GroupOptions
from django.contrib.auth.models import Group, Permission
# from django.contrib.auth.models import User,Group, Permission
from django.contrib.contenttypes.models import ContentType
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer,ContenttypeSerializer,GroupOptionsSerializer,CUserSerializer, CGroupSerializer,CGroupOptionsSerializer
from rest_auth.views import LoginView as RestAuthLoginView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
def getVisiblePermissions():
    ct = ContentType.objects.all()
    myNameList = []
    for c in ct:
        class_name=c.model_class()
        if hasattr(class_name, "xtrmMeta"):
            myNameList.append(class_name.__name__.lower())
    return myNameList

def jwt_response_payload_handler(token, user=None, request=None):
    myNameList=getVisiblePermissions()
    perms=user.groups.first()
    rtn=[]
    if perms:
        for perm in perms.permissions.all().filter(content_type__model__in=myNameList):
            pm={
                "name":perm.name,
                "codename":perm.codename,
                "app_label":perm.content_type.app_label,
                "model":perm.content_type.model
                }
            rtn.append(pm)

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        'permissions':rtn
    }

class LoginView(RestAuthLoginView):
    """
    Overriden LoginView

    get_response serializes the response according to the default serializer (as you already know)
    which in turn, uses the default UserDetailsSeriazlizer (which we don't want)

    What we can do is use our custom jwt_response_payload_handler as our serializer and return in directly
    in the response
    """
    def get_response(self):
        serializers_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):

            # Use jwt_response_payload_handler since we already have the token, user (optional) and the request (optional)
            data = jwt_response_payload_handler(self.token, self.user, self.request)

            return Response(data, status=status.HTTP_200_OK)
        else:
            serializer = serializers_class(instance=self.token, context={'resquest': self.request})

            return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(xViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer
	reporttitle='Users'
	#orientation='landscape'
	options={'canAdd':1,'canPrint':1}
	filters=[
		{'title':'User Name','name':'filter{username}','url':'v1/rights/users/'},
		{'title':'Email','name':'filter{email}'},
		{"title": "Group","name": "filter{groups.name}","url": "v1/rights/groups/"}
	]
	columns=[
		{'title':'Id','name':'id','type':'numeric','searchable':False,'sortable':False,'visible':False},
		{'title':'User Name','name':'username','width':'20%'},
		{'title':'First Name','name':'first_name','width':'20%'},
		{'title':'Last Name','name':'last_name','width':'20%'},
		{'title':'Email','name':'email'}
	]

class GroupViewSet(xViewSet):
	queryset=Group.objects.all()
	serializer_class=GroupSerializer
	reporttitle='Groups'
	#orientation='landscape'
	options={'canAdd':1,'canPrint':1}
	filters=[
		{'title':'name','name':'filter{name}','url':'v1/rights/groups/'}
	]
	columns=[
		{'title':'Id','name':'id','alignment':'right','type':'numeric','searchable':False,'sortable':False,'visible':False},
		{'title':'Name','name':'name'}
	]

class PermissionViewSet(xViewSet):
	queryset=Permission.objects.all()
	serializer_class=PermissionSerializer
	reporttitle='Permissions'
	#orientation='landscape'
	options={'canAdd':1,'canPrint':1}
	filters=[
		{'title':'Name','name':'filter{name}','url':'v1/rights/permissions/'}
	]
	columns=[
		{'title':'Id','name':'id','alignment':'right','type':'numeric','searchable':False,'sortable':False,'visible':False},
		{'title':'Name','name':'name'},
		{'title':'Code Name','name':'codename'}
	]

	def get_queryset(self):
	    myNameList = getVisiblePermissions()
	    return Permission.objects.all().filter(content_type__model__in=myNameList)

class ContenttypeViewSet(xViewSet):
	queryset=ContentType.objects.all()
	serializer_class=ContenttypeSerializer
	reporttitle='Content Types'
	#orientation='landscape'
	options={'canAdd':1,'canPrint':1}
	filters=[
		{'title':'App Label','name':'filter{app_label}','url':'v1/rights/contenttypes/'}
	]
	columns=[
		{'title':'Id','name':'id','alignment':'right','type':'numeric','searchable':False,'sortable':False,'visible':False},
		{'title':'App Label','name':'app_label'},
		{'title':'Model','name':'model'}
	]

class GroupOptionsViewSet(xViewSet):
    queryset = GroupOptions.objects.all()
    serializer_class = GroupOptionsSerializer

class CUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CUserSerializer

    # def get_permissions(self):
    #     permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

class CGroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = CGroupSerializer

class CGroupOptionsViewSet(viewsets.ModelViewSet):
    queryset = GroupOptions.objects.all()
    serializer_class = CGroupOptionsSerializer
