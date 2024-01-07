from pydantic import BaseModel


class StarcoTyreSchema(BaseModel):
    AGSI1: str | None = None
    Alternative_size: str | None = None
    boh_product_no: str | None = None
    Brand: str | None = None
    brand: str | None = None
    Comment: str | None = None
    Comment_link: str | None = None
    ean: str | None = None
    ean_full: str | None = None
    enabled: str | None = None
    full_name: str | None = None
    Image: str | None = None
    Inch: str | None = None
    item_category_id: int | None = None
    item_group: str | None = None
    LI_1: str | None = None
    LI_2: str | None = None
    LI_3: str | None = None
    LI__SI: str | None = None
    Loadindex_kg_at_km_h_1_: str | None = None
    Loadindex_kg_at_km_h_2_: str | None = None
    Loadindex_twin_Tyre_truck: str | None = None
    Lug_height_mm: str | None = None
    name: str | None = None
    net_weight: float | None = None
    Noise_emission_dB: str | None = None
    Noise_emission_Level: str | None = None
    Number_of_Lugs: str | None = None
    Outer_diameter__mm: str | None = None
    Permissible_rim: str | None = None
    PR: str | None = None
    Pressure_bar: str | None = None
    product_no: str | None = None
    Produkt: str | None = None
    Profil: str | None = None
    Radial_Diagonal: str | None = None
    Recommended_rim: str | None = None
    Registration: str | None = None
    Rib_width: str | None = None
    Rolling_resistance: str | None = None
    Rollsize_mm: str | None = None
    Sector: str | None = None
    segment_description: str | None = None
    Size: str | None = None
    SI_1: str | None = None
    SI_2: str | None = None
    Specification: str | None = None
    Static_radius_mm: str | None = None
    sub_segment_description: str | None = None
    TL__TT: str | None = None
    Tyre_ballast_volume_75_Liter: str | None = None
    volume_CuFt: float | None = None
    volume_CuM: float | None = None
    Wet_Grip: str | None = None
    With_mm: str | None = None
    slug: str | None = None
    ___: str | None = None


class StarcoRimSchema(BaseModel):
    AGSI1: str | None = None
    Bearing_type: str | None = None
    boh_product_no: str | None = None
    Bolt_Hole: str | None = None
    Bolt_hole_circle: str | None = None
    Bolt_hole_number: str | None = None
    Brand: str | None = None
    brand: str | None = None
    Center_bore_diameter: str | None = None
    Colour: str | None = None
    Comment: str | None = None
    Comment_link: str | None = None
    Design: str | None = None
    ean: str | None = None
    ean_full: str | None = None
    enabled: str | None = None
    ET: str | None = None
    full_name: str | None = None
    Hub_length: str | None = None
    Hub_type: str | None = None
    Hump: str | None = None
    Image: str | None = None
    Inch: str | None = None
    Install_length: str | None = None
    item_category_id: int | None = None
    item_group: str | None = None
    Load_Capacity_1: str | None = None
    Load_capacity_2: str | None = None
    manufacturer_item_id: str | None = None
    Material: str | None = None
    name: str | None = None
    net_weight: float | None = None
    Offset_hub: str | None = None
    Offset_hub_length: str | None = None
    product_no: str | None = None
    slug: str | None = None
    Produkt: str | None = None
    RAL: str | None = None
    Recom_Tyre_Size: str | None = None
    Rim_centering: str | None = None
    Rim_width: str | None = None


class StarcoStockSchema(BaseModel):
    BEL_STOCK: int = 0
    CEL_STOCK: int = 0
    EKT_STOCK: int = 0
    KAZ_STOCK: int = 0
    MOS_STOCK: int = 0
    RIG_STOCK: int = 0
    RST_STOCK: int = 0
    SPB_STOCK: int = 0
    UKR_STOCK: int = 0
    ean: str | None = ""
    product_no: str | None = ""


class StarcoPriceSchema(BaseModel):
    currency_id: str | None = None
    max_recomended_price: float | None = None
    price: float | None = None
    product_no: str | None = None
    timestamp: str | None = None
