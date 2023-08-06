from xtrm_drest.routers import DynamicRouter
# from .views import UserViewSet, GroupViewSet, PermissionViewSet,ContenttypeViewSet,GroupOptionsViewSet,CUserViewSet,CGroupOptionsViewSet,CGroupViewSet
from .views import UserViewSet, GroupViewSet, PermissionViewSet, ContenttypeViewSet, GroupOptionsViewSet, CUserViewSet, CGroupViewSet
router = DynamicRouter()
# dynamic rest
router.register('users', UserViewSet)
router.register('edit/user', CUserViewSet)
router.register('groups', GroupViewSet)
router.register('edit/group', CGroupViewSet)
router.register('permissions', PermissionViewSet)
router.register('contenttypes', ContenttypeViewSet)
router.register('groupoptions', GroupOptionsViewSet)
# router.register('create_groupoptions', CGroupOptionsViewSet)

urlpatterns = router.urls
