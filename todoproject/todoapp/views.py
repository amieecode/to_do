from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import todo

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
    
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()
        return redirect('home-page')

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'user successfully registered, login now!')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exit')
            return redirect('login')

    return render(request, 'todoapp/login.html', {})  

def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required
def DeleteTask(request, id):
    get_todo = get_object_or_404(todo, user=request.user, id=id)
    get_todo.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('home-page')

@login_required
def Update(request, id):
    get_todo = todo.objects.get(todo, user=request.user, id=id)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

@login_required
def edit_task(request, id):
    #get the task to be updated 
    task = get_object_or_404(todo, user=request.user, id=id)
    
    if request.method == 'POST':
        task_name = request.POST.get('task')
        task.todo_name = task_name
        task.save()
        return redirect('home-page')

    return render(request, 'todoapp/edit_task.html', {'task': task})