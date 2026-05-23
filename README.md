# Kali LabWeave

Kali LabWeave adalah tool CLI untuk terminal Kali Linux yang membantu mendokumentasikan sesi lab secara rapi, konsisten, dan mudah dijadikan laporan. Tool ini mencatat scope, catatan, command log, evidence beserta SHA-256, checklist, timeline, dan menghasilkan report Markdown.

Kali LabWeave dibuat sebagai alat pendamping dokumentasi untuk lab legal, CTF, training, audit internal, atau pekerjaan yang memiliki izin tertulis. Tool ini tidak menjalankan scanning, eksploitasi, brute force, credential theft, bypass, atau aktivitas ofensif lain.

## Fitur Utama

- Membuat workspace lab dengan struktur folder otomatis.
- Mencatat scope atau batasan pengujian yang sudah diotorisasi.
- Menyimpan catatan singkat langsung dari terminal.
- Mencatat command yang pernah dijalankan, termasuk alasan dan ringkasan hasil.
- Menyalin file evidence ke folder project dan menyimpan hash SHA-256.
- Menyediakan checklist workflow lab agar proses dokumentasi tidak tercecer.
- Membuat laporan Markdown siap diedit, di-commit, atau dibagikan.
- Memiliki `doctor` command untuk mengecek kesiapan lingkungan Kali/Codespaces.
- Dibuat dengan Python standard library, tanpa dependency runtime eksternal.

## Kapan Tool Ini Digunakan

Gunakan Kali LabWeave ketika Anda ingin:

- membuat dokumentasi lab Kali yang lebih terstruktur,
- menyiapkan bukti kerja dengan hash file,
- menjaga catatan command tetap mudah dilacak,
- membuat report otomatis setelah sesi lab,
- menyimpan riwayat pembelajaran, CTF, atau audit internal dalam GitHub.

## Persyaratan

- Kali Linux, Debian/Ubuntu, WSL Kali, atau GitHub Codespaces.
- Python 3.10 atau lebih baru.
- `git` untuk clone dan upload repository.
- `python3-venv` jika menjalankan di Kali/Debian.

Pada Kali Linux, jika `venv` belum tersedia:

```bash
sudo apt update
sudo apt install -y python3 python3-venv git
```

## Instalasi Di Kali Linux

Clone repository:

```bash
git clone https://github.com/USERNAME/kali-labweave.git
cd kali-labweave
```

Buat virtual environment dan install package:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Cek instalasi:

```bash
labweave --version
labweave doctor
```

Kali Linux modern biasanya mengaktifkan proteksi PEP 668 sehingga install package Python langsung ke sistem tidak disarankan. Karena itu, instalasi dengan virtual environment adalah cara yang paling aman.

## Instalasi Dengan Script

Repository ini menyediakan script instalasi sederhana:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

Script tersebut akan:

- membuat `.venv`,
- menginstall project dalam mode editable,
- membuat symlink `labweave` ke `$HOME/.local/bin/labweave`.

Jika command `labweave` belum dikenali setelah menjalankan script, tambahkan `$HOME/.local/bin` ke `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Untuk membuatnya permanen di Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Instalasi Di GitHub Codespaces

Project ini sudah menyediakan konfigurasi devcontainer:

```text
.devcontainer/devcontainer.json
```

Saat repository dibuka di Codespaces, setup akan menjalankan:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
```

Jika perlu menjalankan manual di terminal Codespaces:

```bash
source .venv/bin/activate
labweave doctor
```

## Quick Start

Buat workspace lab baru:

```bash
labweave init latihan-kali
cd latihan-kali
```

Tambahkan scope legal:

```bash
labweave scope add "Lab lokal yang sudah diberi izin" --kind note --owner "Saya"
```

Tambahkan catatan:

```bash
labweave note add "Sesi dimulai, fokus pada dokumentasi baseline." --tag kickoff
```

Catat command yang sudah dijalankan:

```bash
labweave cmd add "ip addr" --why "Mencatat interface lokal" --result "Berhasil"
```

Tambahkan evidence file:

```bash
echo "contoh evidence" > hasil.txt
labweave evidence add hasil.txt --label hasil-awal
```

Lihat checklist dan tandai item selesai:

```bash
labweave checklist list
labweave checklist done scope-authorized
```

Buat report Markdown:

```bash
labweave report
```

Report akan tersimpan di folder:

```text
reports/
```

## Contoh Workflow Lengkap

