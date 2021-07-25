import re
import typing

from django.utils import timezone
from rest_framework import serializers

from employee.models import Employee

pattern = re.compile(r'^.+\) values\s?\((?P<fields>.+)\)$')

DOORS = {
    '內大門': '辦公室',
    '外大門': '辦公室',
    '實驗室門': '實驗室',
    '機房': '機房',
}


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
        except Employee.DoesNotExist as e:
            raise serializers.ValidationError('Employee not Found') from e
        # Door
        try:
            # door = DOORS[fields[5]]
            floor, door = fields[5].split('F', 1)
            floor = int(floor)
            door = DOORS[door]
        except KeyError as e:
            raise serializers.ValidationError('Door is invalid') from e
        # Card
        card = fields[4]
        return dict(
            date=date, employee=employee, floor=floor, door=door, card=card)

    def to_representation(self, instance):
        return instance

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HealthDeclaration(serializers.Serializer):

    def to_internal_value(self, data: typing.Dict) -> typing.Dict:
        # date
        try:
            date_string = data[0].replace('上午', 'am').replace('下午', 'pm')
            naive = timezone.datetime.strptime(date_string, '%Y/%m/%d %p %I:%M:%S')
            date = timezone.make_aware(naive)
        except ValueError as e:
            raise serializers.ValidationError('date is invalid') from e
        # working_from
        if not data[1] in ['正常上班', '在家工作', '請假', '出差']:
            raise serializers.ValidationError('`working from` is invalid')
        working_from = data[1]
        # employee
        try:
            employee = Employee.objects.get(id=f'APM{data[2]}')
        except Employee.DoesNotExist as e:
            raise serializers.ValidationError('Employee ID is invalid') from e
        # symptom
        symptom = data[4]
        # measuring_type
        measuring_type = data[5]
        # temperature
        temperature = data[6]
        # risk
        risk = data[7]
        # 61, 62, 63
        row61 = data[8]
        row62 = data[9]
        row63 = data[10]
        return dict(
            date=date,
            working_from=working_from,
            employee=employee,
            symptom=symptom,
            measuring_type=measuring_type,
            temperature=temperature,
            risk=risk,
            row61=row61,
            row62=row62,
            row63=row63,
        )

    def to_representation(self, instance):
        return instance

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
