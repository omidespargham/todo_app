from datetime import datetime
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from todo.forms import TodoAddForm, TodoEditForm, TodoSearchForm
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
            todo_filters = request.GET.dict()
            request.session["filter"] = { "data":todo_filters }
        elif not request.session.get("filter") == None:
            todo_filters = request.session["filter"]["data"]
        if todo_filters:
            todos = Todo.todo_date_and_done_filter(todos,**todo_filters)
            search_form = self.form_class(todo_filters)
        return render(request, self.template_name, {"todos": todos, "search_form": search_form})

class TodoDetailView(LoginRequiredMixin,View):
    template_name = "todo/todo_detail.html"
    def get(self,request,todo_id):
        try:
            todo = Todo.objects.get(pk = todo_id)
            return render(request,self.template_name,{"todo":todo})
        except Todo.DoesNotExist:
            messages.error(request,"todo voojood nadarad ! ")
            return redirect("todo:show_todos")
 
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
    form_class = TodoEditForm
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
            return redirect("todo:todo_detail",todo.id)
        except Todo.DoesNotExist:
            messages.error(request, "todo voojood nadarad ! ", "danger")
            return redirect("todo:todo_detail",todo.id)

class TodoDoneEditView(LoginRequiredMixin,View):
    def get(self,request,todo_id):
        todo = Todo.objects.get(pk=todo_id)
        todo.done = not todo.done
        todo.save()
        return redirect("todo:todo_detail",todo.id)
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
            cl = form.cleaned_data
            todo = Todo(title=cl["title"], user=request.user)
            todo.slug = slugify(cl["title"][:30])
            todo.time_to_do = cl["time_to_do"] if cl.get("time_to_do") else datetime.now()
            todo.save()
            messages.success(request, "todo sakhte shod ! ", "success")
            return redirect("todo:show_todos")
        return render(request, self.template_name, {"form": form})



# Create your views here.
