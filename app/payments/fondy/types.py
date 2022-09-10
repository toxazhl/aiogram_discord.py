from pydantic import BaseModel


class FondyResponse(BaseModel):
    response_status: str


class RegisterPaymentResponse(FondyResponse):
    checkout_url: str
    payment_id: int


class ErrorFondyResponse(FondyResponse):
    error_code: int
    error_message: str
    request_id: str


class RecurringPaymentResponse(FondyResponse):
    actual_amount: str
    actual_currency: str
    amount: str
    approval_code: str
    card_bin: int
    card_type: str
    currency: str
    eci: str
    fee: str
    masked_card: str
    merchant_data: str
    merchant_id: int
    order_id: str
    order_status: str
    order_time: str
    parent_order_id: str
    payment_id: int
    payment_system: str
    product_id: str
    rectoken: str
    rectoken_lifetime: str
    response_code: str
    response_description: str
    # response_signature_string: str
    response_status: str
    reversal_amount: str
    rrn: str
    sender_account: str
    sender_cell_phone: str
    sender_email: str
    settlement_amount: str
    settlement_currency: str
    settlement_date: str
    signature: str
    tran_type: str
    verification_status: str
