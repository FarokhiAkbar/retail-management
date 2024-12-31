import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='retail_management'
        )
        self.cursor = self.conn.cursor()

    def add_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
        self.conn.commit()

    def update_product(self, product_id, name, price):
        self.cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, product_id))
        self.conn.commit()

    def get_product_names(self):
        self.cursor.execute("SELECT name FROM products")
        return [row[0] for row in self.cursor.fetchall()]

    def get_product_id(self, name):
        self.cursor.execute("SELECT id FROM products WHERE name = %s", (name,))
        result = self.cursor.fetchone()
        return result[0] if result else None  # Menghindari error jika produk tidak ditemukan

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        self.conn.commit()

    def get_transactions(self):
        self.cursor.execute("""
            SELECT p.name, t.quantity, t.total_price, t.date
            FROM transactions t
            JOIN products p ON t.product_id = p.id
        """)
        return self.cursor.fetchall()

    def calculate_total_price(self, product_id, quantity):
        self.cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
        price = self.cursor.fetchone()[0]
        return price * quantity

    def add_transaction(self, product_id, quantity, total_price):
        self.cursor.execute("INSERT INTO transactions (product_id, quantity, total_price) VALUES (%s, %s, %s)",
                            (product_id, quantity, total_price))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()