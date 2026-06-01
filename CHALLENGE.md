# Challenge – Applying Testing Levels

## Context

Kamu adalah seorang QA Engineer di startup perjalanan bernama **FlyNow**.

Tim pengembang baru saja menyelesaikan aplikasi **Flight Booking Mini App** yang dapat digunakan untuk:

- Search Flight
- Select Seat
- Payment
- Generate E-Ticket

Sebelum sistem dirilis ke pengguna, tugasmu adalah melakukan beberapa level pengujian untuk memastikan kualitas aplikasi.

---

## Part A – Unit Testing

Jalankan aplikasi dan pelajari struktur source code yang tersedia.

### Task

1. Pilih satu fungsi dari folder `services/` dan buat minimal 4 unit test cases.
2. Gunakan bantuan AI (seperti Gemini atau ChatGPT) untuk menentukan tools automated testing yang sesuai.
3. Analisis fungsi tersebut dan identifikasi kondisi yang perlu diuji.
4. Buat test cases yang dapat memberikan coverage terhadap seluruh jalur logika pada fungsi tersebut.
5. Jalankan seluruh test case yang telah dibuat.
6. Sertakan screenshot hasil eksekusi pengujian.

Gunakan format tabel berikut:

| Test Case ID | Input | Expected Output |
| ------------ | ----- | --------------- |
| TC-01        | ...   | ...             |
| TC-02        | ...   | ...             |
| TC-03        | ...   | ...             |
| TC-04        | ...   | ...             |

---

## Part B – Integration Testing

Perhatikan interaksi antar modul yang terdapat pada aplikasi.

### Task

1. Identifikasi minimal 2 integration points yang terdapat pada aplikasi.
2. Buat minimal 2 integration testing scenarios.
3. Jalankan aplikasi dan lakukan pengujian berdasarkan skenario yang telah dibuat.
4. Dokumentasikan hasil pengujian.
5. Sertakan screenshot yang menunjukkan proses pengujian atau hasil pengujian.

Gunakan format tabel berikut:

| Scenario   | Modules Involved | Expected Result |
| ---------- | ---------------- | --------------- |
| Scenario 1 | ...              | ...             |
| Scenario 2 | ...              | ...             |

---

## Part C – System Testing

Aplikasi FlyNow akan digunakan selama promo liburan nasional dan diperkirakan menerima banyak pengguna dalam waktu yang bersamaan.

**Apache JMeter** akan digunakan untuk melakukan System Testing pada aplikasi FlyNow.

### Task

1. Jalankan aplikasi FlyNow.
2. Buat Test Plan sederhana menggunakan Apache JMeter.
3. Lakukan pengujian terhadap endpoint `/api/search`.
4. Amati minimal 2 metrics hasil pengujian.
5. Analisis hasil yang diperoleh.
6. Sertakan screenshot konfigurasi JMeter dan hasil pengujian.

Gunakan format tabel berikut:

| Metric   | Result | Analysis |
| -------- | ------ | -------- |
| Metric 1 | ...    | ...      |
| Metric 2 | ...    | ...      |

---
