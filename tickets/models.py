from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from users.models import User as User, Team
import datetime
from ckeditor.fields import RichTextField

date = datetime.datetime.now()


class ProductType(models.Model):
    prod_type_id = models.AutoField(primary_key=True)
    prod_type_code = models.CharField(max_length=20, blank=True,
                                 default=f'stat{date.day}{date.hour}{date.minute}{date.microsecond}',
                                 verbose_name='Code')
    prod_type_name = models.CharField(max_length=25, blank=True, default='', verbose_name="Name")
    prod_type_description = models.CharField(max_length=250, verbose_name="Description")
    prod_type_last_update = models.DateTimeField(auto_now=True)
    prod_type_last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name="prod_type_last_updated_by")
    prod_type_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    prod_type_author = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_prod_type_code(self):
        return self.prod_type_code

    def __str__(self):
        return self.prod_type_name


class Status(models.Model):
    stat_id = models.AutoField(primary_key=True)
    stat_code = models.CharField(max_length=20, blank=True, default = f'stat{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name='Code')
    stat_name = models.CharField(max_length=25, blank=True, default='', verbose_name="Name")
    stat_description = models.CharField(max_length=250, verbose_name="Description")
    stat_last_update = models.DateTimeField(auto_now=True)
    stat_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    stat_author = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def get_status_code(self):
        return self.get_status_code()

    def __str__(self):
       return self.stat_name

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_code = models.CharField(max_length=20, blank=True, default=f'client{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name="Client Code")
    client_name = models.CharField(max_length=50, blank=True, default='', verbose_name="Client name")
    client_address = models.CharField(max_length=100, verbose_name="Address")
    client_status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Status")
    client_last_update = models.DateTimeField(auto_now=True, verbose_name="Last update")
    client_last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='client_last_updated_by', null=True, blank=True)
    client_date_added = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Created on")
    account_manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Account manager", related_name='account_manager')
    client_author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Created by")

    def get_client_code(self):
        return self.client_code

    #User.add_to_class("__str__", get_first__name)

    def __str__(self):
       return self.client_name


class Project(models.Model):
    proj_id = models.AutoField(primary_key=True)
    proj_code = models.CharField(max_length=20, blank=True, default=f'proj{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name="Project Code")
    proj_name = models.CharField(max_length=25, blank=True, default='', verbose_name="Name")
    proj_description = models.CharField(max_length=250, verbose_name="Description")
    proj_client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name= "Client", related_name='project_client')
    proj_manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name= "Project Manager", related_name='project_manager')
    proj_status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name= "Status")
    proj_complete_date = models.DateTimeField(null=True, blank=True)
    proj_warranty_end = models.DateField(null=True, blank=True, verbose_name="Warranty Until")
    proj_last_update = models.DateTimeField(null=True, blank=True)
    proj_last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_last_update_by', null=True, blank=True)
    proj_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    proj_author = models.ForeignKey(User, on_delete=models.PROTECT)
    def get_author_name(self):
        return self.proj_author.fullname()

    def __str__(self):
       return self.proj_name

class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_code = models.CharField(max_length=20, blank=True, default=f'prod{date.day}{date.month}{date.hour}{date.minute}{date.microsecond}', verbose_name="Product Code")
    prod_name = models.CharField(max_length=25, blank=True, default='', verbose_name="Name")
    prod_description = models.CharField(max_length=250, verbose_name="Description")
    prod_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Product Type")
    prod_manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Product Manger", related_name='product_manager')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Client", related_name='product_client', default=0)
    prod_status = models.ForeignKey(Status, on_delete=models.PROTECT)
    prod_last_update = models.DateTimeField(auto_now=True)
    prod_last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="product_last_updated_by", null=True, blank=True)
    prod_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    prod_author = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_prod_code(self):
        return self.get_prod_code()

   # User.add_to_class("__str__", get_first__name)
    def __str__(self):
       return self.prod_name

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_code = models.CharField(max_length=20, blank=True, default=f'cat{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name="Category Code")
    cat_name = models.CharField(max_length=25, blank=True, default='', verbose_name="Name")
    cat_description = models.CharField(max_length=45, blank=True, verbose_name="Description")
    cat_status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Status")
    cat_last_update = models.DateTimeField(auto_now=True)
    cat_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    cat_author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='category_manager')

    def __str__(self):
       return self.cat_name

class SubCategory(models.Model):
    scat_id = models.AutoField(primary_key=True)
    scat_code = models.CharField(max_length=20, blank=True, default=f'subcat{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name="Subcategory Code")
    scat_name = models.CharField(max_length=25, blank=True, default='', verbose_name="Name")
    scat_description = models.CharField(max_length=45, verbose_name="Description")
    scat_status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Status")
    scat_last_update = models.DateTimeField(auto_now=True)
    scat_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Category")
    scat_author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
       return self.scat_name

class Module(models.Model):
    mod_id = models.AutoField(primary_key=True)
    mod_code = models.CharField(max_length=20, blank=True, default=f'mod{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name="Module Code")
    mod_name = models.CharField(max_length=25,verbose_name="Name")
    mod_description = models.CharField(max_length=45, verbose_name="Description")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Product")
    mod_status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Status")
    mod_last_update = models.DateTimeField(auto_now=True)
    mod_last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="mod_last_updated_by", null=True, blank=True)
    mod_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    mod_author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
       return self.mod_name

class HotIssue(models.Model):
    hi_id = models.AutoField(primary_key=True)
    hi_code = models.CharField(max_length=20, blank=True, default=f'hi{date.day}{date.hour}{date.minute}{date.microsecond}', verbose_name="Hot-issue Code")
    hi_name = models.CharField(max_length=25,verbose_name="Name")
    hi_description = models.CharField(max_length=45, verbose_name="Description")
    hi_product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Product")
    hi_module = models.ForeignKey(Module, on_delete=models.PROTECT, verbose_name="Module", blank=True, null=True)
    hi_status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Status")
    hi_last_update = models.DateTimeField(auto_now=True)
    hi_closed_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="hi_closed_by")
    hi_date_added = models.DateTimeField(auto_now_add=True, blank=True)
    hi_date_closed = models.DateTimeField(auto_now_add=True, blank=True)
    hi_author = models.ForeignKey(User, on_delete=models.PROTECT)
    hi_last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="hi_last_update_by")

    def __str__(self):
       return self.hi_name

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_description = RichTextField(verbose_name="Description", null=False, blank=False)
    comment_user = models.ForeignKey(User, on_delete=models.PROTECT)
    ticket = models.ForeignKey('Ticket', on_delete=models.PROTECT)
    comment_date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def get_comment_user(self):
        return f'{self.comment_user.first_name} {self.comment_user.last_name}'

    def __str__(self):
        return self.comment_description

class Ticket(models.Model):
    date_code = f'{date.year}{date.month}{date.day}{date.microsecond}'
    ticket_id = models.AutoField(primary_key=True)
    ticket_code = models.CharField(max_length=50, blank=True, default=f'{date_code}', verbose_name="Ticket Code")
    title = models.CharField(max_length=50)
    description = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    solution = models.ForeignKey(Comment, on_delete=models.PROTECT, related_name="comment_solution", blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    hot_issue = models.ForeignKey(HotIssue, on_delete=models.PROTECT, null = True, blank=True, verbose_name="Issue" )
    last_update = models.DateTimeField(auto_now_add=True, blank=True)
    last_update_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_by')
    date_added = models.DateTimeField(auto_now_add=True, blank=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    closed_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="resolved_by")
    ticket_owner = models.ForeignKey(Team, on_delete=models.PROTECT, verbose_name="Assigned to", related_name='ticket_owner')
    ticket_author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Created by")


    def get_team_name(self):
        return self.ticket_owner.team_name

    def __str__(self):
       return self.ticket_code
        
    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})


class TicketAttachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_attachment_id')
    file = models.FileField(upload_to="attachments", blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='uploader')

    def __str__(self):
        return f'File {self.ticket}'


class YearlyReport(models.Model):
    pass