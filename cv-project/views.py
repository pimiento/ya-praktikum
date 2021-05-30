import datetime as dt
from django.shortcuts import render
from .forms import UploadForm
from .utils import utils

def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_content = form.cleaned_data['_file']
            path = form.cleaned_data['_path']
            token = form.cleaned_data['_token']
            name = form.cleaned_data['_name']
            response = utils.send_file(path, file_content, name, token)
            if response.ok:
                utils.reload_app(name, token)
            result = response.reason

        else:
            result = form.errors

    else:
        form = UploadForm()
        result = None

    context = {
        'upload_form': form,
        'result': result
    }
    return render(request, 'cv/index.html', context)
