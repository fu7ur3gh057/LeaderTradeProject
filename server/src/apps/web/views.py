from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from products.models import Product, ProductType


PAGE_SIZE = 20


def home(r):
    return render(r, "index.html", locals())


def catalog(r, slug):
    products = Product.objects.filter(type=ProductType[slug.upper()])
    pages = Paginator(products, PAGE_SIZE)
    page = pages.get_page(int(r.GET.get("page", 1)))
    return render(r, "catalog.html", locals())


def search(r):
    return render(r, "search.html", locals())


def promo(r):
    return render(r, "promo.html", locals())


def about(r):
    return render(r, "about.html", locals())


def news(r):
    from news.models import Post

    posts = Post.objects.filter(live=True).order_by("-date")
    pages = Paginator(posts, PAGE_SIZE)
    page = pages.get_page(int(r.GET.get("page", 1)))
    return render(r, "news.html", locals())


def news_item(r, slug):
    from news.models import Post

    post = Post.objects.get(slug=slug, live=True)
    post_products = [pp.product for pp in post.products.all()]
    other_posts = (
        Post.objects.exclude(slug=slug).filter(live=True).order_by("-date")[:4]
    )
    return render(r, "news-item.html", locals())


def promo(r):
    from promo.models import Promo

    items = Promo.objects.order_by("-start")[:15]
    return render(r, "promo.html", locals())


def promo_spark(r, id):
    from promo.models import Promo

    promo = Promo.objects.get(id=id)
    return render(r, "spark/promo_modal.html", locals())


def review_spark(r, id):
    from promo.models import Review

    review = Review.objects.get(id=id)
    return render(r, "spark/review_modal.html", locals())


def credit(r):
    return render(r, "credit.html", locals())


def calculator(r):
    return render(r, "calc.html", locals())


def portfolio(r):
    from promo.models import Portfolio

    items = Portfolio.objects.all()
    pages = Paginator(items, PAGE_SIZE)
    page = pages.get_page(int(r.GET.get("page", 1)))
    return render(r, "portfolio.html", locals())


def portfolio_item(r, slug):
    from promo.models import Portfolio

    item = get_object_or_404(Portfolio, slug=slug)
    products = [pp.product for pp in item.products.all()]
    other_items = Portfolio.objects.exclude(slug=slug)[:6]
    return render(r, "portfolio-item.html", locals())


def policy(r):
    return render(r, "politics.html", locals())


def reviews(r):
    from promo.models import Review

    items = Review.objects.exclude(published_at=None).order_by("-published_at")
    pages = Paginator(items, PAGE_SIZE)
    page = pages.get_page(int(r.GET.get("page", 1)))
    return render(r, "reviews.html", locals())
