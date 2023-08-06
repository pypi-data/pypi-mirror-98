from django.db import models
from django.conf import settings
from .fields import UniqueCharField,UniqueOptionalCharField,OptionalCharField,RequiredCharField,TextFieldOptional
# Create your models here.


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