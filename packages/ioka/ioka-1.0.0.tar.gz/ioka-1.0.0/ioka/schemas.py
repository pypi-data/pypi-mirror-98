from abc import ABC
from datetime import date
from typing import Optional

from pydantic import BaseModel


# TODO: handle error codes via validation

class AbstractPayment(BaseModel, ABC):
    amount: int
    currency: Optional[int] = 398
    order_id: int
    tr_type: Optional[int] = 0
    email: Optional[str]
    phone: Optional[str]
    additional_params: Optional[str]
    back_url: str
    callback_url: Optional[str]
    client_id: Optional[int]
    token: Optional[str]
    template: Optional[str] = '3D'
    features: Optional[str]

    def dict(self):
        payment_dict = super().dict()
        if not self.features:
            payment_dict.pop('features')
        return payment_dict


class Reference(BaseModel):
    reference: int


class RegisterPaymentResponse(Reference):
    access_hash: str
    url: str


class RegisterPaymentRequest(AbstractPayment):
    pass


class Response(BaseModel):
    error_code: int
    error_message: str


class WithDraw(BaseModel):
    amount: int
    date: date


class Refunds(WithDraw):
    pass


class Card(BaseModel):
    holder: Optional[str]
    pan_masked: Optional[str]
    expiry_date: Optional[date]
    token: Optional[str]


class SavedCard(BaseModel):
    merchant_id: int
    client_id: int
    holder: str
    token: str
    expiry_date: str
    pan_masked: str
    is3ds: Optional[bool]
    brand: str
    emitter: Optional[str]


class Payment(AbstractPayment, Response, Reference):
    error_details: Optional[str]
    ip: Optional[str]
    withdraw: Optional[WithDraw]
    refunds: Optional[Refunds]
    card: Optional[Card]
