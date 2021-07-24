from rest_framework import serializers


class CSVSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        name = data.get('employee_name') or data.get('employee_name_en')
        if not name:
            raise serializers.ValidationError('Employee name not Found')
        return dict(id=data['employee_id'], name=name, group=data['group'])

    def to_representation(self, instance):
        return instance
