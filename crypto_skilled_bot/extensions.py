import requests

from config import VALS


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(from_val, to_val, amount):
        if from_val not in VALS:
            raise APIException(f"Неизвестная валюта <{from_val}>.")

        if to_val not in VALS:
            raise APIException(f"Неизвестная валюта <{to_val}>.")

        if from_val == to_val:
            raise APIException("Не могу обработать одинаковую валюту.")

        amount = amount.replace(',', '.')

        if not amount.replace('.', '').isnumeric():
            raise APIException(f"Количество <{amount}> не является числом")

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={VALS[from_val]}&tsyms={VALS[to_val]}').json()

        return r[VALS[to_val]] * float(amount)
