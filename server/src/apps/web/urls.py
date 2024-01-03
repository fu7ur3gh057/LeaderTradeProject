
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
    path('rassrochka', v.credit),
    path('js/spark/promo/<int:id>', v.promo_spark),
]
