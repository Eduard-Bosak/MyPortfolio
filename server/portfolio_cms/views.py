from django.shortcuts import render
from django.http import HttpResponse
from wagtail.models import Page
from content.models import UiText
from portfolio_cms.models import PortfolioPage, UISettings

# Отображение главной страницы
def home_view(request):
    portfolio = PortfolioPage.objects.live().first()
    if portfolio:
        return portfolio.serve(request)
    # Резервный контент из обычных моделей
    from content.views import home_view as content_home_view
    return content_home_view(request)
