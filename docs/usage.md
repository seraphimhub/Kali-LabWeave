# Usage

## Membuat Lab Baru

```bash
labweave init demo-lab
cd demo-lab
```

Perintah ini membuat folder lab, state internal, folder evidence, notes, dan reports.

## Mencatat Scope

```bash
labweave scope add "Aset lab internal yang sudah diberi izin" --kind note --owner "Tim Lab"
```

Jenis scope yang tersedia:

- `ip`
- `domain`
- `url`
- `note`

## Mencatat Command

```bash
labweave cmd add "ip addr" --why "Mencatat interface lokal" --result "Output tersimpan di notes manual"
```

Kali LabWeave hanya mencatat command. Tool ini tidak menjalankan command tersebut.

## Menambahkan Evidence

```bash
labweave evidence add ./hasil.txt --label hasil-awal
```

File akan disalin ke `evidence/` dan hash SHA-256 dicatat di `.labweave/state.json`.

## Checklist

```bash
labweave checklist list
labweave checklist done scope-authorized
labweave checklist reset scope-authorized
```

## Report

```bash
labweave report
```

Report Markdown dibuat di folder `reports/`.
