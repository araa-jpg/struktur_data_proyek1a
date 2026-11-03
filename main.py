"""
main.py
Program CLI Sistem Manajemen Inventaris Produk.
Struktur data terpilih: Hash Table (Python dict) lewat InventarisHashTable.

Jalankan:  python main.py
"""

from inventaris import Produk, InventarisHashTable


def baca_angka(pesan: str) -> int:
    while True:
        teks = input(pesan).strip()
        if teks.isdigit():
            return int(teks)
        print("  ! Masukkan angka bulat >= 0.")


def data_awal(inv) -> None:
    contoh = [
        Produk("P001", "Laptop Asus Vivobook", "Elektronik", 8500000, 15),
        Produk("P002", "Mouse Wireless Logitech", "Aksesoris", 175000, 120),
        Produk("P003", "Keyboard Mekanik", "Aksesoris", 450000, 60),
        Produk("P004", "Kaos Polos Katun", "Fashion", 65000, 300),
        Produk("P005", "Botol Minum 1L", "Rumah Tangga", 45000, 200),
    ]
    inv.muat_massal(contoh)


def menu_tambah(inv) -> None:
    print("\n-- Tambah Produk Baru --")
    id_produk = input("ID Produk : ").strip().upper()
    if not id_produk:
        print("  ! ID tidak boleh kosong.")
        return
    nama = input("Nama      : ").strip()
    kategori = input("Kategori  : ").strip()
    harga = baca_angka("Harga (Rp): ")
    stok = baca_angka("Stok      : ")
    if inv.sisip(Produk(id_produk, nama, kategori, harga, stok)):
        print(f"  ✓ Produk {id_produk} berhasil ditambahkan.")
    else:
        print(f"  ! Gagal: ID {id_produk} sudah terdaftar.")


def menu_cari(inv) -> None:
    print("\n-- Cari Produk --")
    id_produk = input("ID Produk : ").strip().upper()
    hasil = inv.cari(id_produk)
    if hasil:
        print("  ✓ Ditemukan:")
        print("   ", hasil)
    else:
        print(f"  ! Produk {id_produk} tidak ditemukan.")


def menu_hapus(inv) -> None:
    print("\n-- Hapus Produk --")
    id_produk = input("ID Produk : ").strip().upper()
    if inv.hapus(id_produk):
        print(f"  ✓ Produk {id_produk} berhasil dihapus.")
    else:
        print(f"  ! Produk {id_produk} tidak ditemukan.")


def menu_tampil(inv) -> None:
    print(f"\n-- Daftar Produk ({len(inv)} item) --")
    semua = inv.semua()
    if not semua:
        print("  (inventaris kosong)")
    for p in semua:
        print("  ", p)


def main() -> None:
    inv = InventarisHashTable()
    data_awal(inv)

    menu = {
        "1": ("Tambah produk", menu_tambah),
        "2": ("Cari produk berdasarkan ID", menu_cari),
        "3": ("Hapus produk", menu_hapus),
        "4": ("Tampilkan semua produk", menu_tampil),
    }

    while True:
        print("\n====== SISTEM MANAJEMEN INVENTARIS PRODUK ======")
        for kode, (label, _) in menu.items():
            print(f"  {kode}. {label}")
        print("  0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "0":
            print("Terima kasih. Program selesai.")
            break
        if pilihan in menu:
            menu[pilihan][1](inv)
        else:
            print("  ! Pilihan tidak valid.")


if __name__ == "__main__":
    main()
