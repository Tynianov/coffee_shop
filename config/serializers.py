from rest_framework import serializers

from utils.funcs import get_absolute_url

from .models import RestaurantConfig, RestaurantBranch


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
    working_days = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantBranch
        fields = '__all__'

    def get_branch_phone(self, obj):
        if obj.branch_phone:
            return obj.branch_phone

        config = RestaurantConfig.get_solo()
        return config.phone

    def get_working_days(self, obj):
        print('!', obj.working_days)
        if obj.working_days:
            working_days = {}
            for working_day in obj.working_days.all():
                working_days[working_day.get_name_display()] = working_day.working_hours
            return working_days
        return None
