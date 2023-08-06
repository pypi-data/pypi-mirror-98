# from django.db import models
# from django.conf import settings
# from .fields import UniqueCharField,UniqueOptionalCharField,OptionalCharField,RequiredCharField,TextFieldOptional
# # Create your models here.


# # class BaseModel(TimeStampedModel):
# class BaseModel(models.Model):
#     date_created=models.DateTimeField("Date Created",auto_now_add=True,blank=True,null=True,)
#     date_modified=models.DateTimeField("Date Modified",auto_now=True,blank=True,null=True,)
#     user_created=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="FK_%(class)s_UC")
#     user_modified=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="FK_%(class)s_UM")
#     remarks=TextFieldOptional("Remarks")

#     class Meta:
#         abstract=True

# class MasterModel(BaseModel):
#     name=UniqueCharField("Name",)
#     malias=UniqueOptionalCharField("Alias Name",)
#     officialname=OptionalCharField("Official Name",)

#     def __str__(self):
#         return str(self.name)
#     class Meta:
#         abstract=True
#         ordering=['name']

# class ContactModel(models.Model):
#     address=models.TextField("Address",blank=True,null=True,default='',)
#     city=OptionalCharField("City Name",)
#     state=OptionalCharField("State Name",)
#     country=OptionalCharField("Country Name",)
#     phoneno=OptionalCharField("Phone No.",)
#     mobileno=OptionalCharField("Mobile No.",)
#     emailid=OptionalCharField("Email Address",)

#     class Meta:
#         abstract=True

# class TaxationModel(models.Model):
#     panno=OptionalCharField("PAN No.",)
#     lstin=OptionalCharField("LSTIN",)
#     cstin=OptionalCharField("CSTIN",)
#     gstin=OptionalCharField("GSTIN",)
#     gstregtype=OptionalCharField("GST Registration",choices=(('UN','Unknown'),('CP','Composition'),('CM','Consumer'),('RG','Regular'),('UN','Unregistered')))
#     fromlocalterritory=models.BooleanField("Assessee of Local Territory",default=True)
#     isecommerce=models.BooleanField("Is e-commerce operator",default=False)
#     partytype=OptionalCharField("Party Type",choices=(('NA','Not Applicable'),('DE','Deemed Export'),('BD','Embassy/UN Body'),('SZ','SEZ')))
#     istransporter=models.BooleanField("Is a Transporter",default=False)

#     class Meta:
#         abstract=True

# class BranchModel(ContactModel,TaxationModel,MasterModel):

#     class Meta:
#         abstract=True

# class ContactPersonsModel(models.Model):
#     contactname=RequiredCharField("Contact Name",)
#     contactno=OptionalCharField("Contact No.")
#     emailid=OptionalCharField("Email ID")
#     sr=models.IntegerField("Serial Number",null=True,blank=True,)

#     class Meta:
#         abstract=True
#         ordering=['sr']

# class BankModel(models.Model):
#     titlename=RequiredCharField("Bank Account Title Name",)
#     accountno=RequiredCharField("Bank Account No.",)
#     bankname=RequiredCharField("Bank Name",)
#     branchname=RequiredCharField("Bank - Branch Name",)
#     ifsc=RequiredCharField("IFSC",)
#     sr=models.IntegerField("Serial Number",null=True,blank=True,)

#     class Meta:
#         abstract=True
#         ordering=['sr']

# class VoucherModel(BaseModel):
#     vdate=models.DateField('Date',)
#     voucher_no=OptionalCharField('Voucher No.',)

#     def __str__(self):
#         return str(self.voucher_no)
#     class Meta:
#         abstract=True
#         ordering=['-vdate']

# after custom user
from django.db import models
from django.conf import settings
from .fields import UniqueCharField,UniqueOptionalCharField,OptionalCharField,RequiredCharField,TextFieldOptional
# from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
# Create your models here.


class xManager(models.Manager):
    def __init__(self, key=''):
        super(xManager, self).__init__()
        self.k = key
    def for_user(self, user,methodname=''):
        if methodname=='GET' and user.has_perm(self.model._meta.app_label + '.view_' + self.model.__name__.lower())==False:
            # return super(xManager, self).get_queryset().none()
            raise PermissionDenied()
        if user.is_superuser:
            return super(xManager, self).get_queryset()
        elif user.is_staff:
            if user.groups.first().option.privilege=='GROUP':
                return super(xManager, self).get_queryset().filter(user_created__groups__in=user.groups.all())
            else:
                return super(xManager, self).get_queryset()
        else:
            if self.k!='':
                return super(xManager, self).get_queryset().filter(**{self.k: user})
            else:
                return super(xManager, self).get_queryset().none()
    def all(self):
        return super(xManager, self).get_queryset()

