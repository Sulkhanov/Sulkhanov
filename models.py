class Customer:
    def __init__(self, customer_id, first_name, last_name, date_of_birth,
                 id_number, phone, email, balance=0.0, status='active'):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.id_number = id_number
        self.phone = phone
        self.email = email
        self.balance = balance
        self.status = status

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Transaction:
    def __init__(self, transaction_id, customer_id, tx_type, amount, timestamp):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.type = tx_type
        self.amount = amount
        self.timestamp = timestamp
