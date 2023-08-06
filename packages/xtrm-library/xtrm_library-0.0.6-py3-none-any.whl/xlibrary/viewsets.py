from rest_framework import status
from xtrm_drest.viewsets import DynamicModelViewSet
from rest_framework.response import Response
from django.db import IntegrityError
from .utils import render_filter_obj,render_to_pdf #render_filter_obj,render_to_pdf
from django.http import HttpResponse
from rest_framework.decorators import action
import csv
# import logging
class ModelViewset(DynamicModelViewSet):
    reporttitle='Report'
    orientation='portrait'
    options={'canAdd':0,'canPrint':0}

    def get_queryset(self):
        if self.action=='report':
            self.request.query_params.add('exclude[]','*')
            excludeFields=[]
            for col in self.columns:
                x=col['name'].split('.')
                z=''
                for y in range(len(x)-1):
                    if z=='':
                        z=z + x[y]
                    else:
                        z=z + '.' + x[y]
                    if (z in excludeFields)==False:
                        excludeFields.append(z)
                        self.request.query_params.add('exclude[]',z + '.*')
                self.request.query_params.add('include[]',col['name'])

        serializer=self.get_serializer()
        if hasattr(serializer.Meta.model.objects,'for_user'):
            return serializer.Meta.model.objects.for_user(self.request.user,self.request.method)
        return serializer.Meta.model.objects.all()

    def perform_create(self, serializer):
        if 'user_modified' in serializer.fields:
            serializer.save(user_created=self.request.user,user_modified=self.request.user)

    def perform_update(self,serializer):
        if 'user_modified' in serializer.fields:
            serializer.save(user_modified=self.request.user)

    @action(detail=False)
    def excel(self, request, *args, **kwargs):
        import datetime
        colheaders=[]
        colfields=[]
        for col in self.columns:
            isvisible=True
            if 'visible' in col:
                if col['visible']==False:
                    isvisible=False
            if isvisible:
                colheaders.append(col['title'])
                colfields.append(col['name'].replace('.','__'))
        serializer=self.get_serializer()
        filter =self.filter_queryset(serializer.Meta.model.objects.values_list(*colfields))
        response = HttpResponse(content_type='text/csv')
        file_name =self.reporttitle + '-' + str(datetime.date.today()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(colheaders)
        for i in filter:
            writer.writerow(i)
        response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'
        return response

    @action(detail=False)
    def report(self, request, *args, **kwargs):
        # logging.error(self.columns)
        serializer=super(ModelViewset,self).list(self,request,*args,**kwargs)
        respond={
            'options':self.options,
            'filters':self.filters,
            'columns':self.columns,
            'status':status.HTTP_200_OK,
            'message':self.reporttitle,
            'response':serializer.data
            }
        return Response(respond)

    @action(detail=False)
    def labels(self, request, *args, **kwargs):
        # logging.error(self.columns)
        serializer=self.get_serializer()
        this_model=serializer.Meta.model._meta
        respond={}
        respond['model__title']=this_model.verbose_name.title()
        for f in this_model.fields:
            respond[f.name]=f.verbose_name

        return Response(respond)

    @action(detail=False)
    def pdf(self, request, *args, **kwargs):
        import datetime
        colfields=[]
        columns=self.columns.copy()
        for col in self.columns:
            isvisible=True
            if 'visible' in col:
                if col['visible']==False:
                    isvisible=False
            if isvisible:
                colfields.append(col['name'].replace('.','__'))
            else:
                columns.remove(col)
        query = render_filter_obj(self.filters,request.query_params)
        serializer=self.get_serializer()
        filter = self.filter_queryset(serializer.Meta.model.objects.values_list(*colfields))
        pdf_obj = render_to_pdf('reports/report.html', {'data': filter, 'columns': columns,'period':'As On ' + datetime.date.today().strftime('%d/%m/%Y'),'orientation':self.orientation, 'companyname': 'Extreme Solutions', 'reporttitle': self.reporttitle,'filter':query})
        if pdf_obj:
            response = HttpResponse(
                    pdf_obj, content_type='application/pdf')
            filename = self.reporttitle + '-' + str(datetime.date.today()) + '.pdf'
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response

    def destroy(self, request, *args, **kwargs):
        """
        If foreign key has Protected on delete mode, DRF can't process this.
        """
        instance = self.get_object()
        try:
            instance.delete()
            return_status = status.HTTP_204_NO_CONTENT
            msg = None
        except IntegrityError:
            return_status = status.HTTP_403_FORBIDDEN
            # fields_dict = instance._meta.fields_map
            # msg = dict()
            # msg['message'] = "One of the following fields prevent deleting this instance: {}"\
            #     .format(", ".join(fields_dict.keys()))
            # msg['fields'] = fields_dict.keys()
            msg = dict()
            msg['message']="Can not delete, This is in use !!!"
        return Response(status=return_status, data=msg)

    class Meta:
        abstract=True

