from rest_framework import serializers
from api.models import Brand



class BrandSerializers(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = fields = '__all__'