from rest_framework import serializers
from rest_framework.views import exception_handler
from .models import Message, Order, User, Item, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ItemSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Item
        fields = '__all__'
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)

class OrderSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'