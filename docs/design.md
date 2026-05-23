# Design Notes

Kali LabWeave dibuat dengan tiga batasan utama:

1. Terminal-first untuk Kali Linux.
2. Tidak memiliki fitur ofensif.
3. Tidak bergantung pada package eksternal agar mudah dipasang di lab offline.

## Konsep

Tool ini menjadi "benang dokumentasi" untuk sesi lab. Setiap aksi penting dicatat sebagai event timeline sehingga report akhir bisa dibuat tanpa mencari ulang catatan yang tersebar.

## State

State utama disimpan sebagai JSON di:

```text
.labweave/state.json
```

Format JSON dipilih supaya mudah dibaca, bisa di-diff di Git, dan tetap portabel.

## Evidence

Saat evidence ditambahkan, file disalin ke folder `evidence/` dan SHA-256 dicatat. Ini membantu memastikan file report masih cocok dengan artefak yang dikumpulkan.
