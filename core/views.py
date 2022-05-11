from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

class Home(View):
    template_name = "core/home.html"


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("todo:show_todos")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request,self.template_name)
# Create your views here.
