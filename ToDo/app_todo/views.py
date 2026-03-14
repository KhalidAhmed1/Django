from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm

class TodoListView(ListView):
    model               = Todo
    template_name       = 'app_todo/todo_list.html'
    context_object_name = 'todos'
    ordering            = ['-created_at']

class TodoCreateView(CreateView):
    model         = Todo
    form_class    = TodoForm
    template_name = 'app_todo/todo_form.html'
    success_url   = reverse_lazy('todo-list')

class TodoUpdateView(UpdateView):
    model         = Todo
    form_class    = TodoForm
    template_name = 'app_todo/todo_form.html'
    success_url   = reverse_lazy('todo-list')

class TodoDeleteView(DeleteView):
    model         = Todo
    template_name = 'app_todo/todo_confirm_delete.html'
    success_url   = reverse_lazy('todo-list')