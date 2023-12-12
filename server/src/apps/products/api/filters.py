import django_filters


class ProductFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="type", lookup_expr="iexact")
    min_price = django_filters.NumberFilter(
        field_name="current_price", lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(
        field_name="current_price", lookup_expr="lte"
    )
    color = django_filters.CharFilter(field_name="color", lookup_expr="iexact")
    category = django_filters.NumberFilter(field_name="category", lookup_expr="exact")
