import self as self
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.db.models import Count , F , CharField
from django.shortcuts import render , redirect
from django.views.generic import (ListView ,
                                  DetailView ,
                                  CreateView ,
                                  UpdateView ,
                                  DeleteView , )

from .forms import TicketForm , TicketAttachmentForm, UploadFileForm, CommentForm
from users.models import Profile, CustomUser
from .models import Ticket , Category , SubCategory , Project , Product , Status , Client , HotIssue , Module , \
    TicketAttachment , Comment
from django.core.paginator import Paginator
from django.db.models import Count, Case, When, IntegerField
import datetime
from django.utils import timezone
from datetime import timedelta

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
    ticket_closed_today = Ticket.objects.filter(date_closed__month=today.month, date_closed__day=today.day, date_closed__year=today.year).annotate(count=Count('ticket_id')).values('ticket_id','ticket_code', 'date_added', 'last_update', 'ticket_owner_id__team_name')
    ticket_due_today = Ticket.objects.filter(date_added__lte=today-timedelta(days=3), date_closed=None).annotate(owner=F('ticket_owner_id__team_name'),count=Count('ticket_id')).values('ticket_id','ticket_code', 'date_added', 'last_update', 'ticket_owner_id__team_name')

    ticket_client_open = Ticket.objects.filter(status=1).values('status').annotate(status_name=F('status_id__stat_name'),clientname=F('client__client_name'), total=Count('client')).order_by('-total')
    ticket_client_closed = Ticket.objects.filter(status=2).values('status').annotate(status_name=F('status_id__stat_name'),clientname=F('client__client_name'), total=Count('client')).order_by('-total')

    open_tickets = Ticket.objects.filter(status=1).values('category')
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'team_tickets': team_tickets,
        'ticket_created_today': ticket_created_today,
        'ticket_closed_today': ticket_closed_today,
        'ticket_due_today': ticket_due_today,
        'ticket_category': ticket_category,
        'all_ticket_count': all_ticket_count,
        'ticket_client_closed': ticket_client_closed,
        'ticket_client_open': ticket_client_open,
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
                t_form.instance.ticket_author = request.user
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
            messages.success(request, f'The ticket has been successfully create!')
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

#function that generates the page_object for the pagination
def create_pagination(object, request):
    paginator = Paginator(object, 5, 0)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-date_added')
    page_obj = create_pagination(tickets, request)
    form = UploadFileForm()
    context = {
        'tickets': tickets,
        'form': form,
        'page_obj': page_obj
    }

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            data_set = csv_file.read().decode('UTF-8')
            print(f'Data set: \n {data_set}')
            io_string = io.StringIO(data_set)
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
                        ticket_owner = Profile.objects.get(user_code=column[10]).user,
                        ticket_author = Profile.objects.get(user_code=column[11]).user
                    )
                return render(request, 'ticket/ticket-list.html', context)

            except Exception as e:
                nl = '\n'
                messages.error(request, f"There was an error on line {column} Please make sure you are using the correct template.")
                print(e)
        else:
            print(form.errors)

    return render(request, 'ticket/ticket-list.html', context)



class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project-detail.html'  # <app>/<model>_>viewtype>.html


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['proj_name', 'proj_description', 'proj_code', 'proj_status']
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


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['cat_name', 'cat_description', 'cat_code', 'cat_status']
    template_name = 'category/category-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/category/'

    def form_valid(self, form):
        form.instance.cat_author = self.request.user
        return super().form_valid(form)


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category-list.html'
    context_object_name = 'tcategories'
    paginate_by = 5
    ordering = ['-cat_date_added']


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category-detail.html'  # <app>/<model>_>viewtype>.html


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['cat_name', 'cat_description', 'cat_code', 'cat_status']
    template_name = 'category/category-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/category/'

    def form_valid(self, form):
      form.instance.catAuthor = self.request.user
      return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        if self.request.user.is_staff:
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


class SubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    fields = ['scat_name', 'scat_description', 'category', 'scat_code','scat_status']
    template_name = 'subcategory/subcategory-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/subcategory/'

    def form_valid(self, form):
        form.instance.scat_author = self.request.user
        return super().form_valid(form)


class SubCategoryListView(ListView):
    model = SubCategory
    template_name = 'subcategory/subcategory-list.html'
    context_object_name = 'scategories'
    ordering = ['-scat_date_added']
    paginate_by = 5


class SubCategoryDetailView(DetailView):
    model = SubCategory
    template_name = 'subcategory/subcategory-detail.html'  # <app>/<model>_>viewtype>.html


class SubCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubCategory
    fields = ['scat_name', 'scat_description', 'category', 'scat_code', 'scat_status']
    template_name = 'subcategory/subcategory-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/subcategory/'

    # def form_valid(self, form):
    #   form.instance.scatAuthor = self.request.user
    #  return super().form_valid(form)

    def test_func(self):
        subcategory = self.get_object()
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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['proj_name', 'proj_description', 'proj_code', 'proj_client', 'proj_manager', 'proj_status']
    template_name = 'project/project-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/project/list'

    def form_valid(self, form):
        form.instance.proj_author = self.request.user
        return super().form_valid(form)


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project-list.html'
    context_object_name = 'projects'
    ordering = ['-proj_date_added']
    paginate_by = 5


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['prod_name', 'prod_description', 'prod_code', 'prod_manager', 'client', 'prod_status']
    template_name = 'product/product-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/product/list/'

    def form_valid(self, form):
        form.instance.prod_author = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    ordering = ['-prod_date_added']
    paginate_by = 5


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-detail.html'  # <app>/<model>_>viewtype>.html


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['prod_name', 'prod_code', 'prod_description']
    template_name = 'product/product-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/product/list/'

    def form_valid(self, form):
        form.instance.prod_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.prod_author:
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


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['stat_name', 'stat_description', 'stat_code']
    template_name = 'status/status-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/status/list/'

    def form_valid(self, form):
        form.instance.stat_author = self.request.user
        return super().form_valid(form)


class StatusListView(ListView):
    model = Status
    template_name = 'status/status-list.html'
    context_object_name = 'status'
    ordering = ['-stat_date_added']
    paginate_by = 5


class StatusDetailView(DetailView):
    model = Status
    template_name = 'status/status-detail.html'  # <app>/<model>_>viewtype>.html


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


class StatusDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Status
    success_url = '/status/list'
    template_name = 'status/status_confirm_delete.html'

    def test_func(self):
        client = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['client_id', 'client_name', 'client_address', 'account_manager', 'client_code', 'client_status']
    template_name = 'client/client-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/client/list/'

    def form_valid(self, form):
        form.instance.client_author = self.request.user
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    template_name = 'client/client-list.html'
    context_object_name = 'clients'
    ordering = ['client_name']
    paginate_by = 5


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client-detail.html'  # <app>/<model>_>viewtype>.html


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


class HotIssueCreateView(LoginRequiredMixin, CreateView):
    model = HotIssue
    fields = ['hi_id', 'hi_name', 'hi_description', 'hi_code', 'hi_product', 'hi_module', 'hi_status']
    template_name = 'hotissue/hot-issue-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/hot-issue/list/'

    def form_valid(self, form):
        form.instance.hi_author = self.request.user
        return super().form_valid(form)


class HotIssueListView(ListView):
    model = HotIssue
    template_name = 'hotissue/hot-issue-list.html'
    context_object_name = 'hotissue'
    ordering = ['-hi_date_added']
    paginate_by = 5


class HotIssueDetailView(DetailView):
    model = HotIssue
    template_name = 'hotissue/hot-issue-detail.html'  # <app>/<model>_>viewtype>.html


class HotIssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HotIssue
    fields = ['hi_name', 'hi_description', 'hi_code', 'hi_product','hi_module', 'hi_status']
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


class HotIssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = HotIssue
    success_url = '/hot-issue/list/'
    template_name = 'hotissue/hot-issue_confirm_delete.html'

    def test_func(self):
        hotissue = self.get_object()
        if self.request.user == hotissue.hiAuthor:
            return True
        return False


class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ['mod_name', 'mod_description', 'product', 'mod_code', 'mod_status']
    template_name = 'module/module-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/module/list/'

    def form_valid(self, form):
        form.instance.mod_author = self.request.user
        return super().form_valid(form)


class ModuleListView(ListView):
    model = Module
    template_name = 'module/module-list.html'
    context_object_name = 'modules'
    ordering = ['-mod_date_added']
    paginate_by = 5


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'module/module-detail.html'  # <app>/<model>_>viewtype>.html


class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Module
    fields = ['mod_name', 'mod_description', 'product', 'mod_code', 'mod_status']
    template_name = 'module/module-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/module/list/'

    def form_valid(self, form):
        form.instance.modAuthor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        module = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module
    success_url = '/module/list/'
    template_name = 'module/module_confirm_delete.html'

    def test_func(self):
        module = self.get_object()
        if self.request.user == module.modAuthor:
            return True
        return False


def about(request):
    return render(request, 'ticket/about.html', {'title': 'About'})



#===


class UserListView(ListView):
    model = CustomUser
    template_name = 'user/user-list.html'
    context_object_name = 'modules'
    ordering = ['-mod_date_added']
    paginate_by = 5


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user/user-detail.html'  # <app>/<model>_>viewtype>.html


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['mod_name', 'mod_description', 'prod_id', 'mod_status']
    template_name = 'user/user-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/user/list/'

    def form_valid(self, form):
        form.instance.modAuthor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.get_object()
        if self.request.user == user.modAuthor:
            return True
        return False


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    success_url = '/user/list/'
    template_name = 'user/module_confirm_delete.html'

    def test_func(self):
        user = self.get_object()
        if self.request.user == user.modAuthor:
            return True
        return False



#
# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = DocumentForm()
#     return render(request, 'ticket/upload.html', {
#         'form': form
#     })