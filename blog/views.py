from django.shortcuts import render, HttpResponse
from pelican.contents import Article as _Article
import core


# Create your views here.
def article(request, permalink):
    for article in core.pelican.articles:
        if permalink == int(article.metadata['permalink']):
            return render(request, 'blog/article.html', {
                'article': article
            })
