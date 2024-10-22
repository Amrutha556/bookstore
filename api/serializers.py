from rest_framework import serializers
from api.models import books
from django.contrib.auth.models import User
from api.models import Carts,Reviews

class bookSerializer(serializers.Serializer):
    name=serializers.CharField()
    price=serializers.IntegerField()
    description=serializers.CharField()
    category=serializers.CharField()
    image=serializers.ImageField(required=False,default=None)

class bookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=books
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]

    def create(self, validated_data):
        return User.objects.create_user(**self.validated_data)   
    
class CartSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=serializers.CharField(read_only=True)
    books=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    books=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        fields="__all__"