from django.shortcuts import render, redirect, reverse
import core
import settings


# Create your views here.

def index(request):
    core.pelican.read(True)
    articles = core.pelican.articles
    headers = [item[0] for item in settings.get_fields(articles[0])]
    articles.sort(key=lambda article: -int(article.metadata['permalink']))
    articles = [settings.get_fields(article) for article in articles]
    articles = [[value for key, value in article] for article in articles]
    return render(request, 'console/index.html', {
        'headers': headers,
        'articles': articles,
    })
