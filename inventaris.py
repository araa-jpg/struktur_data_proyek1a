"""
inventaris.py
Sistem Manajemen Inventaris Produk (Proyek 1 - Struktur Data & Algoritma)

Berisi:
  - Produk                : data produk (atribut + representasi teks)
  - InventarisADT         : Abstract Data Type (kontrak operasi)
  - InventarisHashTable   : implementasi dengan Hash Table (dict)    -> STRUKTUR TERPILIH
  - InventarisArray       : implementasi dengan Array-based List (list)
  - InventarisSortedArray : Array List terurut berdasarkan ID + binary search (bisect)
  - InventarisLinkedList  : implementasi dengan Linked List (Node custom)

Ketiga implementasi memiliki antarmuka yang sama sehingga mudah dibandingkan.
"""

from abc import ABC, abstractmethod
from bisect import bisect_left
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
@dataclass
class Produk:
    id_produk: str
    nama: str
    kategori: str
    harga: int
    stok: int

    def __str__(self) -> str:
        harga = f"{self.harga:,}".replace(",", ".")      # format ribuan ala Indonesia
        return (f"[{self.id_produk}] {self.nama:<22} | {self.kategori:<12} | "
                f"Rp {harga:>10} | stok: {self.stok}")


# ---------------------------------------------------------------------------
# ADT (kontrak operasi)
# ---------------------------------------------------------------------------
class InventarisADT(ABC):
    """Abstract Data Type inventaris: hanya mendefinisikan APA yang dilakukan,
    bukan BAGAIMANA caranya. Cara kerja ditentukan oleh kelas turunan."""

    @abstractmethod
    def sisip(self, produk: Produk) -> bool:
        """Menambah produk baru. False jika ID sudah ada."""

    @abstractmethod
    def cari(self, id_produk: str):
        """Mengembalikan objek Produk, atau None jika tidak ditemukan."""

    @abstractmethod
    def hapus(self, id_produk: str) -> bool:
        """Menghapus produk. False jika ID tidak ditemukan."""

    @abstractmethod
    def semua(self) -> list:
        """Mengembalikan seluruh produk sebagai list."""

    @abstractmethod
    def muat_massal(self, daftar: list) -> None:
        """Memuat banyak produk sekaligus (tanpa cek duplikat).
        Dipakai untuk data awal dan benchmark."""

    @abstractmethod
    def __len__(self) -> int:
        ...


# ---------------------------------------------------------------------------
# 1) HASH TABLE (Python dict)  -> struktur data terpilih
# ---------------------------------------------------------------------------
class InventarisHashTable(InventarisADT):
    def __init__(self):
        self._data = {}                       # key: id_produk, value: Produk

    def sisip(self, produk):                  # O(1) rata-rata
        if produk.id_produk in self._data:
            return False
        self._data[produk.id_produk] = produk
        return True

    def cari(self, id_produk):                # O(1) rata-rata
        return self._data.get(id_produk)

    def hapus(self, id_produk):               # O(1) rata-rata
        if id_produk not in self._data:
            return False
        del self._data[id_produk]
        return True

    def semua(self):                          # O(n)
        return list(self._data.values())

    def muat_massal(self, daftar):
        for p in daftar:
            self._data[p.id_produk] = p

    def __len__(self):
        return len(self._data)


# ---------------------------------------------------------------------------
# 2) ARRAY-BASED LIST (Python list)
# ---------------------------------------------------------------------------
class InventarisArray(InventarisADT):
    def __init__(self):
        self._data = []

    def _indeks(self, id_produk):             # pencarian linear O(n)
        for i, p in enumerate(self._data):
            if p.id_produk == id_produk:
                return i
        return -1

    def sisip(self, produk):                  # cek duplikat O(n) + append O(1)
        if self._indeks(produk.id_produk) != -1:
            return False
        self._data.append(produk)
        return True

    def cari(self, id_produk):                # O(n)
        i = self._indeks(id_produk)
        return self._data[i] if i != -1 else None

    def hapus(self, id_produk):               # cari O(n) + geser elemen O(n)
        i = self._indeks(id_produk)
        if i == -1:
            return False
        del self._data[i]
        return True

    def semua(self):                          # O(n)
        return list(self._data)

    def muat_massal(self, daftar):
        self._data.extend(daftar)

    def __len__(self):
        return len(self._data)


# ---------------------------------------------------------------------------
# 2b) ARRAY LIST TERURUT + BINARY SEARCH (bisect)
# ---------------------------------------------------------------------------
class InventarisSortedArray(InventarisADT):
    """List yang selalu terurut menurut id_produk, sehingga pencarian
    memakai binary search O(log n). Sisip/hapus tetap O(n) karena elemen digeser."""

    def __init__(self):
        self._data = []

    def _posisi(self, id_produk):             # binary search O(log n)
        i = bisect_left(self._data, id_produk, key=lambda p: p.id_produk)
        ada = i < len(self._data) and self._data[i].id_produk == id_produk
        return i, ada

    def sisip(self, produk):                  # cari posisi O(log n) + insert O(n)
        i, ada = self._posisi(produk.id_produk)
        if ada:
            return False
        self._data.insert(i, produk)
        return True

    def cari(self, id_produk):                # O(log n)
        i, ada = self._posisi(id_produk)
        return self._data[i] if ada else None

    def hapus(self, id_produk):               # cari O(log n) + geser elemen O(n)
        i, ada = self._posisi(id_produk)
        if not ada:
            return False
        del self._data[i]
        return True

    def semua(self):                          # O(n), sudah terurut berdasarkan ID
        return list(self._data)

    def muat_massal(self, daftar):
        self._data.extend(daftar)
        self._data.sort(key=lambda p: p.id_produk)

    def __len__(self):
        return len(self._data)


# ---------------------------------------------------------------------------
# 3) LINKED LIST (Custom ADT)
# ---------------------------------------------------------------------------
class _Node:
    __slots__ = ("produk", "next")

    def __init__(self, produk, next_node=None):
        self.produk = produk
        self.next = next_node


class InventarisLinkedList(InventarisADT):
    def __init__(self):
        self._head = None
        self._size = 0

    def sisip(self, produk):                  # cek duplikat O(n) + sisip di head O(1)
        if self.cari(produk.id_produk) is not None:
            return False
        self._head = _Node(produk, self._head)
        self._size += 1
        return True

    def cari(self, id_produk):                # O(n)
        cur = self._head
        while cur is not None:
            if cur.produk.id_produk == id_produk:
                return cur.produk
            cur = cur.next
        return None

    def hapus(self, id_produk):               # telusuri O(n) + ubah pointer O(1)
        prev, cur = None, self._head
        while cur is not None:
            if cur.produk.id_produk == id_produk:
                if prev is None:
                    self._head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def semua(self):                          # O(n)
        hasil, cur = [], self._head
        while cur is not None:
            hasil.append(cur.produk)
            cur = cur.next
        return hasil

    def muat_massal(self, daftar):
        for p in daftar:
            self._head = _Node(p, self._head)
            self._size += 1

    def __len__(self):
        return self._size
