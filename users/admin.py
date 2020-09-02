# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm , UserChangeForm
from .models import User
from .models import Profile, Team
from tickets.models import Product, Project, Client, Status, Ticket, HotIssue, Module, TicketAttachment


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment

class TicketAdmin(admin.ModelAdmin):
    inlines = [
        TicketAttachmentInline,
    ]

admin.site.register(Ticket, TicketAdmin)

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email' , 'first_name' , 'last_name']


admin.site.register(User , UserAdmin)
admin.site.register(Profile)
admin.site.register(TicketAttachment)
admin.site.register(Team)
#admin.site.register(Ticket)
admin.site.register(Module)
admin.site.register(HotIssue)
admin.site.register(Status)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Project)