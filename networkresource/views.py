from django.shortcuts import render
from .models import IpmanResource

# Create your views here.
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