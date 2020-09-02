#import self as self
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.template.loader import render_to_string
from django.views.generic import (ListView ,
                                  DetailView ,
                                  CreateView ,
                                  UpdateView ,
                                  DeleteView , )
from users.models import Team
from .forms import TicketForm, TicketAttachmentForm, UploadFileForm, CommentForm, ProjectForm, ClientForm, ProductForm,\
    ModuleForm, ProductTypeForm
from users.models import Profile, User
from .models import Ticket , Category , SubCategory , Project , Product , ProductType, Status , Client , HotIssue , Module ,  \
    TicketAttachment, Comment
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .utils import create_pagination, ticket_filter, project_filter, client_filter, product_filter, product_type_filter, \
                   module_filter, category_filter, subcategory_filter


@login_required
def ticket_detail(request, pk):
    ticket = Ticket.objects.get(ticket_id=pk)
    comment = Comment.objects.filter(ticket=ticket).order_by('-comment_date_added')
    attachment = TicketAttachment.objects.filter(ticket=ticket)
    page_obj = create_pagination(comment, request)
    status = Status.objects.all().values('stat_id', 'stat_name')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if 'mark-solution-button' in request.POST:
            sol_id  = request.POST["input-field"]
            comment_id = Comment.objects.get(comment_id=sol_id)
            date_now = timezone.now()
            Ticket.objects.filter(ticket_id=pk).update(solution = comment_id, status = 2, date_closed=f'{date_now}', last_update_by = request.user, last_update=f'{date_now}')
            print(f"Status is {Status.objects.get(stat_name='Inactive')}")
            return redirect('ticket-detail', pk=(pk))
        else:
            if comment_form.is_valid:
                comment_data = request.POST.dict()
                comment_description = comment_data.get("comment_description")
                status = request.POST['status']
                update_ticket_status(request, status, ticket)
                comment = Comment(comment_description=comment_description, comment_user=request.user, ticket=ticket)
                comment.save()
                messages.success(request, f'The comment has been successfully posted.')
                return redirect('ticket-detail', pk=(pk))
            else:
                messages.error(request, comment_form.errors)
    else:
        comment_form = CommentForm()

    context = {
        'status': status,
        'page_obj': page_obj,
        'ticket': ticket,
        'comment_form': comment_form,
        'comment': comment,
        'attachment': attachment
    }
    return render(request , "ticket/ticket-detail.html" , context)

def update_ticket_status(request, status, ticket):
    print(status)
    pk = ticket.ticket_id
    status_id = Status.objects.get(stat_id=status)
    return Ticket.objects.filter(ticket_id=pk).update(status = status_id)

