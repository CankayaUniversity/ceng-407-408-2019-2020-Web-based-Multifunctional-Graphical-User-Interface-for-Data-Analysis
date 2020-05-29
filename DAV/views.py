from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage

from .forms import FileForm
from .models import File
# Create your views here.

def index(request):

    return render(request, 'DAV/index.html')

def analysisView(request):
    files = File.objects.all()
    return render(request, 'DAV/Analysis.html', {
        'files' : files
    })



def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('analysis')
    else:
        form = FileForm()
    return render(request, 'DAV/upload.html', {
        'form': form
    })
