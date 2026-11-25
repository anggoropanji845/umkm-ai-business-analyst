# KPI Definitions — UMKM AI Business Analyst

**Milestone:** 1 — Descriptive Business Analysis  
**Calculation layer:** Python / Pandas  
**Reference output:** `outputs/umkm_business_summary_stage1.json`

Dokumen ini menjelaskan definisi metrik yang digunakan dalam notebook dan custom component Langflow. Semua KPI dihitung oleh Python; LLM hanya menginterpretasikan hasilnya.

## 1. Order Performance KPIs

| KPI | Definisi | Formula / aturan | Catatan interpretasi |
|---|---|---|---|
| Total Orders | Jumlah order unik dalam dataset. | `nunique(order_id)` | Mencakup seluruh status pesanan. |
| Completed Orders | Jumlah order unik dengan status `Selesai`. | `nunique(order_id)` untuk `status_normalized = "Selesai"` | Digunakan sebagai populasi order selesai untuk AOV. |
| Cancelled Orders | Jumlah order unik dengan status `Batal`. | `nunique(order_id)` untuk `status_normalized = "Batal"` | Tidak mencakup status lain seperti sedang dikirim atau masa pengembalian. |
| Cancellation Rate | Proporsi order batal terhadap seluruh order unik. | `(Cancelled Orders / Total Orders) × 100%` | Denominator mencakup semua status pesanan. Ini definisi operasional proyek, bukan benchmark industri. |
| Completed Payment Total | Total `Total Pembayaran` pada order berstatus `Selesai`. | `sum(Total Pembayaran)` setelah filter `status_normalized = "Selesai"` | Merepresentasikan total nilai pembayaran pada order selesai, bukan laba bersih. |

## 2. Revenue / Order Value KPIs

| KPI | Definisi | Formula / aturan | Catatan interpretasi |
|---|---|---|---|
| AOV Mean — Completed | Rata-rata nilai pembayaran per order selesai. | `mean(Total Pembayaran)` untuk status `Selesai` | Hanya nilai pembayaran non-null yang masuk perhitungan. Sensitif terhadap nilai transaksi ekstrem. |
| AOV Median — Completed | Nilai tengah pembayaran order selesai. | `median(Total Pembayaran)` untuk status `Selesai` | Lebih tahan terhadap nilai transaksi ekstrem; membantu menggambarkan order tipikal. |

**Mengapa mean dan median sama-sama dilaporkan?**  
Jika mean jauh lebih tinggi daripada median, distribusi nilai order dapat condong ke kanan karena sebagian transaksi bernilai jauh lebih besar. Perbedaan ini merupakan indikasi distribusi, bukan bukti penyebab tertentu.

## 3. Quantity and Data Quality Metrics

| KPI / indikator | Definisi | Formula / aturan | Catatan interpretasi |
|---|---|---|---|
| Average Quantity — Valid Values | Rata-rata `total_qty` dari nilai yang tersedia. | `mean(total_qty)` dengan missing values diabaikan | Tidak melakukan imputasi ulang pada notebook revisi. |
| Median Quantity — Valid Values | Median `total_qty` dari nilai yang tersedia. | `median(total_qty)` dengan missing values diabaikan | Lebih robust terhadap nilai quantity yang ekstrem. |
| Missing Quantity Count | Jumlah baris dengan `total_qty` kosong. | `isna(total_qty).sum()` | Dilaporkan; tidak otomatis diisi dengan median. |
| Unknown Payment Method Count | Jumlah baris dengan metode pembayaran kosong atau bernilai `Unknown` (sesuai representasi data). | Hitung missing dan label `Unknown` pada `Metode Pembayaran`. | Tidak boleh disamakan dengan jumlah order bernilai pembayaran nol. |
| Duplicate Rows | Jumlah baris yang identik secara keseluruhan setelah pemuatan data. | `df.duplicated().sum()` | Pemeriksaan duplikasi baris. |
| Duplicate Order IDs | Jumlah kemunculan `order_id` yang terduplikasi setelah kemunculan pertama. | `df["order_id"].duplicated().sum()` | Perlu ditinjau sesuai grain dataset; bukan otomatis berarti seluruh record duplikat tidak valid. |
| Date Parse Failures | Jumlah nilai `order_date` yang gagal dikonversi menjadi tanggal. | `pd.to_datetime(order_date, errors="coerce").isna().sum()` | Interpretasikan bersama jumlah nilai kosong awal dan tanggal yang dapat dipulihkan dari timestamp. |
| Date Mismatch Count | Jumlah baris ketika tanggal `order_date` dan tanggal `Waktu Pesanan Dibuat` berbeda, pada baris yang kedua tanggalnya valid. | Bandingkan bagian tanggal dari kedua kolom. | Perbedaan perlu diperiksa; jangan otomatis memilih salah satu tanpa validasi. |

