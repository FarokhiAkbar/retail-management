import tkinter as tk
from tkinter import messagebox, ttk
from config import Database
from models import Product, Transaction

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Produk dan Transaksi")
        self.root.geometry("800x600")
        self.root.configure(bg="#eaeaea")

        # Database setup
        self.db = Database()

        # Title Label
        self.title_label = tk.Label(self.root, text="Manajemen Produk dan Transaksi", font=("Arial", 20, "bold"), bg="#eaeaea", fg="#333")
        self.title_label.pack(pady=20)

        # Frame untuk manajemen produk
        self.frame_product = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RAISED)
        self.frame_product.pack(pady=10, padx=20, fill=tk.X)

        self.label_name = tk.Label(self.frame_product, text="Nama Produk:", bg="#ffffff")
        self.label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = tk.Entry(self.frame_product, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_price = tk.Label(self.frame_product, text="Harga Produk:", bg="#ffffff")
        self.label_price.grid(row=1, column=0, padx=10, pady=10)
        self.entry_price = tk.Entry(self.frame_product, width=30)
        self.entry_price.grid(row=1, column=1, padx=10, pady=10)

        self.btn_add_product = tk.Button(self.frame_product, text="Tambah Produk", command=self.add_product, bg="#4CAF50", fg="white", width=15)
        self.btn_add_product.grid(row=2, columnspan=2, pady=10)

        self.btn_update_product = tk.Button(self.frame_product, text="Update Produk", command=self.update_product, bg="#2196F3", fg="white", width=15)
        self.btn_update_product.grid(row=3, columnspan=2, pady=5)

        self.btn_delete_product = tk.Button(self.frame_product, text="Hapus Produk", command=self.delete_product, bg="#F44336", fg="white", width=15)
        self.btn_delete_product.grid(row=4, columnspan=2, pady=5)

        # Frame untuk transaksi
        self.frame_transaction = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RAISED)
        self.frame_transaction.pack(pady=10, padx=20, fill=tk.X)

        self.label_product = tk.Label(self.frame_transaction, text="Pilih Produk:", bg="#ffffff")
        self.label_product.grid(row=0, column=0, padx=10, pady=10)
        self.dropdown_product = tk.StringVar(self.frame_transaction)
        self.product_menu = ttk.Combobox(self.frame_transaction, textvariable=self.dropdown_product, values=self.db.get_product_names(), state="readonly")
        self.product_menu.grid(row=0, column=1, padx=10, pady=10)

        self.label_quantity = tk.Label(self.frame_transaction, text="Jumlah:", bg="#ffffff")
        self.label_quantity.grid(row=1, column=0, padx=10, pady=10)
        self.entry_quantity = tk.Entry(self.frame_transaction, width=30)
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=10)

        self.btn_add_transaction = tk.Button(self.frame_transaction, text="Tambah Transaksi", command=self.add_transaction, bg="#2196F3", fg="white", width=15)
        self.btn_add_transaction.grid(row=2, columnspan=2, pady=10)

        # Frame untuk menampilkan transaksi
        self.frame_display = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RAISED)
        self.frame_display.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.label_display = tk.Label(self.frame_display, text="Daftar Transaksi", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333")
        self.label_display.grid(row=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.frame_display, columns=("Nama Produk", "Jumlah", "Total Harga", "Tanggal"), show='headings')
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.tree.heading("Nama Produk", text="Nama Produk")
        self.tree.heading("Jumlah", text="Jumlah")
        self.tree.heading("Total Harga", text="Total Harga")
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.column("Total Harga", width=100, anchor='e')

        self.display_transactions()

        # Configure grid weights to make the treeview expand
        self.frame_display.grid_rowconfigure(1, weight=1)
        self.frame_display.grid_columnconfigure(0, weight=1)

    def add_product(self):
        name = self.entry_name.get()
        price = self.entry_price.get()
        if name and price:
            try:
                price = float(price)
                self.db.add_product(name, price)
                messagebox.showinfo("Info", "Produk berhasil ditambahkan.")
                self.entry_name.delete(0, tk.END)
                self.entry_price.delete(0, tk.END)
                self.product_menu['values'] = self.db.get_product_names()  # Refresh product list
            except ValueError:
                messagebox.showwarning("Perhatian", "Harga harus berupa angka.")
        else:
            messagebox.showwarning("Perhatian", "Pastikan semua field diisi.")

    def update_product(self):
        selected_product = self.dropdown_product.get()
        if selected_product:
            name = self.entry_name.get()
            price = self.entry_price.get()
            if name and price:
                try:
                    price = float(price)
                    product_id = self.db.get_product_id(selected_product)
                    self.db.update_product(product_id, name, price)
                    messagebox.showinfo("Info", "Produk berhasil diperbarui.")
                    self.entry_name.delete(0, tk.END)
                    self.entry_price.delete(0, tk.END)
                    self.product_menu['values'] = self.db.get_product_names()  # Refresh product list
                except ValueError:
                    messagebox.showwarning("Perhatian", "Harga harus berupa angka.")
            else:
                messagebox.showwarning("Perhatian", "Pastikan semua field diisi.")
        else:
            messagebox.showwarning("Perhatian", "Silakan pilih produk yang ingin diperbarui.")

    def delete_product(self):
        selected_product = self.dropdown_product.get()
        if selected_product:
            confirmation = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus produk '{selected_product}'?")
            if confirmation:
                product_id = self.db.get_product_id(selected_product)
                self.db.delete_product(product_id)
                messagebox.showinfo("Info", "Produk berhasil dihapus.")
                self.entry_name.delete(0, tk.END)
                self.entry_price.delete(0, tk.END)
                self.product_menu['values'] = self.db.get_product_names()  # Refresh product list
                self.dropdown_product.set("")  # Reset dropdown
        else:
            messagebox.showwarning("Perhatian", "Silakan pilih produk yang ingin dihapus.")

    def add_transaction(self):
        product_name = self.dropdown_product.get()
        product_id = self.db.get_product_id(product_name)
        quantity = self.entry_quantity.get()
        if product_id and quantity.isdigit() and int(quantity) > 0:
            total_price = self.db.calculate_total_price(product_id, int(quantity))
            self.db.add_transaction(product_id, int(quantity), total_price)
            messagebox.showinfo("Info", "Transaksi berhasil ditambahkan.")
            self.entry_quantity.delete(0, tk.END)
            self.display_transactions()
        else:
            messagebox.showwarning("Perhatian", "Pastikan jumlah valid dan produk dipilih.")

    def display_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        transactions = self.db.get_transactions()
        for transaction in transactions:
            self.tree.insert("", tk.END, values=transaction)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()