from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from saleor.room.models import Room as Table
from saleor.room.models import RoomImage as Image
from saleor.wing.models import Wing


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
    maintenance_url = serializers.HyperlinkedIdentityField(view_name='dashboard:add_room_issue')
    update_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-edit')
    view_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-view')
    delete_url = serializers.HyperlinkedIdentityField(view_name='dashboard:room-delete')
    price = serializers.SerializerMethodField()
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
                  'update_url',
                  'view_url',
                  'delete_url',
                  'maintenance_url'
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
