from django.shortcuts import render, redirect
from .forms import CategoryForm

def add_category(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'category/add.html', {'form': form})