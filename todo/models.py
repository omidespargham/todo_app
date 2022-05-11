from django.db import models
from accounts.models import User
import datetime
class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="mytodos")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.title}"
    

    def todo_date_filter(filter_number,todos):
        now = datetime.datetime.now()
        if filter_number == "1" :
            return todos.filter(created__gte=now - datetime.timedelta(hours=15))
        if filter_number == "2" :
            return todos.filter(created__gte=now - datetime.timedelta(days=2))
        if filter_number == "3" :
            return todos.filter(created__gte=now - datetime.timedelta(days=10))
        return None
        # if filters.get("Two"):
        # if filters.get("Three"):
# Create your models here.
