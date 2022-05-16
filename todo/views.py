from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from todo.forms import TodoAddForm, TodoSearchForm
from todo.models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify


class ShowTodos(LoginRequiredMixin, View):
    template_name = "todo/show_todos.html"
    form_class = TodoSearchForm
    def get(self, request):
        todos = Todo.objects.filter(user=request.user).order_by("-created")
        search_form = self.form_class
        if not request.GET.get("search") == None:
            todos = todos.filter(title__contains=request.GET["search"])

            todos_filter = Todo.todo_date_filter(request.GET.get("date"), todos)
            if not todos_filter == None:
                todos = todos_filter
            search_form = self.form_class(request.GET)
            
        return render(request, self.template_name, {"todos": todos, "search_form": search_form})


    # def get(self, request):
    #     todos = Todo.objects.filter(user=request.user).order_by("-created")
    #     filter_form = TodoDateFilterForm()
    #     search_form = self.form_class
    #     if request.GET.get("search"):
    #         todos = todos.filter(title__contains=request.GET["search"])
    #         search_form = self.form_class(request.GET)
    #     todos_filter = Todo.todo_date_filter(request.GET.get("date"), todos)
    #     if not todos_filter == None:
    #         todos = todos_filter
    #         filter_form = TodoDateFilterForm(request.GET)
    #     return render(request, self.template_name, {"todos": todos, "search_form": search_form, "filter_form": filter_form})


class TodoDeleteView(LoginRequiredMixin, View):
    def get(self, request, todo_id):
        try:
            todo = Todo.objects.get(user=request.user, id=todo_id)
            todo.delete()
            messages.success(request, "todo delete shod ! ", "success")
            return redirect("todo:show_todos")
        except Todo.DoesNotExist:
            messages.error(request, "todo voojood nadarad ! ", "danger")
            return redirect("todo:show_todos")


class TodoEditView(LoginRequiredMixin, View):
    form_class = TodoAddForm
    template_name = "todo/todo_edit.html"
    def get(self, request,todo_id):
        todo = Todo.objects.get(user=request.user, id=todo_id)
        context = {
            "form": self.form_class({"title":todo.title})
        }
        return render(request, self.template_name, context)

    def post(self, request, todo_id):
        try:
            todo = Todo.objects.get(user=request.user, id=todo_id)
            form = self.form_class(request.POST)
            if form.is_valid():
                cl = form.cleaned_data
                todo.title = cl["title"]
                todo.save()
            messages.success(request, "todo update shod ! ", "success")
            return redirect("todo:show_todos")
        except Todo.DoesNotExist:
            messages.error(request, "todo voojood nadarad ! ", "danger")
            return redirect("todo:show_todos")


class TodoAddView(LoginRequiredMixin, View):
    template_name = "todo/todo_add.html"
    form_class = TodoAddForm

    def get(self, request):
        context = {
            "form": self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            todo = Todo(title=title, user=request.user)
            todo.slug = slugify(title[:30])
            todo.save()
            messages.success(request, "todo sakhte shod ! ", "success")
            return redirect("todo:show_todos")
        return render(request, self.template_name, {"form": form})



# Create your views here.