# class BaseModel(TimeStampedModel):
class BaseModel(models.Model):
    date_created=models.DateTimeField("Date Created",auto_now_add=True,blank=True,null=True,)
    date_modified=models.DateTimeField("Date Modified",auto_now=True,blank=True,null=True,)
    user_created=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="FK_%(class)s_UC")
    user_modified=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="FK_%(class)s_UM")
    remarks=TextFieldOptional("Remarks")

    class Meta:
        abstract=True

class MasterModel(BaseModel):
    name=UniqueCharField("Name",)
    malias=UniqueOptionalCharField("Alias Name",)
    officialname=OptionalCharField("Official Name",)

    def __str__(self):
        return str(self.name)
    class Meta:
        abstract=True
        ordering=['name']

class ContactModel(models.Model):
    address=models.TextField("Address",blank=True,null=True,default='',)
    city=OptionalCharField("City Name",)
    state=OptionalCharField("State Name",)
    country=OptionalCharField("Country Name",)
    phoneno=OptionalCharField("Phone No.",)
    mobileno=OptionalCharField("Mobile No.",)
    emailid=OptionalCharField("Email Address",)

    class Meta:
        abstract=True

class TaxationModel(models.Model):
    panno=OptionalCharField("PAN No.",)
    lstin=OptionalCharField("LSTIN",)
    cstin=OptionalCharField("CSTIN",)
    gstin=OptionalCharField("GSTIN",)
    gstregtype=OptionalCharField("GST Registration",choices=(('UN','Unknown'),('CP','Composition'),('CM','Consumer'),('RG','Regular'),('UN','Unregistered')))
    fromlocalterritory=models.BooleanField("Assessee of Local Territory",default=True)
    isecommerce=models.BooleanField("Is e-commerce operator",default=False)
    partytype=OptionalCharField("Party Type",choices=(('NA','Not Applicable'),('DE','Deemed Export'),('BD','Embassy/UN Body'),('SZ','SEZ')))
    istransporter=models.BooleanField("Is a Transporter",default=False)

    class Meta:
        abstract=True

class BranchModel(ContactModel,TaxationModel,MasterModel):

    class Meta:
        abstract=True

class ContactPersonsModel(models.Model):
    contactname=RequiredCharField("Contact Name",)
    contactno=OptionalCharField("Contact No.")
    emailid=OptionalCharField("Email ID")
    sr=models.IntegerField("Serial Number",null=True,blank=True,)

    class Meta:
        abstract=True
        ordering=['sr']

class BankModel(models.Model):
    titlename=RequiredCharField("Bank Account Title Name",)
    accountno=RequiredCharField("Bank Account No.",)
    bankname=RequiredCharField("Bank Name",)
    branchname=RequiredCharField("Bank - Branch Name",)
    ifsc=RequiredCharField("IFSC",)
    sr=models.IntegerField("Serial Number",null=True,blank=True,)

    class Meta:
        abstract=True
        ordering=['sr']

class VoucherModel(BaseModel):
    vdate=models.DateField('Date',)
    voucher_no=OptionalCharField('Voucher No.',)

    def __str__(self):
        return str(self.voucher_no)
    class Meta:
        abstract=True
        ordering=['-vdate']

################################################## User Models ############################################

# class User(AbstractUser):
#     groups = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     email = models.EmailField(max_length=50, unique=True,blank=True,null=True,)

#     REQUIRED_FIELDS = ['groups']

#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = 'users'

#     def get_full_name(self):
#         return '%s %s' % (self.first_name, self.last_name)

#     def get_short_name(self):
#         return self.first_name

#     def __str__(self):
#         return self.username

PRIVILEGE_CHOICES = (
    ('ALL','Can access all permitted data'),
    ('GROUP','Can access permitted data belonging to group only'),
    ('SELF','Can access permitted data belonging to the logged in user only'),
    )
class GroupOptions(models.Model):
    groups = models.OneToOneField(Group, on_delete=models.CASCADE,primary_key=True,related_name='option')
    privilege = models.CharField(max_length = 20, choices=PRIVILEGE_CHOICES, null=False, default='ALL',)
    dummytext=models.CharField('Dummy Text')

    def delete(self,*args,**kwargs):
        self.groups.delete()
        return super(self.__class__, self).delete(*args, **kwargs)