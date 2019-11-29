from django.shortcuts import render, HttpResponse, redirect
from pelican.contents import Article as _Article
import core


# Create your views here.
def article(request, permalink_id):
    for article in core.pelican.articles:
        if permalink_id == int(article.metadata['permalink']):
            return render(request, 'blog/article.html', {
                'article': article
            })
    return redirect('console:index')
