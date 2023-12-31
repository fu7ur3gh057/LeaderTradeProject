from django.utils.translation import gettext_lazy as _
from django_enum_choices.serializers import EnumChoiceField
from rest_framework import serializers

from src.apps.news.models import Post
from products.models import Product
from src.utils.news_utils import video_thumbnail, get_embed_video_link, get_youtube_id


class WagtailImageSerializer(serializers.Serializer):
    def resolve_url(self, obj):
        return obj.file.url

    class Meta:
        fields = ["id", "title", "filename", "file_size", "url"]


class PostSerializer(serializers.ModelSerializer):
    def resolve_body(self, obj: Post):
        res = []
        for b in obj.body:
            if b.block_type == "gallery":
                gal = []
                for img in b.value:
                    gal.append(WagtailImageSerializer(img))
                res.append({"type": b.block_type, "value": gal, "id": b.id})
            elif b.block_type == "image":
                res.append(
                    {
                        "type": b.block_type,
                        "value": WagtailImageSerializer(b.value),
                        "id": b.id,
                    }
                )
            elif b.block_type == "video":
                from wagtail.embeds.embeds import get_embed

                yt_id = get_youtube_id(b.value.url)

                res.append(
                    {
                        "type": b.block_type,
                        "value": b.value.url,
                        "youtube_id": yt_id,
                        "video_thumbnail": video_thumbnail(yt_id),
                        "embed_url": get_embed_video_link(yt_id),
                        "id": b.id,
                    }
                )
            else:
                res.append(b.get_prep_value())
        return res

    def to_representation(self, instance):
        return self.resolve_body(obj=instance)

    class Meta:
        model = Post
        fields = "__all__"
