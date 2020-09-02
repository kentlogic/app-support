# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , PasswordChangeForm
from django.forms import DateInput , SelectDateWidget
from ckeditor.widgets import CKEditorWidget
from .models import Ticket

from tickets.models import TicketAttachment, Ticket, Comment, Project, Client, Product, ProductType, Module, Category, SubCategory, HotIssue

from django.forms import ClearableFileInput


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'client', 'category', 'sub_category', 'project', 'product', 'module', 'ticket_owner',
                  'hot_issue', 'status']


class CommentForm(forms.ModelForm):
    comment_description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Comment
        fields = ['comment_description' , ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['prod_name', 'prod_description', 'prod_code', 'prod_type', 'prod_manager', 'client', 'prod_status']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['mod_name', 'mod_description', 'product', 'mod_code', 'mod_status']

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['prod_type_name', 'prod_type_code', 'prod_type_description']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['proj_name', 'proj_description', 'proj_client', 'proj_code', 'proj_manager', 'proj_warranty_end', 'proj_status']
        widgets = {
            'proj_warranty_end': DateInput()
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'client_address', 'account_manager', 'client_code', 'client_status']



class TicketAttachmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketAttachmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TicketAttachment
        fields = ['file' , ]
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField()
    # widgets = {
    #     'file': ClearableFileInput(attrs={}),
    # }
