from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q

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
)
from src.other.enums import ProductType, UnloadServiceType

logger = get_task_logger(__name__)


@shared_task(name="refresh_resources_beat")
def refresh_resources_beat() -> None:
    # Update 4tochki WSDL file
    refresh_wsdl_file()


# 4TOCHKI TASKS
# BEAT
@shared_task(name="unload_fortochki_beat")
def unload_fortochki_beat() -> None:
    logger.info("Unloading fortochki data...")
    scheduler = UnloadScheduler.objects.filter(
        status=UnloadServiceType.fortochki
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
        filter_query = Q(type=ProductType.RIMS) & Q(external_id=rim_data.code)
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
    chunked_list = [rim_list[i : i + step] for i in range(0, len(rim_list), step)]
    logger.info(f"chunked list size {len(chunked_list)}")
    any([fortochki_get_rim_info_task.delay(i) for i in chunked_list])
    return None


@shared_task(name="fortochki_get_rim_info_task")
def fortochki_get_rim_info_task(code_list: list) -> None:
    logger.info(f"start get rim goods info...")
    converted_code_list = convert_code_list(code_list=code_list)
    info_list = get_rim_goods_info(code_list=converted_code_list)
    logger.info(info_list)
    for info in info_list:
        logger.info(info)
        update_fortochki_rim_info(data=info)
    return None


@shared_task(name="fortochki_unload_tires_task")
def fortochki_unload_tires_task() -> None:
    code_list = []
    tire_list = find_tire_list()
    logger.info(f"founded tire list: {len(tire_list)}")
    # create or update tire
    for tire_data in tire_list:
        filter_query = Q(type=ProductType.TIRES) & Q(external_id=tire_data.code)
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
    chunked_list = [tire_list[i : i + step] for i in range(0, len(tire_list), step)]
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
        logger.info(info)
        update_fortochki_tire_info(data=info)
    return None


# STARCO TASKS
# BEAT
@shared_task(name="unload_starco_beat")
def unload_starco_beat() -> None:
    logger.info("Unloading starco data...")
    scheduler = UnloadScheduler.objects.filter(status=UnloadServiceType.starco).first()
    if scheduler.rim_unload:
        starco_get_rim_task.delay()
    if scheduler.tire_unload:
        starco_get_tire_task.delay()
    return None


@shared_task(name="starco_get_tire_task")
def starco_get_tire_task() -> None:
    pass


@shared_task(name="starco_get_rim_task")
def starco_get_rim_task() -> None:
    rim_list = get_starco_rims()
    for rim_data in rim_list:
        filter_query = Q(type=ProductType.RIMS) & Q(external_id=rim_data.product_no)
        if Product.objects.filter(filter_query).exists():
            continue
        else:
            starco_create_rim(data=rim_data)
    return None


# BEAT
@shared_task(name="starco_get_stock_beat")
def starco_get_stock_beat() -> None:
    stock_list = get_starco_stock()
    for stock_data in stock_list:
        founded_product = Product.objects.filter(
            external_id=stock_data.product_no
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
    price_list = get_starco_prices()
    for price in price_list:
        founded_product = Product.objects.filter(external_id=price.product_no).first()
        if founded_product:
            founded_product.price = price.price
            founded_product.save()
    return None