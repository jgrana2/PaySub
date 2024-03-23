from Payment import Payment

class CreditCard:
    def __init__(self, card_number, card_holder, expiration, cvc, card_holder_id_number, card_holder_id_type, card_payment_method_id):
        self.card_number = card_number
        self.card_holder = card_holder
        self.card_holder_id_number = card_holder_id_number
        self.card_holder_id_type = card_holder_id_type
        self.expiration = expiration
        self.cvc = cvc
        self.payment_method_id = card_payment_method_id

    def display_card_info(self):
        print("Card Number:", self.card_number)
        print("Card Holder:", self.card_holder)
        print("Expiration Date:", self.expiration)
        print("CVC:", self.cvc)

    def process_payment(self, amount, user):
        try:
            payment = Payment(user)
            card_info = {
                "card_number": self.card_number,
                "expiration_year": f"20{self.expiration.split('/')[1]}",
                "expiration_month": self.expiration.split("/")[0],
                "security_code": self.cvc,
                "cardholder": {
                    "name": self.card_holder,
                    "identification": {
                        "number": self.card_holder_id_number,
                        "type": self.card_holder_id_type
                    }
                }
            }
            card_token = payment.create_card_token(card_info)
            payment_info = {
                "transaction_amount": float(amount),
                "token": card_token,
                "description": "Test payment",
                "payment_method_id": self.payment_method_id,
                "installments": 1,
                "payer": {
                    "email": user.email
                }
            }
            result = payment.create_payment(payment_info)
            print("status =>", result["status"])
            print("status_detail =>", result["status_detail"])
            print("id=>", result["id"])
            # Update the payment
            payment_data = {"capture": True}
            payment.update_payment(result["id"], payment_data)
            return result["status"] == 'approved'

        except Exception as e:
            print(f"An error occurred while processing the payment: {e}")
            return False