import mercadopago
from PaymentsStore import PaymentStore

class Payment:
    def __init__(self, user) -> None:
        # Load environment variables from the .env file
        access_token = user.get_access_token()
         # Store MercadoPago SDK instance as an attribute
        self.sdk = mercadopago.SDK(access_token)
        self.payment_store = PaymentStore("mongodb://localhost:27017/", "PaySub", "Payments")

    def create_card_token(self, card_info):
        response = self.sdk.card_token().create(card_info)
        if response["status"] == 201:
            print("Card token created succesfully")
            return response["response"]["id"]
        else:
            raise Exception(f"Failed to create card token: {response}")

    # ========== VERY IMPORTANT FUNCTION ============
    def create_payment(self, payment_info):
        response = self.sdk.payment().create(payment_info)
        # self.payment_store.store_document(response)
        if response["status"] == 201:
            return response["response"]
        else:
            raise Exception(f"Failed to create payment: {response}")
    # ===============================================

    def update_payment(self, payment_id, payment_data):
        response = self.sdk.payment().update(payment_id, payment_data)
        if response["status"] == 200:
            return response["response"]
        else:
            raise Exception(f"Failed to update payment: {response}")