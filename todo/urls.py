from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
    path("showtodos/", views.ShowTodos.as_view(), name="show_todos"),
    path("tododelete/<int:todo_id>", views.TodoDeleteView.as_view(), name="todo_delete"),
    path("tododetail/<int:todo_id>", views.TodoDetailView.as_view(), name="todo_detail"),
    path("todoadd/", views.TodoAddView.as_view(), name="todo_add"),
    path("todoedit/<int:todo_id>", views.TodoEditView.as_view(), name="todo_edit"),
    path("tododone/<int:todo_id>", views.TodoDoneEditView.as_view(), name="todo_done_edit"),

    

]
