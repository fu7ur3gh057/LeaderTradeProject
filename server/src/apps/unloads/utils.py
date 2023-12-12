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
from src.apps.products.models import Category, Product
from src.other.enums import ProductType
from src.utils.number_utils import float_or_none, int_or_none


def create_fortochki_rim(data: DiskPriceRestSchema) -> str | None:
    images = [data.img_big_my, data.img_big_pish, data.img_small]
    price_params = data.whpr.wh_price_rest[0]
    rest_count = sum([i.rest for i in data.whpr.wh_price_rest])
    category = Category.objects.filter(title="Диски").first()
    rim = Product.objects.create(
        title=data.name,
        category=category,
        color=data.color,
        model=data.model,
        price=price_params.price_rozn,
        rest=rest_count,
        type=ProductType.RIMS,
    )
    rim.ext_data = data.model_dump()
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
    product.save()


def update_fortochki_rim_info(data: RimContainerSchema) -> None:
    filter_query = Q(type=ProductType.RIMS) & Q(ext_data__code=data.code)
    rim = Product.objects.filter(filter_query).first()
    if rim is None:
        return None
    brand = Brand.objects.filter(title__exact=data.brand).first()
    if brand is None:
        brand = Brand.objects.create(title=data.brand)
    rim.dia = data.dia
    rim.et = data.et
    rim.pcd = data.bolts_spacing
    rim.unite_pcd = data.bolts_count
    rim.bolts = data.bolts_spacing
    rim.bolts_2 = data.bolts_spacing2
    rim.width = data.width
    brand = brand
    rim.save()


def create_fortochki_tire(data: TyrePriceRestSchema) -> str | None:
    images = [data.img_big_my, data.img_big_pish, data.img_small]
    price_params = data.whpr.wh_price_rest[0]
    rest_count = sum([i.rest for i in data.whpr.wh_price_rest])
    # external_data = {"code": data.code, "images": images, "price": price_params.price}
    category = Category.objects.filter(title="Шины").first()
    tire = Product.objects.create(
        title=data.name,
        category=category,
        model=data.model,
        price=price_params.price_rozn,
        rest=rest_count,
        type=ProductType.TIRES,
    )
    tire.ext_data = data.model_dump()
    tire.save()
    return data.code


def update_fortochki_tire_info(data: TyreContainerSchema) -> None:
    filter_query = Q(type=ProductType.TIRES) & Q(ext_data__code=data.code)
    tire = Product.objects.filter(filter_query).first()
    if tire is None:
        return None
    brand = Brand.objects.filter(title__exact=data.brand).first()
    if brand is None:
        brand = Brand.objects.create(title=data.brand)
    tire.width = data.width
    tire.width2 = data.subwidth
    tire.season = data.season
    tire.height = data.height
    tire.load_index = data.load_index
    tire.speed_index = data.speed_index
    tire.brand = brand
    tire.save()


def get_index_values(data: StarcoRimSchema):
    pass


def _get_rim_model_name_or_none(data: StarcoRimSchema) -> str:
    if data.Brand == "" or data.Brand is None:
        return ""
    split_list = data.full_name.split(data.Brand)
    if len(split_list) < 2:
        return ""
    else:
        return split_list[1].strip()


def starco_create_rim(data: StarcoRimSchema):
    try:
        model = _get_rim_model_name_or_none(data)
        category = Category.objects.filter(title="Диски").first()
        brand = Brand.objects.filter(title__exact=data.Brand).first()
        if brand is None:
            brand = Brand.objects.create(title=data.Brand)
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
        )
    except Exception as ex:
        print(ex)


def starco_create_tire(data: StarcoTyreSchema):
    category = Category.objects.filter(title="Шины").first()
    brand = Brand.objects.filter(title__exact=data.Brand).first()
    if brand is None:
        brand = Brand.objects.create(title=data.Brand)
    Product.objects.create(
        type=ProductType.TIRES,
        model=data.Profil,
    )
