from rest_framework import serializers

from formidable.models import Item
from formidable.serializers.list import NestedListSerializer


class ItemListSerializer(NestedListSerializer):

    field_id = 'value'
    parent_name = 'field_id'

    def validate(self, data):
        data = super().validate(data)
        for index, item in enumerate(data):
            item['order'] = index

        return data


class ItemSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False, allow_null=True,
                                        allow_blank=True, source='help_text')

    class Meta:
        model = Item
        list_serializer_class = ItemListSerializer
        fields = ('value', 'label', 'description')
