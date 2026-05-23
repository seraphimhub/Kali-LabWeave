# Contributing

Terima kasih ingin mengembangkan Kali LabWeave.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
```

## Panduan

- Jaga tool tetap terminal-first dan kompatibel dengan Kali Linux.
- Jangan menambahkan fitur ofensif seperti eksploitasi, credential theft, brute force, atau bypass.
- Utamakan standard library Python agar mudah dipasang di lingkungan lab.
- Tambahkan test untuk perubahan perilaku CLI atau storage.

## Format Commit

Gunakan pesan commit pendek dan jelas, misalnya:

```text
add report timeline section
fix evidence path handling
```
