import requests

from config import VALS


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(from_val, to_val, amount):
        if from_val not in VALS:
            raise APIException(f"Неизвестная валюта <{from_val}>.")

        if to_val not in VALS:
            raise APIException(f"Неизвестная валюта <{to_val}>.")

        if from_val == to_val:
            raise APIException("Невозможно обработать одинаковую валюту.")

        amount = amount.replace(',', '.')

        if not amount.replace('.', '').isnumeric():
            raise APIException(f"Количество <{amount}> не является числом")

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={VALS[from_val]}&tsyms={VALS[to_val]}').json()
        if 'Message' in r:
            raise Exception(r['Message'])

        return r[VALS[to_val]] * float(amount)
