from rest_framework import serializers
from .models import Product, Stock, StockProduct
from pprint import pprint


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']
    
    def __custommap(self, dictionary):
        dictionary = dict(dictionary)
        StockProduct(
            stock = self.stock_id,
            product = dictionary['product'], 
            quantity = dictionary['quantity'],
            price = dictionary['price']
            ).save()

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        id = Stock.objects.filter(address = validated_data['address']).first()
        self.stock_id = id
        list(map(self.__custommap, positions))
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            print(stock, position['price'], position['product'], position['quantity'])
            StockProduct.objects.update_or_create(stock=stock, product = position['product'], defaults={'price': position['price'], 'quantity': position['quantity']})
        return stock
