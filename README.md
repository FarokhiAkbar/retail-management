# Aplikasi Manajemen Produk dan Transaksi

## Deskripsi Aplikasi
Aplikasi ini digunakan untuk mengelola produk dan mencatat transaksi penjualan di perusahaan retail skala kecil.

## Cara Menjalankan Aplikasi
1. Pastikan Anda memiliki Python dan MySQL terinstal.
2. Buat database `retail_management` dan tabel `products` dan `transactions` sesuai dengan struktur berikut:
   ```sql
   CREATE TABLE products (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       price DECIMAL(10, 2) NOT NULL
   );

   CREATE TABLE transactions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       product_id INT,
       quantity INT,
       total_price DECIMAL(10, 2),
       date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (product_id) REFERENCES products(id)
   );