```bash
labweave init demo-lab
cd demo-lab

labweave scope add "Target hanya lab lokal milik sendiri" --kind note --owner "Nama Anda"
labweave note add "Menyiapkan dokumentasi awal." --tag setup
labweave cmd add "uname -a" --why "Mencatat informasi kernel lab" --result "Output dicek"
labweave cmd add "ip addr" --why "Mencatat interface lokal" --result "Interface aktif ditemukan"
labweave checklist done scope-authorized
labweave checklist done environment-noted
labweave report
labweave status
```

## Command Reference

### `labweave init`

Membuat workspace lab baru.

```bash
labweave init NAMA_PROJECT
labweave init NAMA_PROJECT --root /path/tujuan
```

### `labweave doctor`

Mengecek kesiapan environment terminal.

```bash
labweave doctor
```

### `labweave status`

Menampilkan ringkasan project aktif.

```bash
labweave status
```

### `labweave scope add`

Mencatat scope atau batasan legal.

```bash
labweave scope add "192.168.56.10" --kind ip --owner "Tim Internal"
labweave scope add "example.local" --kind domain --owner "Tim Internal"
labweave scope add "Catatan batasan pengujian" --kind note --owner "Saya"
```

Jenis scope yang tersedia:

- `ip`
- `domain`
- `url`
- `note`

### `labweave note add`

Menambahkan catatan.

```bash
labweave note add "Catatan penting dari sesi lab"
labweave note add "Baseline selesai dicatat" --tag baseline --tag report
```

### `labweave cmd add`

Mencatat command tanpa menjalankan command tersebut.

```bash
labweave cmd add "ip addr"
labweave cmd add "uname -a" --why "Mencatat sistem" --result "Berhasil"
```

### `labweave evidence add`

Menyalin file evidence ke folder project dan mencatat SHA-256.

```bash
labweave evidence add ./hasil.txt
labweave evidence add ./screenshot.txt --label bukti-awal
```

### `labweave checklist`

Mengelola checklist lab.

```bash
labweave checklist list
labweave checklist done scope-authorized
labweave checklist reset scope-authorized
```

### `labweave timeline`

Menampilkan timeline aktivitas project.

```bash
labweave timeline
labweave timeline --limit 10
```

### `labweave report`

Membuat report Markdown.

```bash
labweave report
labweave report --output laporan-akhir.md
```

## Struktur Workspace Yang Dibuat

Saat menjalankan `labweave init latihan-kali`, struktur berikut akan dibuat:

```text
latihan-kali/
├── .labweave/
│   └── state.json
├── evidence/
├── notes/
│   └── README.md
└── reports/
```

Penjelasan:

- `.labweave/state.json` menyimpan state utama project.
- `evidence/` menyimpan file evidence yang disalin oleh tool.
- `notes/` menyimpan catatan manual tambahan.
- `reports/` menyimpan report Markdown yang dibuat otomatis.

## Struktur Repository

```text
.
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── design.md
│   └── usage.md
├── scripts/
│   └── install.sh
├── src/
│   └── kali_labweave/
├── tests/
│   └── test_core.py
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
└── pyproject.toml
```

## Testing

Jalankan test dari root repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
```

Smoke test CLI:

```bash
labweave --version
labweave doctor
```

## Upload Ke GitHub

Jika repository belum diinisialisasi:

```bash
git init
git add .
git commit -m "initial kali labweave"
```

Buat repository baru dan push menggunakan GitHub CLI:

```bash
gh repo create kali-labweave --public --source=. --remote=origin --push
```

Jika repository GitHub sudah dibuat manual:

```bash
git remote add origin https://github.com/seraphimhub/kali-labweave.git
git branch -M main
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub Anda.

## Troubleshooting

### `externally-managed-environment`

Jika muncul error ini saat menjalankan `pip install`, gunakan virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

### `labweave: command not found`

Pastikan virtual environment aktif:

```bash
source .venv/bin/activate
```

Atau tambahkan `$HOME/.local/bin` ke `PATH` jika menggunakan `scripts/install.sh`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### `no LabWeave project found`

Jalankan command dari dalam folder project yang dibuat oleh `labweave init`, atau gunakan opsi `--project`:

```bash
labweave --project /path/ke/project status
```

## Etika Dan Batasan Penggunaan

Kali LabWeave hanya ditujukan untuk dokumentasi dan pelaporan. Gunakan hanya pada:

- lab pribadi,
- CTF,
- training resmi,
- sistem milik sendiri,
- pekerjaan audit atau assessment yang memiliki izin tertulis.

Jangan gunakan tool ini untuk mendukung aktivitas ilegal, tidak berizin, atau merugikan pihak lain.

## Lisensi

Project ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.
