from django.core.paginator import Paginator
from .models import *

def get_filename(filename):
    return filename.upper()


def user_filter(filter, url_parameter):
    switcher = {
        'Name': User.objects.filter(scat_name__icontains=url_parameter).order_by('-scat_date_added'),
        'Code': User.objects.filter(scat_code__icontains=url_parameter).order_by('-scat_date_added'),
        'Category': User.objects.filter(category__cat_name__icontains=url_parameter).order_by('-scat_date_added'),
        'Status': User.objects.filter(scat_status__stat_name__icontains=url_parameter).order_by('-scat_date_added'),
    }
    return switcher.get(filter, "Invalid filter")



#function that generates the page_object for the pagination
def create_pagination(object, request):
    paginator = Paginator(object, 10, 0)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj