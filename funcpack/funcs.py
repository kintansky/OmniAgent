from django.core.paginator import Paginator
from django.conf import settings
import xlwt
import os
# from io import BytesIO
from IPy import IP, IPSet
from omni.settings.base import BASE_DIR
import datetime

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


def exportXls(fieldlist, object_list):
    '''
    title: tuple or list
    '''
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    titles = [field.name for field in fieldlist]
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
            sheet.write(row, col, qs[i][t]) # 逐条实例化
            col += 1
        row += 1
    save_path = os.path.join(BASE_DIR, 'collected_static/downloads/temp/{}.xls'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S%f')))
    book.save(save_path)
    # print('保存位置：', save_path)
    # output = BytesIO()
    # book.save(output)
    # output.seek(0)
    return save_path

def getSubNet(ip, mask):
    subnet = IP(IP).make_net(mask)
    return subnet