from pyexpat import model
from django.db import models
from accounts.models import User
import datetime
import pytz
class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="mytodos")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)
    time_to_do = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.title}"
    

    # def todo_date_and_done_filter(date_filter,done_filter,search,todos):
    def todo_date_and_done_filter(todos,date,done_status,search):
        if done_status == "0" and date == "0" and not search:
            return todos
        todos = todos.filter(title__contains=search)
        if done_status == "1" :
            todos = todos.filter(done=True)
        if done_status == "2" :
            todos = todos.filter(done=False)
        now = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
        delta_today = datetime.timedelta(hours=now.hour,minutes=now.minute,seconds=now.second)
        if date == "1" :
            todos = todos.filter(created__gte=now - delta_today)
            
        if date == "2" :
            delta_yes = datetime.timedelta(days=1,hours=now.hour,minutes=now.minute,seconds=now.second)
            todos = todos.filter(created__range=(now - delta_yes,now - delta_today))
            
        if date == "3" :
            delta_week = datetime.timedelta(days=6,hours=now.hour,minutes=now.minute,seconds=now.second)
            todos = todos.filter(created__gte=now - delta_week)
        return todos
        


    # def todo_done_filter(filter_number)