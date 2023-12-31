from typing import Any

from pydantic import BaseModel
from zeep import helpers


# 4tochki schemas
# Rims
class RimContainerSchema(BaseModel):
    avto: str | None = None
    base_color: str | None = None
    bolts_spacing: float | None = None
    bolts_spacing2: float | None = None
    bolts_count: int | None = None
    brand: str | None = None
    code: str | None = None
    color: str | None = None
    dia: float | None = None
    diameter: float | None = None
    et: float | None = None
    img_big_my: str | None = None
    img_big_pish: str | None = None
    img_small: str | None = None
    inset_type: str | None = None
    logo: str | None = None
    marka_html: str | None = None
    marka_logo: str | None = None
    model: str | None = None
    model_html: str | None = None
    mount: str | None = None
    mount_note: str | None = None
    name: str | None = None
    producer: str | None = None
    rim_vid_name: str | None = None
    type: int | None = None
    use_ck: int | None = None
    width: float | None = None

    @staticmethod
    def to_pydantic(data: Any) -> Any:
        response_dict = helpers.serialize_object(data)
        return RimContainerSchema(**response_dict)


class WhprSchema(BaseModel):
    price: float | None = None
    price_rozn: float | None = None
    rest: int | None = None
    wrh: int | None = None

    @staticmethod
    def to_pydantic(data: Any) -> Any:
        response_dict = helpers.serialize_object(data)
        return WhprSchema(**response_dict)


class ArrayOfPriceSchema(BaseModel):
    wh_price_rest: list[WhprSchema] | None = None

    @staticmethod
    def to_pydantic(data: Any) -> Any:
        response_dict = helpers.serialize_object(data)
        return ArrayOfPriceSchema(**response_dict)


class DiskPriceRestSchema(BaseModel):
    code: str | None = None
    slug: str | None = None
    color: str | None = None
    img_big_my: str | None = None
    img_big_pish: str | None = None
    img_small: str | None = None
    marka: str | None = None
    model: str | None = None
    name: str | None = None
    rim_vid_name: str | None = None
    saleId: str | None = None
    type: int | None = None
    whpr: ArrayOfPriceSchema | None = None

    @staticmethod
    def to_pydantic(data: Any) -> Any:
        response_dict = helpers.serialize_object(data)
        return DiskPriceRestSchema(**response_dict)


# Tires
class TyreContainerSchema(BaseModel):
    code: str | None = None
    name: str | None = None
    type: str | None = None
    brand: str | None = None
    model: str | None = None
    season: str | None = None
    width: float | None = 0
    subwidth: float | None = 0
    height: float | None = 0
    subheight: str | None = None
    constr: str | None = None
    diameter: float | None = None
    diameter_out: float | None = None
    load_index: str | None = None
    speed_index: str | None = None
    thorn: bool | None = None
    thorn_type: str | None = None
    puncture: str | None = None
    usa: str | None = None
    protection: str | None = None
    side: str | None = None
    tech: str | None = None
    omolog: str | None = None
    softness: str | None = None
    axle: str | None = None
    sloy: str | None = None
    marker_color: str | None = None
    strengthening: bool | None = None
    wear_index: str | None = None
    tonnage: str | None = None
    noise: str | None = None
    passability: str | None = None
    comfort: str | None = None
    aquaplaning: str | None = None
    moto_use: str | None = None
    protector_type: str | None = None
    use_type: str | None = None
    marka_logo: str | None = None
    img_small: str | None = None
    img_big_pish: str | None = None
    img_big_my: str | None = None

    @staticmethod
    def to_pydantic(data: Any) -> Any:
        response_dict = helpers.serialize_object(data)
        return TyreContainerSchema(**response_dict)


class TyrePriceRestSchema(BaseModel):
    code: str | None = None
    img_big_my: str | None = None
    img_big_pish: str | None = None
    img_small: str | None = None
    marka: str | None = None
    model: str | None = None
    name: str | None = None
    quality: int | None = None
    season: str | None = None
    thorn: bool | None = None
    type: str | None = None
    whpr: ArrayOfPriceSchema | None = None

    @staticmethod
    def to_pydantic(data: Any) -> Any:
        response_dict = helpers.serialize_object(data)
        return TyrePriceRestSchema(**response_dict)
