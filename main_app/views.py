import os.path
from django.urls import reverse
from django.utils import timezone
from .forms import UploadFileForm
from django.shortcuts import render
from main_app.models import Command
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

# Create your views here.

class CommandListView(ListView):

    model = Command
    paginate_by = 100  # if pagination is desired
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def do_action_view(request, action):
    try:
        command = Command.objects.get(name=action)
        activate_action(command)
        return HttpResponseRedirect(reverse('main_app:home'))

    except:
        return HttpResponseRedirect(reverse('main_app:upload'))

def activate_action(command):
    try:
        exec(open(f'/main_app/commands/{command}.py').read())
    except Exception as e:
        print(e.args)


def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            add_action(request.FILES['file'], request.POST['title'])
            return HttpResponseRedirect(reverse('main_app:home'))

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def add_action(file, name):
    save_path = 'main_app/commands/'
    completeName = os.path.join(save_path, name + ".py")

    with open(completeName, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    with open('main_app/commands/__init__.py','a') as imports:
        imports.write(f'\nfrom .{name} import {name}')

    c = Command(name=name)
    c.save()
