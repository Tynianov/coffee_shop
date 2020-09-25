from rest_framework import serializers

from utils.funcs import get_absolute_url

from .models import RestaurantConfig, RestaurantBranch, AppMetadataConfig


class RestaurantConfigSerializers(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantConfig
        fields = ['name', 'email', 'website', 'phone', 'instagram_link', 'facebook', 'logo']

    def get_logo(self, obj):
        if obj.logo:
            return get_absolute_url(obj.logo.url)
        return None


class RestaurantBranchListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantBranch
        fields = ['id', 'branch_name', 'image']

    def get_image(self, obj):
        if obj.image:
            return get_absolute_url(obj.image.url)
        return None


class RestaurantBranchDetailsSerializer(RestaurantBranchListSerializer):
    branch_phone = serializers.SerializerMethodField()
    weekday_working_hours = serializers.SerializerMethodField()
    weekend_working_hours = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantBranch
        fields = '__all__'

    def get_branch_phone(self, obj):
        if obj.branch_phone:
            return obj.branch_phone

        config = RestaurantConfig.get_solo()
        return config.phone

    def get_weekend_working_hours(self, obj):
        if obj.weekend_working_hours:
            return obj.weekend_working_hours.__str__()
        return None

    def get_weekday_working_hours(self, obj):
        if obj.weekday_working_hours:
            return obj.weekday_working_hours.__str__()
        return None


class TnCSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppMetadataConfig
        fields = ['terms_and_conditions']


class WebPageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppMetadataConfig
        fields = '__all__'
