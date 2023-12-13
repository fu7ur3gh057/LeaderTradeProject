import django_filters


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="iexact")
