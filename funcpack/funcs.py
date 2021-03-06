from django.core.paginator import Paginator
from django.conf import settings
import xlwt
import os
# from io import BytesIO
from IPy import IP, IPSet
from omni.settings.base import BASE_DIR
from django.utils import timezone
import json
from math import ceil

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
# fieldList 通过 类._meta.fields 传入
def exportXls(fieldList, object_list, datetime_field=tuple()):
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
            if t in datetime_field:
                sheet.write(row, col, qs[i][t], XLS_DATETIME_FORMAT)
            else:
                sheet.write(row, col, qs[i][t]) # 逐条实例化
            col += 1
        row += 1
    p = os.path.join(BASE_DIR, 'downloads/temp/')
    if not os.path.exists(p):
        os.makedirs(p)
        os.chown(p, 1006, 1006)
    save_path = os.path.join(p, '{}.xls'.format(timezone.datetime.strftime(timezone.datetime.now(), '%Y%m%d%H%M%S%f')))
    book.save(save_path)

    # print('保存位置：', save_path)
    # output = BytesIO()
    # book.save(output)
    # output.seek(0)
    return save_path

# 因为rawobj_list是一个QuerySet，所以fieldList需要通过QuerySet.columns传入
def rawQueryExportXls(fieldList, rawobj_list, datetime_field=tuple()):    # rawquery 不能通过以上方式迭代取出，需要先序列化
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    col = 0
    for t in fieldList:
        sheet.write(0, col, t)
        col += 1
    row = 1
    for rawobj in rawobj_list:
        col = 0
        for t in fieldList:
            if t in datetime_field:
                sheet.write(row, col, rawobj.serializable_value(t), XLS_DATETIME_FORMAT)
            else:
                sheet.write(row, col, rawobj.serializable_value(t))
            col += 1
        row += 1
    p = os.path.join(BASE_DIR, 'downloads/temp/')
    if not os.path.exists(p):
        os.makedirs(p)
        os.chown(p, 1006, 1006)
    save_path = os.path.join(p, '{}.xls'.format(timezone.datetime.strftime(timezone.datetime.now(), '%Y%m%d%H%M%S%f')))
    book.save(save_path)
    return save_path

'''
 exportClassifiedXls 会按照分类字段进行分类写入不同的sheet，所以注意提供的分类字段不要太多，
 同时，还提供了一个写入其他表的接口，但这个表不会分类
'''
def exportClassifiedXls(fieldList, rawobj_list, datetime_field, classify_field, none_classify_fieldList=None, none_classify_rawobj_list=None, none_classify_datetime_field=None, none_classify_sheet_name=None):
    # datetime_field 传入tuple类型
    book = xlwt.Workbook()
    for rawobj in rawobj_list:
        # 按照分类字段切换表格进行添加数据
        if classify_field == '':    # 不分类写表
            try:
                sheet = book.get_sheet('全量')
            except:
                sheet = book.add_sheet('全量')
                col = 0
                for t in fieldList:
                    sheet.write(0, col, t)
                    col += 1
        else:   # 分类写表
            try:
                sheet = book.get_sheet(rawobj.serializable_value(classify_field))
            except:
                sheet = book.add_sheet(rawobj.serializable_value(classify_field))
                col = 0
                for t in fieldList:
                    sheet.write(0, col, t)
                    col += 1
        col = 0
        row = sheet.last_used_row+1
        for t in fieldList:
            if t in datetime_field:
                sheet.write(row, col, rawobj.serializable_value(t), XLS_DATETIME_FORMAT)
            else:
                sheet.write(row, col, rawobj.serializable_value(t))
            col += 1
    # 其他不分类的数据表
    if none_classify_rawobj_list is not None:
        sheet3 = book.add_sheet(none_classify_sheet_name)
        col = 0
        for t in none_classify_fieldList:
            sheet3.write(0, col, t)
            col += 1
        for rawobj in none_classify_rawobj_list:
            col = 0
            row = sheet3.last_used_row+1
            for t in none_classify_fieldList:
                if t in none_classify_datetime_field:
                    sheet3.write(row, col, rawobj.serializable_value(t), XLS_DATETIME_FORMAT)
                else:
                    sheet3.write(row, col , rawobj.serializable_value(t))
                col += 1
    p = os.path.join(BASE_DIR, 'downloads/temp/')
    if not os.path.exists(p):
        os.makedirs(p)
        os.chown(p, 1006, 1006)
    save_path = os.path.join(p, '{}.xls'.format(timezone.datetime.strftime(timezone.datetime.now(), '%Y%m%d%H%M%S%f')))
    book.save(save_path)
    return save_path

def objectDataSerializer(obj, data):    # 序列化单个模型的字段，输出dict，不适用于raw返回的obj
    for f in obj._meta.fields:
        key = f.attname
        val = obj.serializable_value(key)
        data[key] = val
    return data

def objectDataSerializerRaw(rawobj, fieldList, data):   #fieldList需要通过QuerySet.columns传入
    for f in fieldList:
        val = rawobj.serializable_value(f)
        data[f] = val
    return data

def getSubNet(ip, mask):
    subnet = IP(IP).make_net(mask)
    return subnet

def getDateRange(days):
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=days)  # 负数向前
    return time_begin, time_end

def dumpOlt2Json(olts, device_name):
    d = {}
    d['name'] = device_name
    d['children'] = []
    for olt in olts:
        d['children'].append({'name': olt, 'value':10})
    result = json.dumps(d)
    return result

def dict2SearchParas(d):    # 将字典转换成网页搜索的参数格式，以&开头
    s = ''
    for key in d:
        if d[key] is None:
            continue
        s += '&{}={}'.format(key, d[key])
    return s

'''
快排
'''
def quickSortObj(arr, lowIndex, highIndex, sortIndex):  # sortIndex 为需要排序的index
    # 快排, 倒序
    if lowIndex < highIndex:
        pi = partition(arr, lowIndex, highIndex, sortIndex)
        quickSortObj(arr, lowIndex, pi-1, sortIndex)
        quickSortObj(arr, pi+1, highIndex, sortIndex)


def partition(arr, lowIndex, highIndex, sortIndex):
    i = lowIndex - 1
    pivot = arr[highIndex][sortIndex]
    for j in range(lowIndex, highIndex):
        if arr[j][sortIndex] >= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[highIndex] = arr[highIndex], arr[i+1]
    return i+1

'''
快排 end
'''
# 按照子网块大小进行网段平分
def splitNet(targetNet, subMask):
    targetIP, segmentMask = targetNet.split('/')
    net = IP.make_net(targetIP, segmentMask)
    blockSize = 2**(32-subMask) # 块大小
    netCount = ceil(2**(32-int(segmentMask))/blockSize) # 可平分的子网数
    result = []
    for i in range(netCount):
        s = eval('0b'+net[0].strBin())+blockSize*i # 二进制计算下一个子网地址
        snet = IP.make_net(s, subMask)
        # print(snet, snet.len())
        result.append(snet.strNormal())
    return result
