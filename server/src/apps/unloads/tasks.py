from bulk_update.helper import bulk_update
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q, F

from src.api.requests.fortochki_requests import (
    refresh_wsdl_file,
    find_rim_list,
    convert_code_list,
    get_rim_goods_info,
    find_tire_list,
    get_tire_goods_info,
)
from src.api.requests.starco_requests import (
    get_starco_rims,
    get_starco_stock,
    get_starco_prices,
    get_starco_tyres,
)
from src.apps.products.models import Product
from src.apps.unloads.models import UnloadScheduler
from src.apps.unloads.utils import (
    update_fortochki_price_info,
    create_fortochki_rim,
    update_fortochki_rim_info,
    create_fortochki_tire,
    update_fortochki_tire_info,
    starco_create_rim,
    starco_create_tire,
)
from src.other.enums import ProductType, UnloadServiceType
from src.utils.slug_utils import slugify

logger = get_task_logger(__name__)


# 4TOCHKI TASKS
# BEAT
@shared_task(name="unload_fortochki_beat")
def unload_fortochki_beat() -> None:
    refresh_wsdl_file()
    logger.info("Unloading fortochki data...")
    scheduler = UnloadScheduler.objects.filter(
        service=UnloadServiceType.fortochki
    ).first()
    if scheduler.rim_unload:
        fortochki_unload_rims_task.delay()
    if scheduler.tire_unload:
        fortochki_unload_tires_task.delay()
    return None


@shared_task(name="fortochki_unload_rims_task")
def fortochki_unload_rims_task() -> None:
    code_list = []
    rim_list = find_rim_list()
    logger.info(f"founded disk list: {len(rim_list)}")
    # create or update rim
    for rim_data in rim_list:
        slug = slugify(rim_data.name)
        filter_query = Q(type=ProductType.RIMS) & (
            Q(ext_data__code=rim_data.code) | Q(slug=slug)
        )
        founded_rim = Product.objects.filter(filter_query).first()
        if founded_rim is not None:
            update_fortochki_price_info(data=rim_data, product=founded_rim)
        else:
            try:
                code = create_fortochki_rim(data=rim_data)
                code_list.append(code)
            except Exception as ex:
                logger.info(ex)
    step = 200
    chunked_list = [code_list[i : i + step] for i in range(0, len(code_list), step)]
    logger.info(f"chunked list size {len(chunked_list)}")
    any([fortochki_get_rim_info_task.delay(i) for i in chunked_list])
    return None


@shared_task(name="fortochki_get_rim_info_task")
def fortochki_get_rim_info_task(code_list: list) -> None:
    logger.info(f"start get rim goods info...")
    converted_code_list = convert_code_list(code_list=code_list)
    info_list = get_rim_goods_info(code_list=converted_code_list)
    for info in info_list:
        update_fortochki_rim_info(data=info)
    return None


@shared_task(name="fortochki_unload_tires_task")
def fortochki_unload_tires_task() -> None:
    code_list = []
    tire_list = find_tire_list()
    logger.info(f"founded tire list: {len(tire_list)}")
    # create or update tire
    for tire_data in tire_list:
        filter_query = Q(type=ProductType.TIRES) & Q(ext_data__code=tire_data.code)
        founded_tire = Product.objects.filter(filter_query).first()
        if founded_tire is not None:
            update_fortochki_price_info(data=tire_data, product=founded_tire)
        else:
            try:
                code = create_fortochki_tire(data=tire_data)
                code_list.append(code)
            except Exception as ex:
                logger.info(ex)
    step = 200
    chunked_list = [code_list[i : i + step] for i in range(0, len(code_list), step)]
    logger.info(f"chunked list size {len(chunked_list)}")
    any([fortochki_get_tire_info_task.delay(i) for i in chunked_list])
    return None


@shared_task(name="fortochki_get_tire_info_task")
def fortochki_get_tire_info_task(code_list: list) -> None:
    logger.info(f"start get tire goods info...")
    converted_code_list = convert_code_list(code_list=code_list)
    info_list = get_tire_goods_info(code_list=converted_code_list)
    logger.info(info_list)
    for info in info_list:
        update_fortochki_tire_info(data=info)
    return None


# STARCO TASKS
# BEAT
@shared_task(name="unload_starco_beat")
def unload_starco_beat() -> None:
    logger.info("Unloading starco data...")
    scheduler = UnloadScheduler.objects.filter(service=UnloadServiceType.starco).first()
    if scheduler.rim_unload:
        starco_get_rim_task()
    if scheduler.tire_unload:
        starco_get_tire_task()
    starco_get_stock_task.delay()
    return None


# @shared_task(name="starco_get_tire_task")
def starco_get_tire_task() -> None:
    tire_list = get_starco_tyres()
    for tire_data in tire_list:
        slug = slugify(tire_data.full_name)
        filter_query = Q(type=ProductType.TIRES) & (
            Q(ext_data__product_no=tire_data.product_no) | Q(slug=slug)
        )
        if Product.objects.filter(filter_query).exists():
            continue
        else:
            starco_create_tire(data=tire_data)


# @shared_task(name="starco_get_rim_task")
def starco_get_rim_task() -> None:
    rim_list = get_starco_rims()
    for rim_data in rim_list:
        slug = slugify(rim_data.full_name)
        filter_query = Q(type=ProductType.RIMS) & (
            Q(ext_data__product_no=rim_data.product_no) | Q(slug=slug)
        )
        if Product.objects.filter(filter_query).exists():
            continue
        else:
            starco_create_rim(data=rim_data)
    starco_get_stock_task.delay()
    return None


# BEAT
@shared_task(name="starco_get_stock_beat")
def starco_get_stock_task() -> None:
    stock_list = get_starco_stock()
    for stock_data in stock_list:
        founded_product = Product.objects.filter(
            ext_data__product_no=stock_data.product_no
        ).first()
        if founded_product:
            current_rest_count = (
                stock_data.BEL_STOCK
                + stock_data.CEL_STOCK
                + stock_data.EKT_STOCK
                + stock_data.KAZ_STOCK
                + stock_data.MOS_STOCK
                + stock_data.UKR_STOCK
            )
            founded_product.rest = current_rest_count
            founded_product.save()
    starco_get_price_list_task.delay()
    return None


@shared_task(name="starco_get_price_list_task")
def starco_get_price_list_task() -> None:
    updated_products: list[Product] = []
    step = 200
    price_list = get_starco_prices()
    chunked_price_list = [
        price_list[i : i + step] for i in range(0, len(price_list), step)
    ]
    products = Product.objects.annotate(product_no=F("ext_data__product_no"))
    for chunk_prices in chunked_price_list:
        for price in chunk_prices:
            founded_product = (
                products.filter(product_no=price.product_no).only("price").first()
            )
            if founded_product:
                founded_product.price = price.price
                updated_products.append(founded_product)
        bulk_update(updated_products, update_fields=["price"])
        updated_products.clear()
    # for price in price_list:
    #     founded_product = Product.objects.filter(
    #         ext_data__product_no=price.product_no
    #     ).first()
    #     if founded_product:
    #         founded_product.price = price.price
    #         founded_product.save()
    return None
