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

    def __str__(self) -> str:
        return f"{self.user} - {self.title}"
    

    def todo_date_filter(filter_number,todos):
        now = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
        delta_today = datetime.timedelta(hours=now.hour,minutes=now.minute,seconds=now.second)
        if filter_number == "1" :
            todo = todos.filter(created__gte=now - delta_today)
            return todo
        if filter_number == "2" :
            delta_yes = datetime.timedelta(days=1,hours=now.hour,minutes=now.minute,seconds=now.second)
            todo = todos.filter(created__range=(now - delta_yes,now - delta_today))
            return  todo
        if filter_number == "3" :
            delta_week = datetime.timedelta(days=6,hours=now.hour,minutes=now.minute,seconds=now.second)
            todo = todos.filter(created__gte=now - delta_week)
            return todo
        return None
        # if filters.get("Two"):
        # if filters.get("Three"):
# Create your models here.
