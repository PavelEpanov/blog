from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewsForm

from .models import News, Category # Импортируем модель news из текущей директории


def index(request):
    #print(dir(request))
    news = News.objects.all()
    #categories = Category.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
        #'categories': categories,
    }
    return render(request, 'news/index.html', context)


def get_category(request, category_id: int):
    news = News.objects.filter(category_id=category_id)
    #categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, 'category.html', {'news':news, 'category':category})
    #'categories':categories,


def view_news(request, news_id: int):
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item':news_item})


def add_news(request, ):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            News.objects.create(**form.cleaned_data)
            redirect('home')

    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
