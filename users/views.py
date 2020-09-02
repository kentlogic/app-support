from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserChangeForm, ProfileUpdateForm, ProfileRegisterForm
from .models import Profile, Team, User
from datetime import datetime
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been successfully created!')
            return redirect('profile')

    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {
        'form': form
    })

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        p_form.fields["birth_date"].initial = '2-22-2020'

        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been successfully updated!')
            return redirect('user-profile')
        else:
            messages.error(request, p_form.errors)
    else:
        u_form = UserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

    # try:
    #
    #     except Exception as inst:
    #     print(type(inst))    # the exception instance
    #     print(inst.args)     # arguments stored in .args
    #     print(inst)



#Views for Team

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team

    fields = ['team_name', 'team_code', 'team_desc', 'team_lead']
    template_name = 'team/team-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/team/list'

    def form_valid(self, form):
        form.instance.team_date_created_by = self.request.user
        form.instance.team_date_created = datetime.now()
        return super().form_valid(form)


class TeamListView(ListView):
    model = Team
    template_name = 'team/team-list.html'
    context_object_name = 'teams'
    paginate_by = 5
    ordering = ['-team_name']


class TeamDetailView(DetailView):
    model = Team
    template_name = 'team/team-detail.html'  # <app>/<model>_>viewtype>.html


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    fields = ['team_name', 'team_code', 'team_desc', 'team_lead']
    template_name = 'team/team-form.html'  # <app>/<model>_>viewtype>.html
    success_url = '/team/list'

    def form_valid(self, form):
      form.instance.team_date_updated_by = self.request.user
      form.instance.team_date_updated = datetime.now()
      return super().form_valid(form)

    def test_func(self):
        Team = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'team/team_confirm_delete.html'
    success_url = '/team/list'

    def test_func(self):
        client = self.get_object()
        if self.request.user.is_staff:
            return True
        return False
    
def user_list(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, "users/user-list.html", context)

def user_detail(request, pk):
    pass

def delete_user(request, pk):
    pass

def update_user(request, pk):
    pass


def create_user(request):
    u_form = UserCreationForm
    p_form = ProfileRegisterForm
    if request.method == "POST":
        u_form = UserCreationForm(request.POST)
        p_form = ProfileRegisterForm(request.POST)

        if u_form.is_valid:
            pass
        else:
            raise u_form.errors
    return render(request, 'users/create-user.html', {'u_form':u_form,
                                                      'p_form':p_form})