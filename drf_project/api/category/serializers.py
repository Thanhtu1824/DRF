from rest_framework import serializers
from api.models import Category


class CategorySerializers(serializers.ModelSerializer):
    parent_name = serializers.CharField(source="parent.name", read_only=True)

    class Meta:
        model = Category
        fields = '__all__'