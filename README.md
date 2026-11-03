# Sistem Manajemen Inventaris Produk (Proyek 1)

Program CLI sederhana untuk mengelola inventaris produk e-commerce dengan operasi **sisip**, **cari**, dan **hapus** berdasarkan ID Produk.
Struktur data terpilih: **Hash Table (Python `dict`)**, karena ketiga operasi utama O(1) rata-rata.

## File
| File | Isi |
|---|---|
| `inventaris.py` | Kelas `Produk`, ADT `InventarisADT`, dan 4 implementasi: `InventarisHashTable` (terpilih), `InventarisArray`, `InventarisSortedArray`, `InventarisLinkedList` |
| `main.py` | Antarmuka CLI (memakai `InventarisHashTable`) |
| `benchmark.py` | Pengukuran waktu sisip, cari, hapus, dan tampil semua pada keempat implementasi |

## Cara menjalankan
Butuh Python 3.10 atau lebih baru (memakai `bisect` dengan parameter `key`).

```
python main.py        # program CLI
python benchmark.py   # perbandingan kinerja struktur data
```

## Menu CLI
1. Tambah produk (ID duplikat ditolak)
2. Cari produk berdasarkan ID
3. Hapus produk
4. Tampilkan semua produk
0. Keluar
