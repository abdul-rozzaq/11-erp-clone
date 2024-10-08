from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.core.handlers.wsgi import WSGIRequest

from .form import (
    CreateCourseForm,
    GroupForm,
    LoginForm,
    UserRegisterForm,
    UpdateUserForm,
)
from .models import Course, Group, User


@login_required(login_url="login")
def home_page(request: WSGIRequest):

    user: User = request.user
    context = {}

    if user.role == "admin":

        if request.method == "POST":
            form = CreateCourseForm(request.POST)

            if form.is_valid():
                form.save()
        else:
            form = CreateCourseForm()

        context["courses"] = Course.objects.all()
        context["form"] = form

        return render(request, "templates_by_role/admin.html", context)

    elif user.role == "teacher":
        return render(request, "templates_by_role/teacher.html", context)

    elif user.role == "student":
        return render(request, "templates_by_role/student.html", context)

    else:
        return render(request, "templates_by_role/not_assigned.html", context)


@login_required
def settings_page(request: WSGIRequest):

    user: User = request.user

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            return redirect("home")
    else:
        form = UpdateUserForm(instance=user)

    context = {"form": form}

    return render(request, "settings.html", context)


@login_required(login_url="login")
def course_page(request: WSGIRequest, pk: int):

    context = {}
    course = Course.objects.get(pk=pk)

    if request.method == "POST":

        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.course = course
            group.save()
            form.save_m2m()

    else:
        form = GroupForm()

    context["course"] = course
    context["form"] = form

    return render(request, "admin/course.html", context)


@login_required(login_url="login")
def group_page(request: WSGIRequest, pk: int):

    context = {}
    group = Group.objects.get(pk=pk)

    if request.method == "POST":

        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()

    else:
        form = GroupForm()

    context["form"] = GroupForm(instance=group)
    context["group"] = group

    if request.user.role == 'admin':
        return render(request, "admin/group.html", context)
    else:
        return render(request, "teacher/group.html", context)


@login_required(login_url="login")
def delete_group_page(request, pk):
    group = Group.objects.get(pk=pk)
    couse_id = group.course.id

    group.delete()

    return redirect("course", pk=couse_id)


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("home")

    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def register_page(request):

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(request, "auth/register.html", {"form": form})


def logout_page(request):
    logout(request)
    return redirect("home")
