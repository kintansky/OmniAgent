from django.core.paginator import Paginator
from django.conf import settings
import xlwt
import os
# from io import BytesIO
from IPy import IP, IPSet
from omni.settings.base import BASE_DIR
from django.utils import timezone

def pages(request, object_list, page_conf=settings.EACH_PAGE_DEVICES_NUMBER):
    paginator = Paginator(object_list, page_conf)
    page_num = request.GET.get('page', 1)
    page_of_objects = paginator.get_page(page_num)
    current_page_num = page_of_objects.number
    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+3, paginator.num_pages)+1))
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if paginator.num_pages-page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    return page_of_objects, page_range


XLS_DATETIME_FORMAT = xlwt.easyxf(num_format_str='yyyy/mm/dd')

def exportXls(fieldList, object_list, datetime_field=None):
    '''
    title: tuple or list
    '''
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    titles = [field.name for field in fieldList]
    col = 0
    for t in titles:
        sheet.write(0, col, t)
        col += 1
    # 错误写法
    # row = 1
    # for datas in object_list.values():    # 在返回的object_list是filter多条的时候，实例化时是全部一起实例化，导致网页超时
    #     col = 0 
    #     for t in titles:
    #         sheet.write(row, col, datas[t])
    #         col += 1
    #     row += 1
    row = 1
    qs = object_list.values()
    for i in range(object_list.count()):
        col = 0
        for t in titles:
            if t == datetime_field:
                sheet.write(row, col, qs[i][t], XLS_DATETIME_FORMAT)
            else:
                sheet.write(row, col, qs[i][t]) # 逐条实例化
            col += 1
        row += 1
    save_path = os.path.join(BASE_DIR, 'collected_static/downloads/temp/{}.xls'.format(timezone.datetime.strftime(timezone.datetime.now(), '%Y%m%d%H%M%S%f')))
    book.save(save_path)

    # print('保存位置：', save_path)
    # output = BytesIO()
    # book.save(output)
    # output.seek(0)
    return save_path

def rawQueryExportXls(fieldList, rawobj_list, datetime_field=None):    # rawquery 不能通过以上方式迭代取出，需要先序列化
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    col = 0
    for t in fieldList:
        sheet.write(0, col, t)
        col += 1
    row = 1
    for rawobj in rawobj_list:
        data = {}
        col = 0
        for t in fieldList:
            if t == datetime_field:
                sheet.write(row, col, rawobj.serializable_value(t), XLS_DATETIME_FORMAT)
            else:
                sheet.write(row, col, rawobj.serializable_value(t))
            col += 1
        row += 1
    save_path = os.path.join(BASE_DIR, 'collected_static/downloads/temp/{}.xls'.format(timezone.datetime.strftime(timezone.datetime.now(), '%Y%m%d%H%M%S%f')))
    book.save(save_path)
    return save_path

def objectDataSerializer(obj, data):    # 序列化单个模型的字段，输出dict，不适用于raw返回的obj
    for f in obj._meta.fields:
        key = f.attname
        val = obj.serializable_value(key)
        data[key] = val
    return data

def getSubNet(ip, mask):
    subnet = IP(IP).make_net(mask)
    return subnet

def getDateRange(days):
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=days)  # 负数向前
    return time_begin, time_end