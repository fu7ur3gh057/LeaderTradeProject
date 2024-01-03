from django.shortcuts import render
from django.core.paginator import Paginator
from products.models import Product, ProductType


PAGE_SIZE = 20

def home(r):
	return render(r, 'index.html', locals())

def catalog(r, slug):

	products = Product.objects.filter(type=ProductType[slug.upper()])
	pages = Paginator(products, PAGE_SIZE)
	page = pages.get_page(int(r.GET.get('page', 1)))
	return render(r, 'catalog.html', locals())


def search(r):
	return render(r, 'search.html', locals())

def promo(r):
	return render(r, "promo.html", locals())

def about(r):
	return render(r, "about.html", locals())


def news(r):
	from news.models import Post
	posts = Post.objects.filter(live=True).order_by("-date")
	pages = Paginator(posts, PAGE_SIZE)
	page = pages.get_page(int(r.GET.get('page', 1)))
	return render(r, "news.html", locals())


def news_item(r, slug):
	from news.models import Post
	post = Post.objects.get(slug=slug, live=True)
	post_products = [pp.product for pp in post.products.all()]
	other_posts = Post.objects.exclude(slug=slug).filter(live=True).order_by("-date")[:4]
	return render(r, "news-item.html", locals())

def promo(r):
	from promo.models import Promo
	items = Promo.objects.order_by("-start")[:15]
	return render(r, "promo.html", locals())

def promo_spark(r, id):
	from promo.models import Promo
	promo = Promo.objects.get(id=id)
	return render(r, "spark/promo_modal.html", locals())


def credit(r):
	return render(r, "credit.html", locals())