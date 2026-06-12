from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChangePasswordForm, EditProfileForm, EmailAuthenticationForm, RegisterForm
from .models import User


def register_view(request):
    """Страница регистрации."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects:list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Страница входа."""
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('projects:list')
    else:
        form = EmailAuthenticationForm(request)
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта."""
    logout(request)
    return redirect('projects:list')


@login_required
def edit_profile_view(request):
    """Редактирование профиля."""
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    """Смена пароля."""
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


def user_detail_view(request, pk):
    """Страница пользователя."""
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {'user': user})


# Фильтры для страницы пользователей (Вариант 1)
FILTERS = [
    'favorited_authors',
    'authors_i_participate',
    'liked_my_projects',
    'my_participants',
]


def participants_view(request):
    """Страница всех пользователей с фильтрацией."""
    users_qs = User.objects.order_by('id')
    selected_filter = request.GET.get('filter')

    if selected_filter and request.user.is_authenticated:
        if selected_filter == 'favorited_authors':
            # Авторы избранных проектов
            project_ids = request.user.favorites.values_list('id', flat=True)
            users_qs = User.objects.filter(owned_projects__id__in=project_ids).distinct()
        elif selected_filter == 'authors_i_participate':
            # Авторы проектов, в которых я участвую
            project_ids = request.user.participated_projects.values_list('id', flat=True)
            users_qs = User.objects.filter(owned_projects__id__in=project_ids).distinct()
        elif selected_filter == 'liked_my_projects':
            # Пользователи, которым нравятся мои проекты
            my_project_ids = request.user.owned_projects.values_list('id', flat=True)
            users_qs = User.objects.filter(favorites__id__in=my_project_ids).distinct()
        elif selected_filter == 'my_participants':
            # Участники моих проектов
            my_project_ids = request.user.owned_projects.values_list('id', flat=True)
            users_qs = User.objects.filter(participated_projects__id__in=my_project_ids).distinct()
        else:
            selected_filter = None

    paginator = Paginator(users_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/participants.html', {
        'participants': page_obj,
        'active_filter': FILTERS,
        'active_skill': selected_filter,
    })