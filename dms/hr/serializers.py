import re
import typing

from rest_framework import serializers

from employee.models import Employee

pattern = re.compile(r'^.+\) values\s?\((?P<fields>.+)\)$')


class GatewayLogSerializer(serializers.Serializer):

    def to_internal_value(self, data: typing.Dict) -> typing.Dict:
        match = pattern.search(data['log'])
        if not match:
            raise serializers.ValidationError('Log pattern not match')
        fields = match.group('fields').strip("'").split("','")
        # Date
        time = fields[1].split(':')
        date = data['date'].replace(
            hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
        # Employee
        try:
            employee = Employee.objects.get(name=fields[7])
        except Employee.DoesNotExist:
            raise serializers.ValidationError('Employee not Found') from None
        # Door
        door = fields[5]
        # Card
        card = fields[4]
        return dict(date=date, employee=employee, door=door, card=card)

    def to_representation(self, instance):
        return instance

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