## 4. Monthly Trend Metrics

| KPI | Definisi | Formula / aturan | Catatan interpretasi |
|---|---|---|---|
| Monthly Total Orders | Jumlah order unik per bulan berdasarkan `analysis_date`. | `nunique(order_id)` per bulan | Bulan dibentuk dari tanggal analisis yang telah divalidasi. |
| Monthly Completed Orders | Jumlah order berstatus `Selesai` per bulan. | Hitung status `Selesai` per bulan | Menunjukkan volume order selesai. |
| Monthly Cancelled Orders | Jumlah order berstatus `Batal` per bulan. | Hitung status `Batal` per bulan | Menunjukkan volume pembatalan. |
| Monthly Cancellation Rate | Proporsi order batal terhadap seluruh order pada bulan yang sama. | `(Monthly Cancelled Orders / Monthly Total Orders) × 100%` | Jika total order bulan tersebut 0, nilainya `null`/N/A, bukan 0%. |

Bulan tanpa record transaksi tetap ditampilkan dalam rentang waktu sebagai gap. Gap tidak berarti cancellation rate 0%, dan tren tidak boleh diinterpretasikan seolah-olah data tersedia secara kontinu.

## 5. Segment and Product Metrics

| KPI | Definisi | Formula / aturan | Catatan interpretasi |
|---|---|---|---|
| Cancellation Rate by Payment Method | Proporsi order batal dalam setiap kelompok metode pembayaran. | `cancelled_orders_in_group / total_orders_in_group × 100%` | Tampilkan jumlah order (`n`) bersama rate. |
| Cancellation Rate by Province | Proporsi order batal dalam setiap kelompok provinsi. | `cancelled_orders_in_group / total_orders_in_group × 100%` | Hasil yang ditampilkan pada ringkasan utama menggunakan minimum 30 order per kelompok. |
| Cancellation Rate by Shipping Option | Proporsi order batal dalam setiap kelompok opsi pengiriman. | `cancelled_orders_in_group / total_orders_in_group × 100%` | Tampilkan ukuran sampel; perbedaan deskriptif bukan bukti sebab-akibat. |
| Cancellation Reasons | Frekuensi alasan pembatalan pada order berstatus `Batal`. | `value_counts()` pada `Alasan Pembatalan` untuk order batal | Jangan menghitung alasan dari seluruh order. |
| Top Categories by Unique Orders | Jumlah order unik yang memuat suatu kategori produk. | Pisahkan `product_categories` berdasarkan koma, gunakan `explode`, lalu `nunique(order_id)` per kategori. | Satu order dapat memuat beberapa kategori; jumlah antar-kategori tidak harus menjumlah ke total order. Ini bukan jumlah unit terjual. |

## 6. Reference values from the supplied cleaned dataset

Nilai berikut merupakan hasil analisis pada file cleaned yang disediakan untuk Milestone 1. Nilai ini dapat berubah jika file sumber atau aturan cleaning berubah.

| KPI | Reference value |
|---|---:|
| Total Orders | 18,868 |
| Completed Orders | 16,045 |
| Cancelled Orders | 2,573 |
| Cancellation Rate | 13.64% |
| Completed Payment Total | Rp950,963,704 |
| AOV Mean — Completed | Rp59,268.54 |
| AOV Median — Completed | Rp26,896 |
| May 2025 Cancellation Rate | 20.76% (170 / 819) |
| November 2025 Cancellation Rate | 8.93% (101 / 1,131) |

## 7. Important distinctions and limitations

1. `Unknown Payment Method` is not the same metric as `Total Pembayaran = 0`.
2. `Completed Payment Total` and AOV are not net profit. HPP, marketplace commissions, operating expenses, and other costs are not included.
3. Cancellation rate is a project-defined descriptive metric. No external industry benchmark is supplied.
4. Segment-level cancellation-rate differences do not establish causation.
5. Category counts represent unique orders containing a category, not item quantities or units sold.
6. Monthly zero-order periods have an undefined cancellation rate (`null` / N/A), not 0%.
7. The supplied CSV is already cleaned. The original raw file is needed to audit earlier missing-value imputation and initial date-parsing decisions.

## 8. Implementation consistency

Keep these definitions consistent across:
- `notebooks/UMKM_Business_Analysis_Stage1.ipynb`
- `langflow/UMKMDataAnalyzer_Stage1.py`
- `outputs/umkm_business_summary_stage1.json`
- `docs/agent_evaluation.md`
- Langflow Prompt Template

If a KPI definition changes, update the notebook, component, prompt, reference JSON, and this document together, then rerun the agent evaluation.
