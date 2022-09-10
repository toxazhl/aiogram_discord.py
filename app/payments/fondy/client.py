import cloudipsp
from cloudipsp import Api, Checkout, Payment, Pcidss

from .types import RegisterPaymentResponse, ErrorFondyResponse, RecurringPaymentResponse


class FondyClient:
    def __init__(
        self,
        merchant_id: int | str,
        secret_key: str,
    ):
        self.api = Api(
            merchant_id=merchant_id,
            secret_key=secret_key,
        )
        self.payment = Payment(api=self.api)
        self.pcidss = Pcidss(api=self.api)

    def register_payment(
        self,
        amount: int,
        webhook_url: str,
        order_desc: str,
        lifetime: str | int,
        required_rectoken: str = "Y",
        lang: str = "uk",
    ):
        checkout = Checkout(api=self.api)
        data = {
            "currency": "UAH",
            "amount": amount,
            'server_callback_url': webhook_url,
            'order_desc': order_desc,
            'lifetime': lifetime,
            "required_rectoken": required_rectoken,
            "lang": lang,
        }
        try:
            return RegisterPaymentResponse.parse_obj(checkout.url(data))
        except cloudipsp.exceptions.ResponseError as error:
            return ErrorFondyResponse.parse_obj(error.response)

    def recurring_payment(
        self,
        rectoken: str,
        amount: int,
        currency: str = "UAH",
    ):
        data = {
            "rectoken": rectoken,
            "amount": amount,
            "currency": currency
        }
        try:
            response = self.payment.recurring(data)
            return RecurringPaymentResponse.parse_obj(response)
        except cloudipsp.exceptions.ResponseError as error:
            return ErrorFondyResponse.parse_obj(error.response)
