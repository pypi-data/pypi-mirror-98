from django.db import models

class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }
    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)

class BaseCharField(CaseInsensitiveFieldMixin,models.CharField):
    description="An abstract class for Character Fields, With max_length set to 255."

    def __init__(self,*args,**kwargs):
        kwargs['max_length']=255
        super().__init__(*args,**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def get_db_prep_value(self,value,*args,**kwargs):
        if value:
            value=value.strip()
        if self.blank==self.null==self.unique==True and value=='':
            value=None

        return value

    class Meta:
        abstract=True

class UniqueCharField(BaseCharField):
    description="A Unique CharField"

    def __init__(self,*args,**kwargs):
        kwargs['unique']=True
        kwargs['blank']=False
        kwargs['null']=False
        super().__init__(*args,**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["unique","blank","null"]
    #     return name, path, args, kwargs

class UniqueOptionalCharField(BaseCharField):
    description="A Unique CharField"

    def __init__(self,*args,**kwargs):
        kwargs['unique']=True
        kwargs['blank']=True
        kwargs['null']=True
        super().__init__(*args,**kwargs)



    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["unique","blank","null"]
    #     return name, path, args, kwargs

class RequiredCharField(BaseCharField):
    description="A required CharField"

    def __init__(self,*args,**kwargs):
        kwargs['blank']=False
        kwargs['null']=False
        super().__init__(*args,**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["blank","null"]
    #     return name, path, args, kwargs

class OptionalCharField(BaseCharField):
    description="An optional CharField"

    def __init__(self,*args,**kwargs):
        kwargs['blank']=True
        kwargs['null']=True
        kwargs['default']=''
        super().__init__(*args,**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["blank","default"]
    #     return name, path, args, kwargs

class AmountField(models.DecimalField):
    description="A numeric field with two decimal places"

    def __init__(self,*args,**kwargs):
        kwargs['max_digits']=12
        kwargs['decimal_places']=2
        kwargs['default']=0
        super().__init__(*args,**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["max_digits","decimal_places","default"]
    #     return name, path, args, kwargs

class QtyField(models.DecimalField):
    description="A numeric field with four decimal places"

    def __init__(self,*args,**kwargs):
        kwargs['max_digits']=12
        kwargs['decimal_places']=4
        kwargs['default']=0
        super().__init__(*args,**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["max_digits","decimal_places","default"]
    #     return name, path, args, kwargs

class TextFieldOptional(models.TextField):
    description="A multiline optional text field"

    def __init__(self,*args,**kwargs):
        kwargs['null']=True
        kwargs['blank']=True
        super().__init__(*args,**kwargs)

    def get_db_prep_value(self,value,*args,**kwargs):
        if value:
            value=value.strip()

        return value

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["null","blank"]
    #     return name, path, args, kwargs

class TextFieldRequired(models.TextField):
    description="A multiline required text field"

    def __init__(self,*args,**kwargs):
        kwargs['null']=False
        kwargs['blank']=False
        super().__init__(*args,**kwargs)

    def get_db_prep_value(self,value,*args,**kwargs):
        if value:
            value=value.strip()

        return value

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["null","blank"]
    #     return name, path, args, kwargs

class EmailFieldOptional(models.EmailField):
    description="An optional email field"

    def __init__(self,*args,**kwargs):
        kwargs['null']=True
        kwargs['blank']=True
        super().__init__(*args,**kwargs)

    # def get_db_prep_value(self,value,*args,**kwargs):
    #     if value:
    #         value=value.strip()
    #     if self.blank==self.null==self.unique==True and value=='':
    #         value=None

    #     return value

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["null","blank"]
    #     return name, path, args, kwargs

class EmailFieldOptionalUnique(CaseInsensitiveFieldMixin,models.EmailField):
    description="An optional unique email field"

    def __init__(self,*args,**kwargs):
        kwargs['unique']=True
        kwargs['null']=True
        kwargs['blank']=True
        super().__init__(*args,**kwargs)

    def get_db_prep_value(self,value,*args,**kwargs):
        # if value:
        #     value=value.strip()
        if value=='':
            value=None

        return value

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["unique","null","blank"]
    #     return name, path, args, kwargs

class EmailFieldRequiredUnique(CaseInsensitiveFieldMixin,models.EmailField):
    description="A required unique email field"

    def __init__(self,*args,**kwargs):
        kwargs['unique']=True
        kwargs['null']=False
        kwargs['blank']=False
        super().__init__(*args,**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs["unique","null","blank"]
    #     return name, path, args, kwargs

class ForeignKeyOptional(models.ForeignKey):
    description="An optional foreign key field"

    def __init__(self,*args,**kwargs):
        kwargs['blank']=True
        kwargs['null']=True
        kwargs['on_delete']=models.PROTECT
        super().__init__(*args,**kwargs)

    def get_db_prep_value(self,value,*args,**kwargs):
        # if value:
        #     value=value.strip()
        if value=='':
            value=None

        return value

class ForeignKeyProtected(models.ForeignKey):
    description="A protected foreign key field"

    def __init__(self,*args,**kwargs):
        kwargs['on_delete']=models.PROTECT
        super().__init__(*args,**kwargs)

    # def get_db_prep_value(self,value,*args,**kwargs):
    #     if value:
    #         value=value.strip()

    #     return value

class ForeignKeyCascade(models.ForeignKey):
    description="A cascade foreign key field"

    def __init__(self,*args,**kwargs):
        kwargs['on_delete']=models.CASCADE
        super().__init__(*args,**kwargs)

    # def get_db_prep_value(self,value,*args,**kwargs):
    #     if value:
    #         value=value.strip()

    #     return value

class DateFieldOptional(models.DateField):
    description="An optional Date Field"

    def __init__(self,*args,**kwargs):
        kwargs['blank']=True
        kwargs['null']=True
        super().__init__(*args,**kwargs)

    def get_db_prep_value(self,value,*args,**kwargs):
        # if value:
        #     value=value.strip()
        if value=='':
            value=None

        return value

class DateTimeFieldOptional(models.DateTimeField):
    description="An optional DateTime Field"

    def __init__(self,*args,**kwargs):
        kwargs['blank']=True
        kwargs['null']=True
        super().__init__(*args,**kwargs)

    def get_db_prep_value(self,value,*args,**kwargs):
        # if value:
        #     value=value.strip()
        if value=='':
            value=None

        return value