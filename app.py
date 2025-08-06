# app.py
from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# --- BANK SOAL ---
# (Semua soal dari permintaan sebelumnya dimasukkan di sini)
questions = {
    'pilihan_ganda': [
        # Soal 1-20
        {"id": "pg1", "soal": "Siapakah tokoh yang pertama kali memperkenalkan istilah Kecerdasan Artifisial (AI) pada tahun 1956?", "options": ["Russel dan Norvig", "Garry Kasparov", "Ahmad Humaini", "John McCarthy", "Alan Turing"], "jawaban": "John McCarthy", "poin": 2.5},
        {"id": "pg2", "soal": "Menurut definisi KBBI, Kecerdasan Artifisial adalah program komputer yang dirancang untuk meniru kecerdasan manusia dalam hal...", "options": ["Memiliki perasaan dan emosi", "Mengambil keputusan dan menyediakan dasar penalaran", "Membutuhkan istirahat seperti manusia", "Berinteraksi sosial secara langsung", "Memiliki kesadaran penuh akan eksistensinya"], "jawaban": "Mengambil keputusan dan menyediakan dasar penalaran", "poin": 2.5},
        {"id": "pg3", "soal": "Tahapan evolusi AI di mana sistem masih mengandalkan logika dan aturan-aturan yang eksplisit disebut sebagai...", "options": ["Era Deep Learning", "Era Pembelajaran Mesin", "Era Simbolik", "Era Big Data", "Era Komputasi Kuantum"], "jawaban": "Era Simbolik", "poin": 2.5},
        {"id": "pg4", "soal": "Kategori AI yang memiliki kecerdasan setingkat manusia secara menyeluruh dan dapat melakukan tugas apa pun yang dapat dilakukan manusia adalah...", "options": ["Artificial Narrow Intelligence (ANI)", "Artificial Superintelligence (ASI)", "Artificial General Intelligence (AGI)", "Reactive Machine AI", "Limited Memory AI"], "jawaban": "Artificial General Intelligence (AGI)", "poin": 2.5},
        {"id": "pg5", "soal": "Superkomputer IBM Deep Blue yang mengalahkan grand master catur Garry Kasparov adalah contoh dari jenis AI...", "options": ["Theory of Mind AI", "Self Aware AI", "Limited Memory AI", "Reactive Machine AI", "Artificial General Intelligence (AGI)"], "jawaban": "Reactive Machine AI", "poin": 2.5},
        {"id": "pg6", "soal": "Manakah di antara berikut ini yang merupakan contoh dari aplikasi Limited Memory AI?", "options": ["IBM Deep Blue", "Sistem rekomendasi Netflix di awal kemunculannya", "Kendaraan self-driving", "Kalkulator", "Program pengecek ejaan sederhana"], "jawaban": "Kendaraan self-driving", "poin": 2.5},
        {"id": "pg7", "soal": "Jenis AI yang diprediksi dapat memahami pemikiran dan emosi entitas lain, namun saat ini belum terealisasi adalah...", "options": ["Reactive Machine AI", "Limited Memory AI", "Theory of Mind AI", "Self Aware AI", "Artificial Narrow Intelligence (ANI)"], "jawaban": "Theory of Mind AI", "poin": 2.5},
        {"id": "pg8", "soal": "Menurut para ahli dalam dokumen, Artificial Superintelligence (ASI) diperkirakan akan tercapai pada tahun...", "options": ["2030", "2040", "2050", "2060", "2070"], "jawaban": "2060", "poin": 2.5},
        {"id": "pg9", "soal": "Berikut ini adalah perangkat lunak yang termasuk dalam kategori alat desain grafis berbasis AI, kecuali...", "options": ["Canva Magic Studio", "Looka", "Synthesia", "Adobe Express", "Design Evo"], "jawaban": "Synthesia", "poin": 2.5},
        {"id": "pg10", "soal": "Perangkat AI seperti Fathom dan Nyota digunakan untuk tujuan...", "options": ["Manajemen media sosial", "Pembuatan gambar dari teks", "Notulis dan asisten rapat", "Pengembangan aplikasi dan pemrograman", "Sintesis suara"], "jawaban": "Notulis dan asisten rapat", "poin": 2.5},
        {"id": "pg11", "soal": "Kemampuan AI untuk mempelajari pola dari data yang sangat banyak dan menjadi lebih baik seiring waktu disebut...", "options": ["Kemampuan Beradaptasi", "Pengenalan Pola", "Belajar dari Data", "Algoritma Prediktif", "Kecerdasan Statis"], "jawaban": "Belajar dari Data", "poin": 2.5},
        {"id": "pg12", "soal": "Apa komponen utama AI yang mencakup TensorFlow, PyTorch, dan Keras?", "options": ["Perangkat keras", "Perangkat lunak (algoritma)", "Infrastruktur data", "Sensor dan aktuator", "Framework dan library"], "jawaban": "Framework dan library", "poin": 2.5},
        {"id": "pg13", "soal": "Perangkat AI seperti Midjourney dan DALL-E 3 digunakan untuk...", "options": ["Membuat musik", "Menulis email", "Menciptakan gambar berdasarkan deskripsi teks", "Mengelola proyek", "Merekrut karyawan"], "jawaban": "Menciptakan gambar berdasarkan deskripsi teks", "poin": 2.5},
        {"id": "pg14", "soal": "Salah satu perbedaan mendasar antara kecerdasan artifisial dan kecerdasan manusia adalah...", "options": ["AI dapat belajar, sedangkan manusia tidak", "Manusia membuat keputusan berdasarkan data, sedangkan AI berdasarkan emosi", "AI tidak memiliki perasaan, sedangkan manusia memilikinya", "AI mampu beradaptasi, sedangkan manusia statis", "Manusia hanya memahami hal yang ada dalam datanya"], "jawaban": "AI tidak memiliki perasaan, sedangkan manusia memilikinya", "poin": 2.5},
        {"id": "pg15", "soal": "Tahap pertama dalam cara kerja kecerdasan artifisial adalah...", "options": ["Pelatihan Model", "Menghasilkan Output", "Pengumpulan Data", "Analisis Prediktif", "Adaptasi Sistem"], "jawaban": "Pengumpulan Data", "poin": 2.5},
        {"id": "pg16", "soal": "GitHub Copilot, Bubble, dan Cursor adalah contoh perangkat AI yang membantu dalam bidang...", "options": ["Desain Grafis", "Manajemen Proyek", "Layanan Pelanggan", "Pembuatan Aplikasi & Pemrograman", "Penelitian Akademik"], "jawaban": "Pembuatan Aplikasi & Pemrograman", "poin": 2.5},
        {"id": "pg17", "soal": "Karakteristik AI yang memungkinkannya memperbaiki diri dengan mengevaluasi hasil dari kesalahan yang pernah dibuatnya disebut...", "options": ["Belajar dari Data", "Kemampuan Beradaptasi", "Pengenalan Pola", "Logika Statis", "Memori Terbatas"], "jawaban": "Kemampuan Beradaptasi", "poin": 2.5},
        {"id": "pg18", "soal": "Manakah yang BUKAN merupakan komponen perangkat keras utama untuk AI?", "options": ["CPU (Central Processing Unit)", "GPU (Graphics Processing Unit)", "TPU (Tensor Processing Unit)", "Algoritma supervised learning", "Sensor dan aktuator"], "jawaban": "Algoritma supervised learning", "poin": 2.5},
        {"id": "pg19", "soal": "Menurut dokumen, perangkat AI seperti Textio dan CVViZ dapat membantu meningkatkan objektivitas dalam proses...", "options": ["Pemasaran", "Penjadwalan", "Layanan pelanggan", "Rekrutmen", "Manajemen pengetahuan"], "jawaban": "Rekrutmen", "poin": 2.5},
        {"id": "pg20", "soal": "Perangkat lunak AI yang membantu dalam menulis, mengelola, dan mengatur email dengan lebih efisien disebut...", "options": ["Manajemen Proyek", "Email Cerdas", "Notulis Rapat", "Sintesis Suara", "Pembuat Resume"], "jawaban": "Email Cerdas", "poin": 2.5}
    ],
    'menjodohkan': [
        {"id": "m1", "pernyataan": "ANI (Artificial Narrow Intelligence)", "jawaban": "D", "poin": 3},
        {"id": "m2", "pernyataan": "Self Aware AI", "jawaban": "A", "poin": 3},
        {"id": "m3", "pernyataan": "Limited Memory AI", "jawaban": "B", "poin": 3},
        {"id": "m4", "pernyataan": "ASI (Artificial Superintelligence)", "jawaban": "C", "poin": 3},
        {"id": "m5", "pernyataan": "Theory of Mind AI", "jawaban": "E", "poin": 3}
    ],
    'pilihan_majemuk': [
        {"id": "pm1", "soal": "Berdasarkan evolusi Kecerdasan Artifisial, manakah tahapan yang dijelaskan dalam dokumen?", "options": ["Era Simbolik", "Era Kuantum", "Pembelajaran Mesin (Machine Learning)", "Deep Learning", "Era Informasi"], "jawaban": ["Era Simbolik", "Pembelajaran Mesin (Machine Learning)", "Deep Learning"], "poin": 4},
        {"id": "pm2", "soal": "Manakah dari berikut ini yang merupakan contoh aplikasi atau perangkat AI dalam kategori Asisten KA (AI Assistants/Chatbots)?", "options": ["Siri", "Google Assistant", "Runway", "Alexa", "Filmora"], "jawaban": ["Siri", "Google Assistant", "Alexa"], "poin": 4},
        {"id": "pm3", "soal": "Menurut dokumen, apa saja karakteristik utama dari Kecerdasan Artifisial?", "options": ["Memiliki intuisi dan kreativitas murni", "Belajar dari Data", "Kemampuan Beradaptasi", "Pengenalan Pola", "Membuat keputusan dengan pertimbangan moral dan etika"], "jawaban": ["Belajar dari Data", "Kemampuan Beradaptasi", "Pengenalan Pola"], "poin": 4},
        {"id": "pm4", "soal": "Manakah dari perangkat berikut yang digunakan untuk bidang penulisan (writing) dan penelitian (research)?", "options": ["Rytr", "FeedHive", "Sudowrite", "Deep Research", "ClickUp"], "jawaban": ["Rytr", "Sudowrite", "Deep Research"], "poin": 4},
        {"id": "pm5", "soal": "Komponen utama apa saja yang diperlukan untuk membangun sistem Kecerdasan Artifisial?", "options": ["Perangkat keras (CPU, GPU)", "Perangkat lunak (algoritma pembelajaran)", "Kreativitas manusia", "Infrastruktur data (Big Data)", "Emosi dan perasaan"], "jawaban": ["Perangkat keras (CPU, GPU)", "Perangkat lunak (algoritma pembelajaran)", "Infrastruktur data (Big Data)"], "poin": 4}
    ],
    'benar_salah': [
        {"id": "bs1", "soal": "Artificial General Intelligence (AGI) adalah jenis AI yang kemampuannya sudah jauh melampaui kecerdasan manusia dalam segala bidang.", "jawaban": "Salah", "poin": 3},
        {"id": "bs2", "soal": "Sistem rekomendasi pada layanan streaming seperti Youtube dan Spotify adalah contoh dari Reactive Machine AI karena bekerja berdasarkan data riwayat pengguna.", "jawaban": "Benar", "poin": 3},
        {"id": "bs3", "soal": "Kecerdasan Artifisial dapat membuat keputusan dengan mempertimbangkan nilai moral dan etika, sama seperti manusia.", "jawaban": "Salah", "poin": 3},
        {"id": "bs4", "soal": "Pelatihan model adalah proses di mana AI menggunakan algoritma untuk mengenali pola dari data yang telah dikumpulkan.", "jawaban": "Benar", "poin": 3},
        {"id": "bs5", "soal": "Perangkat AI seperti Suno dan Udio dapat digunakan untuk menciptakan musik atau melodi secara otomatis.", "jawaban": "Benar", "poin": 3}
    ]
}

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    nama_siswa = request.form['nama_siswa']
    jawaban_siswa = {}
    skor = 0

    # Menilai Pilihan Ganda
    for q in questions['pilihan_ganda']:
        id_soal = q['id']
        jawaban_terpilih = request.form.get(id_soal)
        jawaban_siswa[id_soal] = jawaban_terpilih
        if jawaban_terpilih == q['jawaban']:
            skor += q['poin']

    # Menilai Menjodohkan
    for q in questions['menjodohkan']:
        id_soal = q['id']
        jawaban_terpilih = request.form.get(id_soal)
        jawaban_siswa[id_soal] = jawaban_terpilih
        if jawaban_terpilih == q['jawaban']:
            skor += q['poin']

    # Menilai Pilihan Majemuk
    for q in questions['pilihan_majemuk']:
        id_soal = q['id']
        jawaban_terpilih = request.form.getlist(id_soal)
        jawaban_siswa[id_soal] = jawaban_terpilih
        if sorted(jawaban_terpilih) == sorted(q['jawaban']):
            skor += q['poin']

    # Menilai Benar/Salah
    for q in questions['benar_salah']:
        id_soal = q['id']
        jawaban_terpilih = request.form.get(id_soal)
        jawaban_siswa[id_soal] = jawaban_terpilih
        if jawaban_terpilih == q['jawaban']:
            skor += q['poin']
            
    # Menyimpan hasil ke CSV
    output_file = 'hasil_ujian.csv'
    data_to_save = {
        'Nama Siswa': [nama_siswa],
        'Skor': [skor],
        'Jawaban': [str(jawaban_siswa)]
    }
    df = pd.DataFrame(data_to_save)

    if not os.path.isfile(output_file):
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(output_file, mode='a', header=False, index=False)

    return render_template('result.html', nama=nama_siswa, skor=round(skor, 2))

if __name__ == '__main__':
    app.run(debug=True)