from django import template
from django.template.defaultfilters import stringfilter
# import logging
# logger=logging.getLogger()
# import datetime

register = template.Library()

@register.filter
@stringfilter
def lower(value):
    return value.lower()

@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None

@register.filter
def minusOne(num, i):
    try:
        return num - i
    except:
        return None

@register.filter
def get_type(value):
    return type(value)

@register.simple_tag
def filters_tag(rowcnt0, rowcnt, *args, **kwargs):
    field = kwargs['field']
    filters = kwargs['filters']
    row = list_item(filters, rowcnt0-2)
    result = list_item(row, field)
    return result

@register.simple_tag
def filters_mid_tag(rowcnt0, rowcnt, *args, **kwargs):
    field = kwargs['field']
    filters = kwargs['filters']
    row = list_item(filters, rowcnt0-1)
    result = list_item(row, field)
    return result

@register.filter
def addcol( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value + arg
    except: pass
    return ''

@register.simple_tag
def slotTotalAmt(rowcnt, colcnt, *args, **kwargs):
    cols = kwargs['cols']
    rows = kwargs['rows']
    colindex = kwargs['colindex']
    sum = 0
    cols_counter = 0
    for c in cols:
        if(cols_counter == colindex):
            for r in rows:
                sum = sum + int(r[cols_counter])
        cols_counter = cols_counter + 1
        # sum = sum + int(r[0])
    return sum

@register.simple_tag
def slotAvgAmt(rowcnt, colcnt, *args, **kwargs):
    cols = kwargs['cols']
    rows = kwargs['rows']
    colindex = kwargs['colindex']
    row_length = kwargs['row_length']
    sum = 0
    cols_counter = 0
    for c in cols:
        if(cols_counter == colindex):
            for r in rows:
                # logger.error(r[cols_counter])
                if r[cols_counter]:
                    sum = sum + int(r[cols_counter])
        cols_counter = cols_counter + 1
        # sum = sum + int(r[0])
        sum = sum / row_length
    return sum

@register.filter
def slotTotalAmount(arg):
    return sum(list_item(d, 'id') for d in arg)

@register.filter
def update_variable(data, value):
    data = value
    return data

# @register.simple_tag
# def custom_tag(rowcnt, colcnt, *args, **kwargs):
#     row_data = kwargs['row_data'] # rowcnt
#     col_data = kwargs['col_data'] # colcnt
#     key = kwargs['key']
#     isformat = list_item(key, 'format')
#     # if isformat is not None:
#     #     return datetime.datetime.strptime(col_data, '%Y/%m/%d')
#         # return datetime.datetime.strptime(col_data, '%Y/%m/%d').strftime('%d-%m-%Y')
#     # curr_col = col_data[innerloop_counter]
#     # format_string = '%d-%m-%Y'
#     # if curr_col.type == 'date'
#     #       row_data[outerloop_counter][curr_col.key].strftime(format_string)
#     # if curr_col.alignment
#     #       args.style['text-align']=curr_col.alignment
#     # return row_data[outerloop_counter][curr_col.key]
#     # args.style['text-align'] = 'left'
#     return col_data

# @register.simple_tag
# def style_tag(colcnt, *args, **kwargs):
#     cols = kwargs['col_data']
#     style = 'padding:5px;font-size: 10px;'
#     # if cols.alignment is not None:
#     #     style = style + 'text-align:'+cols.alignment

#     return style

# @register.simple_tag
# def type_tag(colcnt, *args, **kwargs):
#     cols = kwargs['col_data']
#     xtype = 'text' # date|number-precision|text
#     # if cols.type is not None:
#     #     xtype = cols.type

#     return xtype

@register.filter
def col_aggregation(obj, cnt):
    new = list_item(obj, cnt)
    newObj = list_item(new, 'aggregation')
    return newObj

@register.filter
def col_type(obj, cnt):
    new = list_item(obj, cnt)
    newObj = list_item(new, 'type')
    return newObj

@register.filter
def col_style(obj, cnt):
    new = list_item(obj, cnt)

    col_width = ''
    width = list_item(new, 'width')
    if width is not None:
        col_width = 'width: '+width+';'

    # style = 'padding-left: 2px;padding-right: 2px;padding-top: 2px;font-size: 10px;'+col_width
    newObj = list_item(new, 'alignment')
    if newObj is not None:
        if newObj == 'centre':
           newObj = 'center'
        style = 'padding-left: 2px;padding-right: 2px;padding-top: 2px;font-size: 10px;'+col_width+'text-align:'+newObj+';'
    else:
        style = 'padding-left: 2px;padding-right: 2px;padding-top: 2px;font-size: 10px;text-align:left;'+col_width
    return style

@register.filter
def col_precision(obj, cnt):
    new = list_item(obj, cnt)
    newObj = list_item(new, 'precision')
    if(newObj == None):
       newObj = 2
    return newObj

