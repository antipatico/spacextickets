import datetime
from json import JSONEncoder, JSONDecoder
import uuid


class OrderStatusEncoder(JSONEncoder):
    def default(self, obj):
        from spacextickets.orders.views import OrderStatus
        if isinstance(obj, OrderStatus):
            return {
                '__type__': 'OrderStatus',
                'value': str(obj)
            }
        return TypeError("%s is not an OrderStatus." % str(obj))


class OrderStatusDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        from spacextickets.orders.views import OrderStatus
        if '__type__' in d:
            t = d.pop('__type__')
            if t == 'OrderStatus':
                name, member = d.pop('value').split(".")
                return OrderStatus[member]

        raise TypeError("%s is not an OrderStatus." % str(d))


class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return {
                '__type__': 'UUID',
                'value': str(obj)
            }
        return TypeError("%s is not an UUID." % str(obj))


class UUIDDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        if '__type__' in d:
            t = d.pop('__type__')
            if t == 'UUID':
                return uuid.UUID(d.pop('value'))

        raise TypeError("%s is not an UUID." % str(d))


class DateEncoder(UUIDEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return {
                '__type__': 'date',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
            }
        raise TypeError("%s is not a datetime.date." % str(obj))


class DateDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        if '__type__' in d:
            t = d.pop('__type__')
            if t == 'date':
                return datetime.date(**d)

        raise TypeError("%s is not a datetime.date." % str(d))


class TimeEncoder(UUIDEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.time):
            return {
                '__type__': 'time',
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
            }
        raise TypeError("%s is not a datetime.time." % str(obj))


class TimeDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        if '__type__' in d:
            t = d.pop('__type__')
            if t == 'time':
                return datetime.time(**d)

        raise TypeError("%s is not a datetime.date." % str(d))