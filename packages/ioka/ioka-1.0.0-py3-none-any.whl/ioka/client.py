from json.decoder import JSONDecodeError
from typing import List

from pydantic import ValidationError, parse_obj_as
from restaiohttp import API
from ioka import schemas


class IOKA:

    def __init__(self, secret_key: str, host: str):
        self.secret_key = secret_key
        self.host = host

    @property
    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept-Language': 'ru',
            'Authorization': f'Bearer {self.secret_key}'
        }

    def prepare_url(self, url_path: str, params: dict = None) -> str:
        if params:
            from urllib.parse import urlencode
            query_params = urlencode(params)
            return f'{self.host}{url_path}?{query_params}'
        return f'{self.host}{url_path}'

    async def register_payment(self, payment: schemas.AbstractPayment):
        url_path = '/api/payments/register/'
        url = self.prepare_url(url_path)
        data = payment.dict()

        async with API(url=url) as api:
            response = await api.post(data=data, headers=self._headers)
            try:
                model = schemas.RegisterPaymentResponse(**response)
                return model
            except ValidationError as e:
                return e.json()

    async def change_payment_amount(self, reference: int, amount: int):
        url_path = f'/api/payments/{reference}/amount/'
        url = self.prepare_url(url_path)
        data = {
            'amount': amount
        }

        async with API(url=url) as api:
            try:
                response = await api.put(data=data, headers=self._headers)
                return response
            except JSONDecodeError as e:
                # TODO: Need discussing
                return {'status': '204 No Content'}

    async def withdraw_payment(self, reference: int, amount: int):
        url_path = '/api/payments/withdraw/'
        url = self.prepare_url(url_path)
        data = {
            'reference': reference,
            'amount': amount
        }

        async with API(url=url) as api:
            response = await api.post(data=data, headers=self._headers)
            return response

    async def cancel_payment(self, reference: int):
        url_path = '/api/payments/cancel/'
        url = self.prepare_url(url_path)
        data = {
            'reference': reference
        }

        async with API(url=url) as api:
            response = await api.post(data=data, headers=self._headers)
            try:
                model = schemas.Response(**response)
                return model
            except ValidationError as e:
                return e.json()

    async def refund_payment(self, reference: int, amount: int, reason: str = None):
        url_path = '/api/payments/refund/'
        url = self.prepare_url(url_path)
        data = {
            'reference': reference,
            'amount': amount,
            'reason': reason
        }

        async with API(url=url) as api:
            response = await api.post(data=data, headers=self._headers)
            try:
                model = schemas.Response(**response)
                return model
            except ValidationError as e:
                return e.json()

    async def get_payment_status(self, reference: int):
        url_path = f'/api/payments/{reference}/status/'
        url = self.prepare_url(url_path)

        async with API(url=url) as api:
            response = await api.get(headers=self._headers)
            try:
                model = schemas.Payment(**response)
                return model
            except ValidationError as e:
                return e.json()

    async def get_client_saved_cards(self, client_id: int):
        url_path = '/api/cards/'
        params = {
            'client_id': client_id,
        }
        url = self.prepare_url(url_path, params=params)
        async with API(url=url) as api:
            response = await api.get(headers=self._headers)
            try:
                models = parse_obj_as(List[schemas.SavedCard], response)
                return models
            except ValidationError as e:
                return e.json()

    async def get_client_saved_card_by_token(self, token: str, client_id: int):
        url_path = f'/api/cards/{token}/'
        params = {
            'client_id': client_id
        }
        url = self.prepare_url(url_path, params=params)

        async with API(url=url) as api:
            response = await api.get(headers=self._headers)
            try:
                model = schemas.SavedCard(**response)
                return model
            except ValidationError as e:
                return e.json()

    async def delete_saved_card_by_token(self, token: str) -> dict:
        url_path = f'/api/cards/{token}/'
        url = self.prepare_url(url_path)

        async with API(url=url) as api:
            response = await api.delete(headers=self._headers)
            return response
