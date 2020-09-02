from django.core.paginator import Paginator
from .models import *

def get_filename(filename):
    return filename.upper()


def ticket_filter(filter, url_parameter):
    switcher = {
        'Code': Ticket.objects.filter(ticket_code__icontains=url_parameter).order_by('-date_added'),
        'Client': Ticket.objects.filter(client__client_name__icontains=url_parameter).order_by('-date_added'),
        'Status': Ticket.objects.filter(status_id__stat_name__icontains=url_parameter).order_by('-date_added'),
        'Category': Ticket.objects.filter(category_id__cat_name__icontains=url_parameter).order_by('-date_added'),
        'Sub-Category': Ticket.objects.filter(sub_category_id__scat_name__icontains=url_parameter).order_by('-date_added'),
        'Project': Ticket.objects.filter(project_id__proj_name__icontains=url_parameter).order_by('-date_added'),
        'Product': Ticket.objects.filter(product_id__prod_name__icontains=url_parameter).order_by('-date_added'),
    }
    return switcher.get(filter, "Invalid filter")


def project_filter(filter, url_parameter):
    switcher = {
        'Name': Project.objects.filter(proj_name__icontains=url_parameter).order_by('-proj_date_added'),
        'Client': Project.objects.filter(proj_client__client_name__icontains=url_parameter).order_by('-proj_date_added'),
        'Status': Project.objects.filter(proj_status__stat_name__icontains=url_parameter).order_by('-proj_date_added'),
        'Manager': Project.objects.filter(proj_manager__first_name__icontains=url_parameter, proj_manager__last_name__icontains=url_parameter).order_by('-proj_date_added'),
    }
    return switcher.get(filter, "Invalid filter")

def client_filter(filter, url_parameter):
    switcher = {
        'Name': Client.objects.filter(client_name__icontains=url_parameter).order_by('-client_date_added'),
        'Address': Client.objects.filter(client_address__icontains=url_parameter).order_by('-client_date_added'),
        'Status': Client.objects.filter(client_status__stat_name__icontains=url_parameter).order_by('-client_date_added'),
        'Manager': Client.objects.filter(account_manager__first_name__icontains=url_parameter).order_by('-client_date_added'),
    }
    return switcher.get(filter, "Invalid filter")

def product_filter(filter, url_parameter):
    switcher = {
        'Name': Product.objects.filter(prod_name__icontains=url_parameter).order_by('-prod_date_added'),
        'Client': Product.objects.filter(client_id__client_name__icontains=url_parameter).order_by('-prod_date_added'),
        'Status': Product.objects.filter(prod_status__stat_name__icontains=url_parameter).order_by('-prod_date_added'),
        'Manager': Product.objects.filter(prod_manager__first_name__icontains=url_parameter).order_by('-prod_date_added'),
    }
    return switcher.get(filter, "Invalid filter")

def product_type_filter(filter, url_parameter):
    switcher = {
        'Name': ProductType.objects.filter(prod_type_name__icontains=url_parameter).order_by('-prod_type_date_added'),
        'Code': ProductType.objects.filter(prod_type_code__icontains=url_parameter).order_by('-prod_type_date_added'),
    }
    return switcher.get(filter, "Invalid filter")

def module_filter(filter, url_parameter):
    switcher = {
        'Name': Module.objects.filter(mod_name__icontains=url_parameter).order_by('-mod_date_added'),
        'Code': Module.objects.filter(mod_code__icontains=url_parameter).order_by('-mod_date_added'),
        'Product': Module.objects.filter(product__prod_name__icontains=url_parameter).order_by('-mod_date_added'),
        'Status': Module.objects.filter(mod_status__stat_name__icontains=url_parameter).order_by('-mod_date_added'),
    }
    return switcher.get(filter, "Invalid filter")

def category_filter(filter, url_parameter):
    switcher = {
        'Name': Category.objects.filter(cat_name__icontains=url_parameter).order_by('-cat_date_added'),
        'Code': Category.objects.filter(cat_code__icontains=url_parameter).order_by('-cat_date_added'),
        'Status': Category.objects.filter(cat_status__stat_name__icontains=url_parameter).order_by('-cat_date_added'),
    }
    return switcher.get(filter, "Invalid filter")


def subcategory_filter(filter, url_parameter):
    switcher = {
        'Name': SubCategory.objects.filter(scat_name__icontains=url_parameter).order_by('-scat_date_added'),
        'Code': SubCategory.objects.filter(scat_code__icontains=url_parameter).order_by('-scat_date_added'),
        'Category': SubCategory.objects.filter(category__cat_name__icontains=url_parameter).order_by('-scat_date_added'),
        'Status': SubCategory.objects.filter(scat_status__stat_name__icontains=url_parameter).order_by('-scat_date_added'),
    }
    return switcher.get(filter, "Invalid filter")



#function that generates the page_object for the pagination
def create_pagination(object, request):
    paginator = Paginator(object, 10, 0)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj