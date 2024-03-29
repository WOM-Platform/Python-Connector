import json
from datetime import datetime

class Voucher:
    def to_JSON(self):
        return self.__dict__

    @staticmethod
    def create(aim: str, latitude: float, longitude: float, timestamp: datetime, count: int = 1) -> 'Voucher':
        voucher = Voucher()
        voucher.Aim = aim
        voucher.Latitude = latitude
        voucher.Longitude = longitude
        voucher.Timestamp = timestamp.isoformat()
        voucher.Count = count
        voucher.CreationMode = 'Standard'

        return voucher

    @staticmethod
    def createWithoutLocation(aim: str, timestamp: datetime, count: int = 1) -> 'Voucher':
        voucher = Voucher()
        voucher.Aim = aim
        voucher.Latitude = 0.0
        voucher.Longitude = 0.0
        voucher.Timestamp = timestamp.isoformat()
        voucher.Count = count
        voucher.CreationMode = 'SetLocationOnRedeem'

        return voucher

class VoucherEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Voucher):
            return obj.to_JSON()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
