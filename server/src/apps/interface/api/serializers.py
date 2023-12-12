from rest_framework import serializers

from src.apps.interface.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
