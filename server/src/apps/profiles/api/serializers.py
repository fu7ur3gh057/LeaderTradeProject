from rest_framework import serializers

from src.apps.profiles.models import Profile, LegalCard


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["full_name", "email", "city", "is_legal"]


class LegalCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalCard
        fields = "__all__"


class LegalCardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalCard
        fields = [
            "title",
            "legal_address",
            "email",
            "inn",
            "kpp",
            "bik",
            "ogrn",
            "settlement",
            "korr",
            "general_director",
        ]
