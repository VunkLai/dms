from rest_framework import serializers


class CSVSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        name = data.get('employee_name') or data.get('employee_name_en')
        if not name:
            raise serializers.ValidationError('Employee name not Found')

        return dict(
            id=data['employee_id'],
            name=name,
            dep_id=data['dep_id'],
            dep_name=data['dep_name'],
            group=data['group'])

    def to_representation(self, instance):
        return instance

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
