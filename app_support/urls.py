"""app_support URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf

    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  pa
    
    th('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include # new
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name='user-profile'),
    path('team/list', user_views.TeamListView.as_view(), name='team-list'),
    path('team/new', user_views.TeamCreateView.as_view(), name='team-create'),
    path('team/<int:pk>/', user_views.TeamDetailView.as_view(), name='team-detail'),
    path('team/<int:pk>/update/', user_views.TeamUpdateView.as_view(), name='team-update'),
    path('team/<int:pk>/delete/', user_views.TeamDeleteView.as_view(), name='team-delete'),
    path('user/list/', user_views.user_list, name='user-list'),
    path('user/new/', user_views.create_user, name='create-user'),
    path('user/<int:pk>/', user_views.user_detail, name='user-detail'),
    path('user/<int:pk>/update/', user_views.update_user, name='user-update'),
    path('user/<int:pk>/delete/', user_views.delete_user, name='user-delete'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # new
    path('', include('tickets.urls')), # new
    #path('users/list', user_views.UserListView , 'user-list'), # new

    #path('accounts/password/change/', user_views.password_reset),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
