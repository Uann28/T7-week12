# Tugas 6 (Week 12) - Dashboard Visualisasi Data PySide6

Aplikasi dashboard interaktif yang dibangun menggunakan **PySide6**, **Pandas**, dan **Matplotlib**. Aplikasi ini berfungsi untuk memvisualisasikan data mentah menjadi informasi yang berguna dalam bentuk tabel, kartu ringkasan, dan grafik yang saling terintegrasi.

### 👤 Identitas
- **Nama** : Juan Jordan Anugrah
- **NIM** : F1D02310061
- **Kelas** : D

### 🌟 Fitur Utama
1. **Data Terintegrasi Otomatis:** Membaca lebih dari 50 baris data dari CSV (Script otomatis men-generate data sampel jika file CSV belum ada di komputer).
2. **Dashboard Summary:** Menampilkan ringkasan Total Penjualan, Total Transaksi, dan Rata-rata Rating secara dinamis.
3. **Matplotlib Ter-embed:** Menampilkan *Bar Chart* (Penjualan per Kategori) dan *Pie Chart* (Distribusi Tipe Pelanggan) langsung di dalam antarmuka PySide6.
4. **Filter Interaktif:** Dua *ComboBox* untuk memfilter data berdasarkan *Branch* (Cabang) dan *Product Line* (Kategori Produk). Grafik dan tabel akan otomatis diperbarui (*redraw*).
5. **Ekspor PNG:** Tombol ekspor untuk menyimpan kedua *chart* ke dalam format `.png` ke penyimpanan lokal.
6. **Data Tabular:** *QTableWidget* responsif yang menampilkan data mentah dari Pandas DataFrame.

---

### 📊 Penjelasan Dataset Kaggle (Sesuai Kriteria Nilai Bonus)

Dataset yang digunakan mengadopsi struktur dari **Supermarket Sales Dataset** dari Kaggle.
🔗 **Link Dataset Asli:** [Kaggle - Supermarket Sales](https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales)

Dataset ini merekam data historis penjualan supermarket di 3 cabang berbeda selama 3 bulan. Data ini sangat cocok untuk *dashboard* bisnis karena mencakup metrik performa produk, tren pembayaran, dan kepuasan pelanggan. 

**Makna Kolom Utama yang Divisualisasikan:**
* `Invoice ID`: Nomor identifikasi unik untuk setiap transaksi/struk belanja.
* `Branch`: Cabang supermarket tempat transaksi terjadi (A, B, atau C).
* `Customer type`: Jenis keanggotaan pembeli (Member / Normal). Divisualisasikan pada *Pie Chart* untuk melihat segmentasi.
* `Product line`: Kategori barang yang dibeli (misal: *Health and beauty*, *Electronic accessories*, dll). Divisualisasikan pada *Bar Chart* horizontal.
* `Unit price` & `Quantity`: Harga per satuan barang dan jumlah yang dibeli.
* `Total`: Total pendapatan (*revenue*) dari satu transaksi yang sudah termasuk pajak 5%.
* `Payment`: Metode pembayaran yang digunakan (*Cash*, *Credit card*, *Ewallet*).
* `Rating`: Penilaian kepuasan pelanggan (skala 1-10) terhadap layanan belanja. Ditampilkan sebagai rata-rata pada *Dashboard Card*.

---

### 🚀 Cara Menjalankan Aplikasi
1. Pastikan Python 3 dan *library* yang diperlukan sudah terpasang.
   ```bash
   pip install PySide6 pandas matplotlib