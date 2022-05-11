from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
    path("showtodos/", views.ShowTodos.as_view(), name="show_todos"),
    path("deletetodo/<int:todo_id>", views.TodoDeleteView.as_view(), name="todo_delete"),
    path("addtodo/", views.TodoAddView.as_view(), name="todo_add"),
    path("edittodo/<int:todo_id>", views.TodoEditView.as_view(), name="todo_edit"),
    

]
