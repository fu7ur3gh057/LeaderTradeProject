
from django.urls import path, include
from src.apps.web import views as v

urlpatterns = [
    path('', v.home),
    path('catalog/<slug:slug>', v.catalog),
    path('search', v.search),
    path('about', v.about),
    path('news', v.news),
    path('news/<slug:slug>', v.news_item),
    path('promo', v.promo),
    path('calculator', v.calculator),
    path('portfolio', v.portfolio),
    path('portfolio/<slug:slug>', v.portfolio_item),
    path('policy', v.policy),
    path('reviews', v.reviews),
    path('rassrochka', v.credit),
    path('froala_editor/',include('froala_editor.urls')),
    path('js/spark/promo/<int:id>', v.promo_spark),
    path('js/spark/review/<int:id>', v.review_spark),
]
