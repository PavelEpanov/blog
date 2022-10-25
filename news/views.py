from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewsForm
from .models import News, Category # Импортируем модель news из текущей директории
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.core.paginator import Paginator


def test(request):
    objects = ['1John', '1Paul', '1Alex', '1Sofa', '2John', '2Paul', '2Alex', '1John', '1Paul', '1Alex', '1John', '1Paul', '1Alex']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(MyMixin, ListView):
    model = News # news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    mixin_prop = 'hello world'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #success_url = reverse_lazy('home')

# def index(request):
#     #print(dir(request))
#     news = News.objects.all()
#     #categories = Category.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         #'categories': categories,
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id: int):
#     news = News.objects.filter(category_id=category_id)
#     #categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'category.html', {'news':news, 'category':category})
#     #'categories':categories,


# def view_news(request, news_id: int):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item':news_item})


# def add_news(request, ):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             #news = News.objects.create(**form.cleaned_data) # Возвращает объект
#             news = form.save()
#             return redirect(news)
#
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