@login_required()
def dashboard(request):
    all_tickets = Ticket.objects.all().values('category').annotate(catname=F('category_id__cat_name'), total=Count('category')).order_by('-total')
    ticket_category = Ticket.objects.all().values('category').annotate(catname=F('category_id__cat_name'), total=Count('category')).order_by('-total')
    ticket_status = Ticket.objects.all().values('status').annotate(statname=F('status_id__stat_name'), total=Count('status')).order_by('-total')
    ticket_product = Ticket.objects.all().values('product').annotate(prodname=F('product_id__prod_name'), total=Count('product')).order_by('-total')
    ticket_product_open = Ticket.objects.all().values('status__stat_name', 'client__client_name', 'product_id__prod_name').annotate(prodname=F('product_id__prod_name'), total=Count('product')).order_by('-total')
    ticket_client = Ticket.objects.all().values('client').annotate(clientname=F('client__client_name'), count=Count('ticket_code'), total=Count('client')).order_by('-total')
    all_ticket_count = Ticket.objects.all().annotate(count=Count('ticket_code'))
    today = timezone.now()
    team = Profile.objects.get(user=request.user)
    team_tickets = Ticket.objects.filter(ticket_owner=team.team_id)
    ticket_created_today = Ticket.objects.filter(date_added__month=today.month, date_added__day=today.day, date_added__year=today.year).annotate(count=Count('ticket_id')).values('ticket_id','ticket_code', 'date_added', 'last_update', 'ticket_owner_id__team_name', 'status_id__stat_name')
    ticket_closed_today = Ticket.objects.filter(date_closed__month=today.month, date_closed__day=today.day, date_closed__year=today.year)\
        .annotate(perc=Count('ticket_id') / Ticket.objects.all().count() * 100,count=Count('ticket_id')).values('ticket_id','ticket_code', 'date_added', 'last_update', 'ticket_owner_id__team_name')
    ticket_due_today = Ticket.objects.filter(date_added__lte=today-timedelta(days=3), date_closed=None).annotate(owner=F('ticket_owner_id__team_name'),count=Count('ticket_id')).values('ticket_id','ticket_code', 'date_added', 'last_update', 'ticket_owner_id__team_name')

    print(f"{ticket_closed_today.values_list()}")
    print(f"{ticket_closed_today.values()}")

    open_tickets = Ticket.objects.filter(status=1).values('category')
    user = User.objects.get(id=request.user.id)
    context = {
        'team_tickets': team_tickets,
        'ticket_created_today': ticket_created_today,
        'ticket_closed_today': ticket_closed_today,
        'ticket_due_today': ticket_due_today,
        'ticket_category': ticket_category,
        'all_ticket_count': all_ticket_count,
        'ticket_client': ticket_client,
        'ticket_product_open': ticket_product_open,
        'ticket_product': ticket_product,
        'first_name': user.first_name,
        'open_tickets': open_tickets,
        'all_tickets': all_tickets,
        'ticket_status': ticket_status,
        'software': Ticket.objects.filter(category='1'),
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def create_project(request):
    p_form = ProjectForm
    if request.method == 'POST':
        if p_form.is_valid:
            p_form = ProjectForm(request.POST)
            p_form.instance.proj_author = request.user
            p_form.save()
            messages.success(request, "Project successfully created.")
            return redirect('project-list')
        else:
            messages.error(request, p_form.errors)
    context = {
        'p_form': p_form
    }

    return render(request, 'project/project-form.html', context)

@login_required
def create_ticket(request):
    if request.method == 'POST':
        t_form = TicketForm(request.POST)
        ta_form = TicketAttachmentForm(request.POST , request.FILES)

        if t_form.is_valid:
            files = request.FILES.getlist('file')
            t_form.instance.ticket_author = request.user
            t_form.instance.last_update_by = request.user
            t_form.save()

            if ta_form.is_valid():
                for f in files:
                    print(f'Start Saved: {f}')
                    ta = TicketAttachment(ticket=t_form.instance, file=f, uploaded_by=request.user)
                    ta.save()
                    print(f'End Saved: {f}')
                #  upload_file (user, t_form, ta_form, f)

            messages.success(request, f'The ticket has been successfully created!')
            return redirect('ticket-list')
        else:
            messages.error(request, ta_form.errors)
    else:
        t_form = TicketForm(request.POST)
        ta_form = TicketAttachmentForm(request.POST , request.FILES,)
    context = {
        't_form': t_form,
        'ta_form': ta_form
    }
    return render(request , "ticket/ticket-form.html" , context)





@login_required
def ticket_update(request, pk):
    ticket = Ticket.objects.get(ticket_id=pk)
    ticket_values = {'title': ticket.title , 'description': ticket.description, 'client': ticket.client, 'category': ticket.category, 'sub_category': ticket.sub_category, 'project': ticket.project, 'product': ticket.product, 'module': ticket.module, 'ticket_owner': ticket.ticket_owner, 'status': ticket.status, 'issue:': ticket.hot_issue}
    closed = Status.objects.get(stat_name='Closed')
    if request.method == 'POST':
        t_form = TicketForm(request.POST)
        ta_form = TicketAttachmentForm(request.POST , request.FILES)

        if t_form.is_valid:
            files = request.FILES.getlist('file')
            if ta_form.is_valid():
                for f in files:
                    print(f'Start Saved: {f}')
                    ta = TicketAttachment(ticket=ticket, file=f, uploaded_by=request.user)
                    ta.save()
                    print(f'End Saved: {f}')

                ticket_data = request.POST.dict()
                title = ticket_data.get("title")
                description =  ticket_data.get("description")
                client =  ticket_data.get("client")
                category =  ticket_data.get("category")
                sub_category =  ticket_data.get("sub_category")
                project =  ticket_data.get("project")
                product =  ticket_data.get("product")
                module =  ticket_data.get("module")
                status =  ticket_data.get("status")
                issue =  ticket_data.get("issue")
                ticket_owner =  ticket_data.get("ticket_owner")
                if int(status) == int(closed.stat_id):
                    date_closed = timezone.now()
                else:
                    date_closed = None

                print(f"Status submitted is: {status} = {closed.stat_id} hence {date_closed}")
                t_form.instance.last_update_by = request.user
                Ticket.objects.filter(ticket_id=pk).update(title = title, description = description, client = client,
                                                           category = category,
                                                           sub_category = sub_category,
                                                           project = project,
                                                           product = product,
                                                           module = module,
                                                           status = status,
                                                           hot_issue = issue,
                                                           ticket_owner = ticket_owner,
                                                           date_closed = date_closed)
            messages.success(request, f'The ticket has been successfully updated!')
            return redirect('ticket-detail', pk=(pk))
        else:
            messages.error(request, ta_form.errors)
    else:
        t_form = TicketForm(initial=ticket_values)
        ta_form = TicketAttachmentForm(request.POST , request.FILES,)

    ticket_attachment = TicketAttachment.objects.filter(ticket=pk).values("file")
    tickets = Ticket.objects.get(ticket_id=pk)

    context = {
    'tickets': tickets,
    'attachments': ticket_attachment,
    't_form': t_form,
    'ta_form': ta_form

    }
    return render(request , "ticket/ticket-form.html" , context)





def ticket_list(request):
    form = UploadFileForm(request.FILES)
    ctx = {}
    url_parameter = request.GET.get("t")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        tickets = ticket_filter(url_filter, url_parameter)
        print(f"Tickets are {tickets.values()}")
        page_obj = create_pagination(tickets, request)
    else:
        tickets = Ticket.objects.all().order_by('-date_added')
        page_obj = create_pagination(tickets, request)

    ctx["form"] = form
    ctx["tickets"] = tickets
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="ticket/tickets-partial-list.html",
            context={
                "form": form,
                "tickets": tickets,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    elif request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            print(f'Column: \n {io_string}')
            next(io_string)
            try:
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    _, created = Ticket.objects.update_or_create(
                        title = column[0],
                        description = column[1],
                        client = Client.objects.get(client_code=column[2]),
                        category = Category.objects.get(cat_code=column[3]),
                        sub_category = SubCategory.objects.get(scat_code=column[4]),
                        project = Project.objects.get(proj_code=column[5]),
                        product = Product.objects.get(prod_code=column[6]),
                        module = Module.objects.get(mod_code=column[7]),
                        status = Status.objects.get(stat_code=column[8]),
                        hot_issue = HotIssue.objects.get(hi_code=column[9]),
                        ticket_owner = Team.objects.get(team_code=column[10]),
                        ticket_author = Profile.objects.get(user_code=column[11]).user,
                        last_update_by =Profile.objects.get(user_code=column[11]).user
                    )
                return render(request, 'ticket/ticket-list.html', ctx)

            except Exception as e:
                messages.error(request, f"There was an error on line {column} Please make sure you are using the correct template.")
                print(e)
            finally:
                return render(request, 'ticket/ticket-list.html', ctx)
        else:
            print(form.errors)

    return render(request, 'ticket/ticket-list.html', context=ctx)


def project_list(request):
    ctx = {}
    url_parameter = request.GET.get("p")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        projects = project_filter(url_filter, url_parameter)
        print(f"Projects are {projects.values()}")
        page_obj = create_pagination(projects, request)
    else:
        projects = Project.objects.all().order_by('-proj_date_added')
        print(f"all projects are {projects}")
        page_obj = create_pagination(projects, request)
        print(f"all projects page_obj are {page_obj}")

    ctx["projects"] = projects
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="project/projects-partial-list.html",
            context={
                "projects": projects,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'project/project-list.html', context=ctx)

def product_type_list(request):
    ctx = {}
    url_parameter = request.GET.get("p")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        product_types = product_type_filter(url_filter, url_parameter)
        print(f"product_types are {product_types.values()}")
        page_obj = create_pagination(product_types, request)
    else:
        product_types = ProductType.objects.all().order_by('-prod_type_date_added')
        print(f"all product_types are {product_types}")
        page_obj = create_pagination(product_types, request)
        print(f"all product_typess page_obj are {page_obj}")

    ctx["product_types"] = product_types
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="product_type/product-types-partial-list.html",
            context={
                "product_types": product_types,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'product_type/product-type-list.html', context=ctx)




    return render(request, 'dashboard/dashboard.html', context)

@login_required
def create_product_type(request):
    p_form = ProductTypeForm
    if request.method == 'POST':
        try:
            p_form = ProductTypeForm(request.POST)
            if p_form.is_valid:
                p_form.instance.prod_type_author = request.user
                p_form.instance.prod_type_date_added = timezone.now()
                p_form.instance.prod_type_last_update_by = request.user
                p_form.instance.prod_type_last_update = timezone.now()

                p_form.save()
                messages.success(request, "Product type successfully created.")
                return redirect('product-type-list')
            else:
                print(p_form.errors)
                messages.error(request, p_form.errors)
        except Exception as e:
            print(f"error is {e}")
    context = {
        'p_form': p_form
    }

    return render(request, 'product_type/product-type-form.html', context)

class ProductTypeDetailView(DetailView):
    model = ProductType
    template_name = 'product_type/product-type-detail.html'  # <app>/<model>_>viewtype>.html

@login_required
def update_product_type(request, pk):
    prod_type = ProductType.objects.get(prod_type_id=pk)
    prod_type_values = {'prod_type_name': prod_type.prod_type_name , 'prod_type_description': prod_type.prod_type_description}
    if request.method == 'POST':
        p_form = ProductTypeForm(request.POST)
        if p_form.is_valid():
            prod_type_data = request.POST.dict()
            prod_type_name = prod_type_data.get("prod_type_name")
            prod_type_description = prod_type_data.get("prod_type_description")
            prod_type_code = prod_type_data.get("prod_type_code")
            prod_type_last_update  = timezone.now()
            prod_type_last_update_by = request.user
            ProductType.objects.filter(prod_type_id=pk).update(prod_type_name=prod_type_name, prod_type_description=prod_type_description,
                                                         prod_type_code=prod_type_code,
                                                         prod_type_last_update=prod_type_last_update,
                                                         prod_type_last_update_by=prod_type_last_update_by
                                                         )
            messages.success(request, f'The Product type has been successfully updated!')
            return redirect('product-type-detail', pk=(pk))
        else:
            messages.error(request, p_form.errors)
    else:
        p_form = ProductTypeForm(initial=prod_type_values)

    prod_type = ProductType.objects.get(prod_type_id=pk)

    context = {
        'prod_type': prod_type,
        'p_form': p_form,
    }
    return render(request, "product_type/product-type-form.html", context)



def client_list(request):
    ctx = {}
    url_parameter = request.GET.get("c")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        clients = client_filter(url_filter, url_parameter)
        page_obj = create_pagination(clients, request)
        print(f"Clients filtered {clients.values()}")
    else:
        clients = Client.objects.all().order_by('-client_date_added')
        print(f"all Clients are {clients}")
        page_obj = create_pagination(clients, request)
        print(f"all Clients page_obj are {page_obj}")

    ctx["clients"] = clients
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="client/clients-partial-list.html",
            context={
                "clients": clients,
                "page_obj": page_obj}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'client/client-list.html', context=ctx)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project-detail.html'  # <app>/<model>_>viewtype>.html





@login_required
def update_project(request, pk):
    project = Project.objects.get(proj_id=pk)
    project_values = {'proj_name': project.proj_name , 'proj_description': project.proj_description, 'proj_client': project.proj_client, 'proj_code': project.proj_code, 'proj_manager': project.proj_manager, 'proj_warranty_end': project.proj_warranty_end, 'proj_status': project.proj_status}
    if request.method == 'POST':
        p_form = ProjectForm(request.POST)
        if p_form.is_valid():
            project_data = request.POST.dict()
            proj_name = project_data.get("proj_name")
            proj_description = project_data.get("proj_description")
            proj_client = project_data.get("proj_client")
            proj_code = project_data.get("proj_code")
            proj_manager = project_data.get("proj_manager")
            proj_warranty_end = project_data.get("proj_warranty_end")
            print(f"warranty end is : {proj_warranty_end} {type(proj_warranty_end)}")
            proj_status = project_data.get("proj_status")

            p_form.instance.last_update = timezone.now()
            p_form.instance.last_update_by = request.user
            Project.objects.filter(proj_id=pk).update(proj_name=proj_name, proj_description=proj_description,
                                                         proj_code=proj_code,
                                                         proj_manager=proj_manager,
                                                         proj_warranty_end=proj_warranty_end,
                                                         proj_status=proj_status
                                                         )
            messages.success(request, f'The project has been successfully updated!')
            return redirect('project-detail', pk=(pk))
        else:
            messages.error(request, p_form.errors)
    else:
        p_form = ProjectForm(initial=project_values)

    project = Project.objects.get(proj_id=pk)

    context = {
        'project': project,
        'p_form': p_form,
    }
    return render(request, "project/project-form.html", context)




class CategoryListView(ListView):
    model = Category
    template_name = 'category/category-list.html'
    context_object_name = 'tcategories'
    paginate_by = 5
    ordering = ['-cat_date_added']

def category_list(request):
    ctx = {}
    url_parameter = request.GET.get("c")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        categories = category_filter(url_filter, url_parameter)
        print(f"categories are {categories.values()}")
        page_obj = create_pagination(categories, request)
    else:
        categories = Category.objects.all().order_by('-cat_date_added')
        print(f"all categories are {categories}")
        page_obj = create_pagination(categories, request)
        print(f"all categories page_obj are {page_obj}")

    ctx["categories"] = categories
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="category/categories-partial-list.html",
            context={
                "categories": categories,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'category/category-list.html', context=ctx)


def subcategory_list(request):
    ctx = {}
    url_parameter = request.GET.get("sc")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        subcategories = subcategory_filter(url_filter, url_parameter)
        print(f"subcategories are {subcategories.values()}")
        page_obj = create_pagination(subcategories, request)
    else:
        subcategories = SubCategory.objects.all().order_by('-scat_date_added')
        print(f"all subcategories are {subcategories}")
        page_obj = create_pagination(subcategories, request)
        print(f"all subcategories page_obj are {page_obj}")

    ctx["subcategories"] = subcategories
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="subcategory/subcategories-partial-list.html",
            context={
                "subcategories": subcategories,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'subcategory/subcategory-list.html', context=ctx)

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category-detail.html'  # <app>/<model>_>viewtype>.html


class SubCategoryListView(ListView):
    model = SubCategory
    template_name = 'subcategory/subcategory-list.html'
    context_object_name = 'scategories'
    ordering = ['-scat_date_added']
    paginate_by = 5


class SubCategoryDetailView(DetailView):
    model = SubCategory
    template_name = 'subcategory/subcategory-detail.html'  # <app>/<model>_>viewtype>.html

class ProjectListView(ListView):
    model = Project
    template_name = 'project/project-list.html'
    context_object_name = 'projects'
    ordering = ['-proj_date_added']
    paginate_by = 5





class ProductListView(ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    ordering = ['-prod_date_added']
    paginate_by = 5

def product_list(request):
    ctx = {}
    url_parameter = request.GET.get("p")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        products = product_filter(url_filter, url_parameter)
        print(f"products are {products.values()}")
        page_obj = create_pagination(products, request)
    else:
        products = Product.objects.all().order_by('-prod_date_added')
        print(f"all products are {products}")
        page_obj = create_pagination(products, request)
        print(f"all products page_obj are {page_obj}")

    ctx["products"] = products
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="product/products-partial-list.html",
            context={
                "products": products,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'product/product-list.html', context=ctx)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-detail.html'  # <app>/<model>_>viewtype>.html



class StatusListView(ListView):
    model = Status
    template_name = 'status/status-list.html'
    context_object_name = 'status'
    ordering = ['-stat_date_added']
    paginate_by = 5


class StatusDetailView(DetailView):
    model = Status
    template_name = 'status/status-detail.html'  # <app>/<model>_>viewtype>.html









class ClientListView(ListView):
    model = Client
    template_name = 'client/client-list.html'
    context_object_name = 'clients'
    ordering = ['client_name']
    paginate_by = 5


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client-detail.html'  # <app>/<model>_>viewtype>.html









class HotIssueListView(ListView):
    model = HotIssue
    template_name = 'hotissue/hot-issue-list.html'
    context_object_name = 'hotissue'
    ordering = ['-hi_date_added']
    paginate_by = 5


class HotIssueDetailView(DetailView):
    model = HotIssue
    template_name = 'hotissue/hot-issue-detail.html'  # <app>/<model>_>viewtype>.html





class ModuleDetailView(DetailView):
    model = Module
    template_name = 'module/module-detail.html'  # <app>/<model>_>viewtype>.html


def about(request):
    return render(request, 'ticket/about.html', {'title': 'About'})


"""
#########################
Create views
#########################
"""


class HotIssueCreateView(LoginRequiredMixin, CreateView):
    model = HotIssue
    fields = ['hi_id', 'hi_name', 'hi_description', 'hi_code', 'hi_product', 'hi_module', 'hi_status']
    template_name = 'hotissue/hot-issue-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/hot-issue/list/'

    def form_valid(self, form):
        form.instance.hi_author = self.request.user
        return super().form_valid(form)


class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ['mod_name', 'mod_description', 'product', 'mod_code', 'mod_status']
    template_name = 'module/module-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/module/list/'

    def form_valid(self, form):
        form.instance.mod_author = self.request.user
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['cat_name', 'cat_description', 'cat_code', 'cat_status']
    template_name = 'category/category-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/category/list/'

    def form_valid(self, form):
        form.instance.cat_author = self.request.user
        return super().form_valid(form)


class SubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    fields = ['scat_name', 'scat_description', 'category', 'scat_code', 'scat_status']
    template_name = 'subcategory/subcategory-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/subcategory/list/'

    def form_valid(self, form):
        form.instance.scat_author = self.request.user
        return super().form_valid(form)



@login_required
def create_product(request):
    p_form = ProductForm
    if request.method == 'POST':
        try:
            p_form = ProductForm(request.POST)
            if p_form.is_valid:
                p_form.instance.prod_author = request.user
                p_form.instance.prod_date_added = timezone.now()
                p_form.instance.prod_last_update_by = request.user
                p_form.instance.prod_last_update = timezone.now()
                p_form.save()
                messages.success(request, "Product successfully created.")
                return redirect('product-list')
            else:
                print(p_form.errors)
                messages.error(request, p_form.errors)
        except Exception as e:
            print(f"error is {e}")
    context = {
        'p_form': p_form
    }

    return render(request, 'product/product-form.html', context)

@login_required
def create_module(request):
    m_form = ModuleForm
    if request.method == 'POST':
        try:
            m_form = ModuleForm(request.POST)
            if m_form.is_valid:
                m_form.instance.mod_author = request.user
                m_form.instance.mod_date_added = timezone.now()
                m_form.instance.mod_last_update_by = request.user
                m_form.instance.mod_last_update = timezone.now()
                m_form.save()
                messages.success(request, "Module successfully created.")
                return redirect('module-list')
            else:
                print(m_form.errors)
                messages.error(request, m_form.errors)
        except Exception as e:
            print(f"error is {e}")
    context = {
        'm_form': m_form
    }
    return render(request, 'module/module-form.html', context)

def module_list(request):
    ctx = {}
    url_parameter = request.GET.get("m")
    url_filter = request.GET.get("f")

    print(f"URL param {url_parameter} Filter: {url_filter}")
    if url_parameter:
        modules = module_filter(url_filter, url_parameter)
        print(f"modules are {modules.values()}")
        page_obj = create_pagination(modules, request)
    else:
        modules = Module.objects.all().order_by('-mod_date_added')
        print(f"all products are {modules}")
        page_obj = create_pagination(modules, request)
        print(f"all products page_obj are {page_obj}")

    ctx["modules"] = modules
    ctx["page_obj"] = page_obj

    if request.is_ajax():
        html = render_to_string(
            template_name="module/modules-partial-list.html",
            context={
                "modules": modules,
                "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'module/module-list.html', context=ctx)

@login_required
def update_module(request, pk):
    module = Module.objects.get(mod_id=pk)
    module_values = {'mod_name': module.mod_name , 'mod_description': module.mod_description, 'product': module.product, 'mod_code': module.mod_code, 'mod_status': module.mod_status}
    if request.method == 'POST':
        m_form = ModuleForm(request.POST)
        if m_form.is_valid():
            module_data = request.POST.dict()
            mod_name = module_data.get("mod_name")
            mod_description = module_data.get("mod_description")
            product = module_data.get("product")
            mod_code = module_data.get("mod_code")
            mod_status = module_data.get("mod_status")
            mode_last_update  = timezone.now()
            mod_last_update_by = request.user
            Module.objects.filter(mod_id=pk).update(mod_name=mod_name, mod_description=mod_description,
                                                         product=product,
                                                         mod_code=mod_code,
                                                         mod_status=mod_status,
                                                         mod_last_update=mode_last_update,
                                                         mod_last_update_by=mod_last_update_by
                                                         )
            messages.success(request, f'The module has been successfully updated!')
            return redirect('module-detail', pk=pk)
        else:
            messages.error(request, m_form.errors)
    else:
        m_form = ModuleForm(initial=module_values)

    module = Module.objects.get(mod_id=pk)

    context = {
        'module': module,
        'm_form': m_form,
    }
    return render(request, "module/module-form.html", context)


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['stat_name', 'stat_description', 'stat_code']
    template_name = 'status/status-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/status/list/'

    def form_valid(self, form):
        form.instance.stat_author = self.request.user
        return super().form_valid(form)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['client_id', 'client_name', 'client_address', 'account_manager', 'client_code', 'client_status']
    template_name = 'client/client-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/client/list/'

    def form_valid(self, form):
        form.instance.client_author = self.request.user
        return super().form_valid(form)


@login_required
def create_client(request):
    c_form = ClientForm
    if request.method == 'POST':
        if c_form.is_valid:
            c_form = ClientForm(request.POST)
            c_form.instance.client_author = request.user
            c_form.instance.last_update = timezone.now()
            c_form.save()
            messages.success(request, "Project successfully created.")
            return redirect('client-list')
        else:
            messages.error(request, c_form.errors)
    context = {
        'c_form': c_form
    }

    return render(request, 'client/client-form.html', context)





"""
#########################
Update views
#########################
"""


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['proj_name', 'proj_description', 'proj_code', 'proj_manager', 'proj_warranty_end', 'proj_status']
    template_name = 'project/project-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/project/list'

    def form_valid(self, form):
        form.instance.proj_manager = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['cat_name', 'cat_description', 'cat_code', 'cat_status']
    template_name = 'category/category-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/category/list/'

    def form_valid(self, form):
        form.instance.catAuthor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class SubCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubCategory
    fields = ['scat_name', 'scat_description', 'category', 'scat_code', 'scat_status']
    template_name = 'subcategory/subcategory-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/subcategory/list/'

    # def form_valid(self, form):
    #   form.instance.scatAuthor = self.request.user
    #  return super().form_valid(form)

    def test_func(self):
        subcategory = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['prod_name', 'prod_code', 'prod_description', 'client', 'prod_type', 'prod_status']
    template_name = 'product/product-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/product/list/'

    def form_valid(self, form):
        form.instance.prod_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.prod_author:
            return True
        return False


class StatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Status
    fields = ['stat_name', 'stat_description', 'stat_code']
    template_name = 'status/status-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/status/list/'

    def form_valid(self, form):
        form.instance.stat_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        client = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['client_name', 'client_address', 'account_manager', 'client_code', 'client_status']
    template_name = 'client/client-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/client/list/'

    """
    def form_valid(self, form):
        #form.instance.clientAuthor = self.request.user
        form.instance.clientAuthor = self.request.is_staff
        return super().form_valid(form)
    """

    def test_func(self):
        client = self.get_object()
        # if self.request.user == client.clientAuthor:
        if self.request.user.is_staff:
            return True
        return False

@login_required
def update_client(request, pk):
    client = Client.objects.get(client_id=pk)
    client_values = {'client_name': client.client_name , 'client_address': client.client_address, 'account_manager': client.account_manager, 'client_code': client.client_code, 'client_status': client.client_status}
    if request.method == 'POST':
        c_form = ClientForm(request.POST)
        if c_form.is_valid():
            client_data = request.POST.dict()
            client_name = client_data.get("client_name")
            client_address = client_data.get("client_address")
            account_manager = client_data.get("account_manager")
            client_code = client_data.get("client_code")
            client_status = client_data.get("client_status")
            client_last_update = timezone.now()
            client_last_update_by = request.user

            Client.objects.filter(client_id=pk).update(client_name=client_name, client_address=client_address,
                                                         account_manager=account_manager,
                                                         client_code=client_code,
                                                         client_status=client_status,
                                                         client_last_update=client_last_update,
                                                         client_last_update_by=client_last_update_by
                                                         )
            messages.success(request, f'The client details has been successfully updated!')
            return redirect('client-detail', pk=(pk))
        else:
            messages.error(request, c_form.errors)
    else:
        c_form = ClientForm(initial=client_values)
        c_form = ClientForm(initial=client_values)

    client = Client.objects.get(client_id=pk)

    context = {
        'client': client,
        'c_form': c_form,
    }
    return render(request, "client/client-form.html", context)


class HotIssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HotIssue
    fields = ['hi_name', 'hi_description', 'hi_code', 'hi_product', 'hi_module', 'hi_status']
    template_name = 'hotissue/hot-issue-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/hot-issue/list/'

    def form_valid(self, form):
        form.instance.hi_last_update_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        hotissue = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Module
    fields = ['mod_name', 'mod_description', 'product', 'mod_code', 'mod_status']
    template_name = 'module/module-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/module/list/'

    def form_valid(self, form):
        form.instance.mod_author = self.request.user
        return super().form_valid(form)



"""
#########################
Delete views
#########################
"""

class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module
    success_url = '/module/list/'
    template_name = 'module/module_confirm_delete.html'

    def test_func(self):
        module = self.get_object()
        if self.request.user == module.mod_author:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/project/list/'
    template_name = 'project/project_confirm_delete.html'

    def test_func(self):
        project = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/ticket/list/'
    template_name = 'ticket/ticket_confirm_delete.html'

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.ticket_author:
            return True
        return False


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = '/category/'

    def test_func(self):
        client = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class SubCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubCategory
    success_url = '/subcategory/'
    template_name = 'subcategory/subcategory_confirm_delete.html'

    def test_func(self):
        subcategory = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/product/list/'
    template_name = 'product/product_confirm_delete.html'

    def test_func(self):
        client = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class StatusDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Status
    success_url = '/status/list'
    template_name = 'status/status_confirm_delete.html'

    def test_func(self):
        client = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = '/client/list/'
    template_name = 'client/client_confirm_delete.html'  # <app>/<model>_>viewtype>.html

    def test_func(self):
        client = self.get_object()
        # if self.request.user == client.clientAuthor:
        if self.request.user.is_staff:
            return True
        return False


class HotIssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = HotIssue
    success_url = '/hot-issue/list/'
    template_name = 'hotissue/hot-issue_confirm_delete.html'

    def test_func(self):
        hotissue = self.get_object()
        if self.request.user == hotissue.hiAuthor:
            return True
        return False




