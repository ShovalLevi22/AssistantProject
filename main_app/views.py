from django.shortcuts import render
from main_app.models import Command
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse
import os.path
from main_app import commands
# Create your views here.
def do_action_view(request, action):
    try:
        command = Command.objects.get(name=action)
        if command:
            file_name = f"commands.{command.path}"
            module = __import__(file_name)
            func = getattr(module, command.name)
            func()
    except:
    # else:
        # upload_file(request)
        return HttpResponseRedirect(reverse('main_app:upload'))


def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            add_action(request.FILES['file'], request.POST['title'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def add_action(file, name):
    # target = open("name.txt", "a+")
    save_path = 'C:/Users/shovi/PycharmProjects/AssistantProject/main_app/commands/'

    name_of_file = name

    completeName = os.path.join(save_path, name_of_file + ".py")

    # file1 = open(completeName, "w")

    with open(completeName, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        # print(destination)

    # file1.close()


class UploadView(FormView):
    form_class = UploadFileForm
    template_name = 'upload.html'
    success_url = '/thanks/'
    # success_url = '/thanks/'
    # def post(self, request, *args, **kwargs):
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # add_action(request.FILES['file'])
    #         return HttpResponseRedirect('/success/url/')

    def form_valid(self, form):
        # add_action(request.FILES['file'])
        print('valid')
        # return HttpResponseRedirect('/success/url/')
        return super().form_valid(form)
