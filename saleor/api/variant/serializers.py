# variant rest api serializers.py
from datetime import date
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...product.models import ProductVariant
from ...discount.models import Sale
from ...discount.models import get_variant_discounts
from rest_framework.serializers import (
                SerializerMethodField,
                )
User = get_user_model()


class VariantListSerializer(serializers.ModelSerializer):
    productName = SerializerMethodField()
    price = SerializerMethodField()
    quantity = SerializerMethodField()
    tax = SerializerMethodField()
    discount = SerializerMethodField()
    product_category = SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = (
            'id',
            'productName',
            'sku',
            'price',
            'tax',
            'discount',
            'quantity',
            'product_category',
        )

    def get_discount(self, obj):
        today = date.today()
        price = obj.get_price_per_item().gross
        discounts = Sale.objects.filter(start_date__lte=today).filter(end_date__gte=today)
        discount = 0
        discount_list = get_variant_discounts(obj, discounts)
        for discount in discount_list:
            try:
                discount = discount.factor
                discount = (Decimal(discount) * Decimal(price))
            except:
                discount = discount.amount.gross

        return discount

    def get_quantity(self, obj):
        quantity = obj.get_stock_quantity()
        return quantity

    def get_productName(self, obj):
        productName = obj.display_product()
        return productName

    # def get_description(self,obj):
    #     return self.products.description
    def get_price(self, obj):
        price = obj.get_price_per_item().gross
        return price

    def get_tax(self, obj):
        if obj.product.product_tax:
            tax = obj.product.product_tax.tax
        else:
            tax = 0
        return tax

    def get_product_category(self, obj):
        product_category = obj.product_category()
        return product_category