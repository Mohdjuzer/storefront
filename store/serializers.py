from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Review

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.SerializerMethodField(method_name='get_products_count', read_only=True)
    def get_products_count(self, collection: Collection):
        return collection.product_set.count()
        
    

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','slug','description','inventory', 'unit_price','price_tax', 'collection']
    price_tax = serializers.SerializerMethodField(method_name='calc_tax')
    def calc_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)

class ReviewSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']     
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)   
 
        