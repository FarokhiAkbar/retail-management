class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Transaction:
    def __init__(self, id, product_id, quantity, total_price, date):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price
        self.date = date