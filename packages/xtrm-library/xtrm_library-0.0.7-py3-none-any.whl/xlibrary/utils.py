from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
# import logging
import datetime


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_filter_obj(fObj, qObj):
    query = []
    # logging.error(fObj)
    # logging.error(qObj)
    for v in fObj:
        if isinstance(v['title'], list):
            for vx in v['title']:
                if qObj.__contains__(vx['name']):
                    query.append(
                        {'title': vx['title'], 'value': qObj[vx['name']]})
        else:
            if qObj.__contains__(v['name']):
                flg = False
                if 'type' in v.keys():
                    if v['type'] =='date':
                        flg = True
                        query.append({'title': v['title'], 'value': datetime.datetime.strptime(qObj[v['name']], '%Y-%m-%d').strftime('%d/%m/%Y')})
                if not flg:
                    query.append({'title': v['title'], 'value': qObj[v['name']]})
            elif qObj.__contains__('filter{' + v['name'] + '.gte}'):
                if 'type' in v.keys():
                    if v['type'] =='period':
                        query.append({'title': v['title'], 'value': datetime.datetime.strptime(qObj['filter{' + v['name'] + '.gte}'], '%Y-%m-%d').strftime('%d/%m/%Y') + ' To ' + datetime.datetime.strptime(qObj['filter{' + v['name'] + '.lte}'],'%Y-%m-%d').strftime('%d/%m/%Y')})

    # logging.error(query)
    return query


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box

        return get_page_body(box.all_children())
