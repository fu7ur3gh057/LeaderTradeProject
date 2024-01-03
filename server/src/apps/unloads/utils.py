from bulk_update.helper import bulk_update
from django.db.models import Q
from zeep import Client

from src.api.schemas.fortochki_schemas import (
    DiskPriceRestSchema,
    TyrePriceRestSchema,
    RimContainerSchema,
    TyreContainerSchema,
)
from src.api.schemas.starco_schemas import StarcoRimSchema, StarcoTyreSchema
from src.apps.catalog.models import Brand
from products.models import Category, Product
from src.other.enums import ProductType, UnloadServiceType
from src.utils.number_utils import float_or_none, int_or_none


def get_or_create_brand(title: str) -> Brand:
    brand = Brand.objects.filter(title__iexact=title).first()
    if brand is None:
        brand = Brand.objects.create(title=title)
    return brand


def prepare_fortochki_rim(data: DiskPriceRestSchema, category) -> str | None:
    images = [data.img_big_my, data.img_big_pish, data.img_small]
    price_params = data.whpr.wh_price_rest[0]
    rest_count = sum([i.rest for i in data.whpr.wh_price_rest])
    rim = Product(
        title=data.name,
        category=category,
        color=data.color,
        model=data.model,
        price=price_params.price_rozn,
        rest=rest_count,
        type=ProductType.RIMS,
        ext_data=data.model_dump(),
        image=images[0] if images else None,
        unload_service=UnloadServiceType.fortochki,
    )
    return rim


def create_fortochki_rim(data: DiskPriceRestSchema) -> str | None:
    images = [data.img_big_my, data.img_big_pish, data.img_small]
    price_params = data.whpr.wh_price_rest[0]
    rest_count = sum([i.rest for i in data.whpr.wh_price_rest])
    category = Category.objects.filter(title=ProductType.RIMS).first()
    rim = Product.objects.create(
        title=data.name,
        category=category,
        color=data.color,
        model=data.model,
        price=price_params.price_rozn,
        rest=rest_count,
        type=ProductType.RIMS,
        ext_data=data.model_dump(),
        unload_service=UnloadServiceType.fortochki,
    )
    rim.save()
    return data.code


def update_fortochki_price_info(
    data: DiskPriceRestSchema | TyrePriceRestSchema, product: Product
) -> None:
    price_params = data.whpr.wh_price_rest[0]
    rest_count = sum([i.rest for i in data.whpr.wh_price_rest])
    product.rest = rest_count
    product.price = price_params.price_rozn
    product.ext_data["price"] = price_params.price
    return product


def update_fortochki_rim_info(data: RimContainerSchema, rim: Product) -> None:
    rim.dia = data.dia
    rim.et = data.et
    rim.pcd = data.bolts_spacing
    rim.unite_pcd = data.bolts_count
    rim.bolts = data.bolts_spacing
    rim.bolts2 = data.bolts_spacing2
    rim.width = data.width
    return rim


def create_fortochki_tire(data: TyrePriceRestSchema) -> str | None:
    images = [data.img_big_my, data.img_big_pish, data.img_small]
    price_params = data.whpr.wh_price_rest[0]
    rest_count = sum([i.rest for i in data.whpr.wh_price_rest])
    # external_data = {"code": data.code, "images": images, "price": price_params.price}
    category = Category.objects.filter(title=ProductType.TIRES).first()
    tire = Product.objects.create(
        title=data.name,
        category=category,
        model=data.model,
        price=price_params.price_rozn,
        rest=rest_count,
        type=ProductType.TIRES,
        unload_service=UnloadServiceType.fortochki,
    )
    tire.ext_data = data.model_dump()
    tire.save()
    return data.code


def update_fortochki_tire_info(data: TyreContainerSchema) -> None:
    filter_query = Q(type=ProductType.TIRES) & Q(ext_data__code=data.code)
    tire = Product.objects.filter(filter_query).first()
    if tire is None:
        return None
    brand = get_or_create_brand(title=data.brand)
    tire.width = data.width
    tire.width2 = data.subwidth
    tire.season = data.season
    tire.height = data.height
    tire.load_index = data.load_index
    tire.speed_index = data.speed_index
    tire.brand = brand
    tire.save()


# STARCO
def _get_model_name_or_none(data) -> str:
    if data.Brand == "" or data.Brand is None:
        return ""
    # splitting by Brand
    if data.Brand in data.full_name:
        split_list = data.full_name.split(data.Brand)
    else:
        split_list = data.full_name.lower().split(data.Brand.lower())
    if len(split_list) < 2:
        return ""
    else:
        return split_list[1].strip()


def starco_create_rim(data: StarcoRimSchema) -> None:
    try:
        model = _get_model_name_or_none(data=data)
        category = Category.objects.filter(title=ProductType.RIMS).first()
        brand = get_or_create_brand(title=data.Brand)
        Product.objects.create(
            category=category,
            type=ProductType.RIMS,
            title=data.full_name,
            model=model,
            bolts=int_or_none(data.Bolt_hole_number),
            pcd=float_or_none(data.Bolt_hole_circle),
            dia=float_or_none(data.Center_bore_diameter),
            color=data.Colour,
            width=float_or_none(data.Rim_width),
            et=int_or_none(data.ET),
            size=float_or_none(data.Inch),
            brand=brand,
            ext_data=data.model_dump(),
            unload_service=UnloadServiceType.starco,
        )
    except Exception as ex:
        print(ex)


def get_width_height_size(data: StarcoTyreSchema) -> tuple:
    try:
        size = data.Size
        if "/" in size and "R" in size:
            split_list = size.split("R")
            wh = split_list[0].split("/")
            return float_or_none(wh[0]), int_or_none(wh[1]), int_or_none(split_list[1])
        elif "/" in size and "-" in size:
            split_list = size.split("-")
            wh = split_list[0].split("/")
            return float_or_none(wh[0]), int_or_none(wh[1]), int_or_none(split_list[1])
        elif "-" in size:
            split_list = size.split("-")
            return float_or_none(split_list[0]), None, int_or_none(split_list[1])
        # elif '.' in size and 'R' in size:
        #     pass
        elif "R" in size:
            split_list = size.split("R")
            return float_or_none(split_list[0]), None, int_or_none(split_list[1])
        else:
            return None, None, None
    except Exception as ex:
        print(ex)
        return None, None, None


def starco_create_tire(data: StarcoTyreSchema) -> None:
    try:
        model = _get_model_name_or_none(data=data)
        category = Category.objects.filter(title=ProductType.TIRES).first()
        width, height, size = get_width_height_size(data=data)
        brand = get_or_create_brand(title=data.Brand)
        Product.objects.create(
            category=category,
            type=ProductType.TIRES,
            title=data.full_name,
            model=model,
            speed_index=data.SI_1,
            load_index=data.LI_1,
            width=width,
            height=height,
            size=size,
            brand=brand,
            ext_data=data.model_dump(),
            unload_service=UnloadServiceType.starco,
        )
    except Exception as ex:
        print(ex)


def update_price():
    pass


def chunks(lst, n:int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]