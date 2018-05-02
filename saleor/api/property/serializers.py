from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from saleor.room.models import Room as Table
from saleor.room.models import RoomImage as Image
from saleor.wing.models import Wing
from saleor.billpayment.models import BillPayment

class ImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )

    class Meta:
        model = Image
        fields = ('id',
                  'room',
                  'image')


class TableListSerializer(serializers.ModelSerializer):
    rental_income_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-rental-income')
    maintenance_url = serializers.HyperlinkedIdentityField(view_name='dashboard:add_room_issue')
    update_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-edit')
    view_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-view')
    delete_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-delete')
    price = serializers.SerializerMethodField()
    total_tax = serializers.SerializerMethodField()
    total_rent = serializers.SerializerMethodField()
    total_maintenance = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()
    room_wing = serializers.SerializerMethodField()
    room_images = ImageSerializer(many=True)

    class Meta:
        model = Table
        fields = ('id',
                  'name',
                  'room_type',
                  'room_wing',
                  'price',
                  'service_charges',
                  'bedrooms',
                  'parking_space',
                  'floor_space',
                  'is_booked',
                  'description',
                  'room_images',
                  'total_tax',
                  'total_rent',
                  'total_maintenance',
                  'total_income',
                  'update_url',
                  'view_url',
                  'delete_url',
                  'maintenance_url',
                  'rental_income_url'
                 )

    def get_price(self, obj):
        try:
            return obj.price.gross
        except:
            return ''

    def get_room_type(self, obj):
        try:
            return obj.room_type.name
        except:
            return ''

    def get_room_wing(self, obj):
        try:
            return obj.room_wing.name
        except:
            return ''

    def get_total_tax(self, obj):
        tax = 0
        try:
            rents = BillPayment.objects.filter(bill__billtype__name='Rent', room__pk=obj.id)
            for i in rents:
                tax += i.bill.tax
        except Exception as e:
            print(e)
        return tax

    def get_total_rent(self, obj):
        amount = 0
        try:
            rents = BillPayment.objects.filter(bill__billtype__name='Rent', room__pk=obj.id)
            for i in rents:
                amount += i.bill.amount
        except Exception as e:
            print(e)
        return amount

    def get_total_maintenance(self, obj):
        maintenance = 0
        try:
            rents = BillPayment.objects.filter(bill__billtype__name='Maintenance', room__pk=obj.id)
            for i in rents:
                maintenance += i.bill.amount
        except Exception as e:
            print ('-')*100
            print(e)
        return maintenance

    def get_total_income(self, obj):
        # return 0
        return (self.get_total_rent(obj) - ( self.get_total_maintenance(obj) + self.get_total_tax(obj) ) )


class WingSerializer(serializers.ModelSerializer):
    room_wing = TableListSerializer(many=True)

    class Meta:
        model = Wing
        fields = ('id',
                  'name',
                  'room_wing')


class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id',
                  'name',
                  'description',)

    def create(self, validated_data):
        instance = Table()
        instance.name = validated_data.get('name')
        if validated_data.get('description'):
            instance.description = validated_data.get('description')
        instance.save()

        return instance


class UpdateSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ('id',
                  'name',
                  'room_type',
                  'room_wing',
                  'price',
                  'service_charges',
                  )

    def get_price(self, obj):
        try:
            return obj.price.gross
        except:
            return ''

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
