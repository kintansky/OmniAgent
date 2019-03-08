from django.shortcuts import render
from .models import IpmanResource
from .models import IpRecord
from .forms import IPsearchForm
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('omni')), 'funcpack'))
from funcpack.funcs import pages

# Create your views here.
# port views
def show_ports(request):
    context = {}
    return render(request, 'resource.html', context)

def search_device_ports(request):
    device_name = request.GET.get('device_name', 'NULL')
    context = {}
    if device_name != 'NULL':    
        ipman_resource = IpmanResource.objects.filter(device_name=device_name)
        context['device_ports'] = ipman_resource
    context['device_name'] = device_name
    return render(request, 'resource.html', context)

# iprecord views
def ip_list(request):
    ip_all_list = IpRecord.objects.all()
    page_of_objects, page_range = pages(request, ip_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = IpRecord.objects.all().count()
    context['ip_search_form'] = IPsearchForm()
    return render(request, 'iprecord.html', context)

def search_ip(request):
    ip_search_form = IPsearchForm(request.GET)
    if ip_search_form.is_valid():
        ip_address = ip_search_form.cleaned_data['ip_address']
        device_name = ip_search_form.cleaned_data['device_name']
        ip_description = ip_search_form.cleaned_data['description']
        if ip_address != '':
            ip_all_list = IpRecord.objects.filter(device_ip=ip_address)
        elif device_name != '':
            ip_all_list = IpRecord.objects.filter(device_name=device_name, ip_description__icontains=ip_description)
        else:
            ip_all_list = IpRecord.objects.filter(ip_description__icontains=ip_description)
    else:
        context = {}
        context['ip_search_form'] = ip_search_form
        return render(request, 'iprecord.html', context)

    page_of_objects, page_range = pages(request, ip_all_list)


    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = IpRecord.objects.all().count()
    context['search_ip_address'] = ip_address
    context['search_device_name'] = device_name
    context['search_description'] = ip_description
    context['ip_search_form'] = ip_search_form
    return render(request, 'iprecord.html', context)