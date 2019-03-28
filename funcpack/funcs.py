from django.core.paginator import Paginator
from django.conf import settings
import xlwt
from io import BytesIO
from IPy import IP, IPSet

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
    row = 1
    for datas in object_list.values():
        col = 0 
        for t in titles:
            sheet.write(row, col, datas[t])
            col += 1
        row += 1
    output = BytesIO()
    book.save(output)
    output.seek(0)
    return output

def getSubNet(ip, mask):
    subnet = IP(IP).make_net(mask)
    return subnet