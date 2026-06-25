import streamlit as st
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Antrian Rumah Sakit",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Simulasi Antrian Rumah Sakit")

# Inisialisasi session state
if "antrian" not in st.session_state:
    st.session_state.antrian = []

if "nomor_terakhir" not in st.session_state:
    st.session_state.nomor_terakhir = 0

if "sedang_dilayani" not in st.session_state:
    st.session_state.sedang_dilayani = None

# Layout
col1, col2 = st.columns(2)

# ======================
# Tambah Pasien
# ======================
with col1:
    st.subheader("➕ Pendaftaran Pasien")

    nama = st.text_input("Nama Pasien")

    poli = st.selectbox(
        "Pilih Poli",
        [
            "Poli Umum",
            "Poli Gigi",
            "Poli Anak",
            "Poli Mata",
            "Poli Jantung"
        ]
    )

    if st.button("Ambil Nomor Antrian"):
        if nama:
            st.session_state.nomor_terakhir += 1

            pasien = {
                "nomor": st.session_state.nomor_terakhir,
                "nama": nama,
                "poli": poli,
                "waktu": datetime.now().strftime("%H:%M:%S")
            }

            st.session_state.antrian.append(pasien)

            st.success(
                f"Nomor Antrian Anda: A-{pasien['nomor']:03d}"
            )
        else:
            st.warning("Masukkan nama pasien terlebih dahulu.")

# ======================
# Loket/Panggilan
# ======================
with col2:
    st.subheader("🩺 Loket Pelayanan")

    if st.button("Panggil Pasien Berikutnya"):
        if st.session_state.antrian:
            st.session_state.sedang_dilayani = (
                st.session_state.antrian.pop(0)
            )
        else:
            st.warning("Tidak ada pasien dalam antrian.")

    if st.session_state.sedang_dilayani:
        pasien = st.session_state.sedang_dilayani

        st.info(
            f"""
            Sedang Dilayani

            Nomor : A-{pasien['nomor']:03d}

            Nama : {pasien['nama']}

            Poli : {pasien['poli']}
            """
        )

# ======================
# Statistik
# ======================
st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Menunggu",
        len(st.session_state.antrian)
    )

with c2:
    st.metric(
        "Nomor Terakhir",
        st.session_state.nomor_terakhir
    )

with c3:
    if st.session_state.sedang_dilayani:
        st.metric(
            "Sedang Dilayani",
            f"A-{st.session_state.sedang_dilayani['nomor']:03d}"
        )
    else:
        st.metric(
            "Sedang Dilayani",
            "-"
        )

# ======================
# Daftar Antrian
# ======================
st.subheader("📋 Daftar Antrian Menunggu")

if st.session_state.antrian:
    data = []

    for p in st.session_state.antrian:
        data.append({
            "Nomor": f"A-{p['nomor']:03d}",
            "Nama": p["nama"],
            "Poli": p["poli"],
            "Jam Daftar": p["waktu"]
        })

    st.dataframe(
        data,
        use_container_width=True
    )
else:
    st.info("Belum ada pasien yang menunggu.")

import streamlit as st
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Printer Queue",
    page_icon="🖨️",
    layout="wide"
)


#___________________________________________
# SIMULASI PRINTER
#___________________________________________

st.title("🖨️ Simulasi Printer Queue (FIFO)")

# Session State
if "queue" not in st.session_state:
    st.session_state.queue = []

if "job_id" not in st.session_state:
    st.session_state.job_id = 0

if "printed" not in st.session_state:
    st.session_state.printed = []

if "current_job" not in st.session_state:
    st.session_state.current_job = None


# ==========================
# Input Dokumen
# ==========================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Tambah Dokumen")

    nama_file = st.text_input("Nama Dokumen")

    jumlah_halaman = st.number_input(
        "Jumlah Halaman",
        min_value=1,
        value=1
    )

    if st.button("Tambah ke Queue"):
        if nama_file:
            st.session_state.job_id += 1

            job = {
                "id": st.session_state.job_id,
                "nama": nama_file,
                "halaman": jumlah_halaman,
                "waktu": datetime.now().strftime("%H:%M:%S")
            }

            st.session_state.queue.append(job)

            st.success(
                f"Dokumen '{nama_file}' berhasil masuk antrian."
            )
        else:
            st.warning("Masukkan nama dokumen terlebih dahulu.")


# ==========================
# Statistik
# ==========================
with col2:
    st.subheader("Statistik")

    st.metric(
        "Menunggu Cetak",
        len(st.session_state.queue)
    )

    st.metric(
        "Sudah Dicetak",
        len(st.session_state.printed)
    )


st.divider()

# ==========================
# Tombol Print
# ==========================
st.subheader("Kontrol Printer")

if st.button("🖨️ Cetak Dokumen Berikutnya"):
    if st.session_state.queue:

        st.session_state.current_job = (
            st.session_state.queue.pop(0)
        )

        st.session_state.printed.append(
            st.session_state.current_job
        )

    else:
        st.warning("Queue kosong.")


# ==========================
# Sedang Dicetak
# ==========================
if st.session_state.current_job:

    job = st.session_state.current_job

    st.info(
        f"""
        Sedang Dicetak

        ID Job : {job['id']}
        
        Dokumen : {job['nama']}
        
        Halaman : {job['halaman']}
        """
    )

st.divider()

# ==========================
# Queue Saat Ini
# ==========================
st.subheader("📋 Antrian Printer")

if st.session_state.queue:

    data_queue = []

    for job in st.session_state.queue:
        data_queue.append({
            "ID": job["id"],
            "Dokumen": job["nama"],
            "Halaman": job["halaman"],
            "Waktu Masuk": job["waktu"]
        })

    st.dataframe(
        data_queue,
        use_container_width=True
    )

else:
    st.info("Tidak ada dokumen dalam antrian.")


# ==========================
# Riwayat Cetak
# ==========================
st.subheader("📄 Riwayat Cetak")

if st.session_state.printed:

    history = []

    for job in st.session_state.printed:
        history.append({
            "ID": job["id"],
            "Dokumen": job["nama"],
            "Halaman": job["halaman"]
        })

    st.dataframe(
        history,
        use_container_width=True
    )

else:
    st.info("Belum ada dokumen yang dicetak.")


#==================================
# CALL CENTER KOPERASI
#==================================

import streamlit as st
from datetime import datetime

# ==========================
# Konfigurasi Halaman
# ==========================
st.set_page_config(
    page_title="Call Center Koperasi",
    page_icon="☎️",
    layout="wide"
)

st.title("☎️ Simulasi Call Center Koperasi")
st.write("Simulasi antrian panggilan anggota koperasi menggunakan metode FIFO.")

# ==========================
# Session State
# ==========================
if "antrian" not in st.session_state:
    st.session_state.antrian = []

if "ticket" not in st.session_state:
    st.session_state.ticket = 1000

if "sedang_dilayani" not in st.session_state:
    st.session_state.sedang_dilayani = None

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ==========================
# Layout
# ==========================
col1, col2 = st.columns(2)

# ==========================
# Input Panggilan
# ==========================
with col1:
    st.subheader("📞 Panggilan Masuk")

    nama = st.text_input("Nama Anggota")

    kategori = st.selectbox(
        "Jenis Layanan",
        [
            "Informasi Simpanan",
            "Informasi Pinjaman",
            "Keluhan Layanan",
            "Pembayaran Angsuran",
            "Lainnya"
        ]
    )

    if st.button("Masukkan ke Antrian"):
        if nama:
            st.session_state.ticket += 1

            data = {
                "ticket": st.session_state.ticket,
                "nama": nama,
                "kategori": kategori,
                "jam": datetime.now().strftime("%H:%M:%S")
            }

            st.session_state.antrian.append(data)

            st.success(
                f"Tiket #{data['ticket']} berhasil masuk antrian."
            )
        else:
            st.warning("Masukkan nama anggota.")

# ==========================
# Petugas Call Center
# ==========================
with col2:
    st.subheader("👨‍💼 Petugas Call Center")

    if st.button("Layani Panggilan Berikutnya"):
        if st.session_state.antrian:
            panggilan = st.session_state.antrian.pop(0)

            st.session_state.sedang_dilayani = panggilan
            st.session_state.riwayat.append(panggilan)

        else:
            st.warning("Tidak ada panggilan dalam antrian.")

    if st.session_state.sedang_dilayani:
        data = st.session_state.sedang_dilayani

        st.info(
            f"""
Tiket : #{data['ticket']}

Nama : {data['nama']}

Layanan : {data['kategori']}
"""
        )

# ==========================
# Statistik
# ==========================
st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Menunggu",
    len(st.session_state.antrian)
)

c2.metric(
    "Sudah Dilayani",
    len(st.session_state.riwayat)
)

c3.metric(
    "Nomor Tiket Terakhir",
    st.session_state.ticket
)

# ==========================
# Daftar Antrian
# ==========================
st.subheader("📋 Antrian Panggilan")

if st.session_state.antrian:

    tabel = []

    for item in st.session_state.antrian:
        tabel.append({
            "Tiket": item["ticket"],
            "Nama": item["nama"],
            "Kategori": item["kategori"],
            "Jam Masuk": item["jam"]
        })

    st.dataframe(tabel, use_container_width=True)

else:
    st.info("Tidak ada antrian saat ini.")

# ==========================
# Riwayat
# ==========================
st.subheader("📑 Riwayat Layanan")

if st.session_state.riwayat:

    history = []

    for item in st.session_state.riwayat:
        history.append({
            "Tiket": item["ticket"],
            "Nama": item["nama"],
            "Kategori": item["kategori"]
        })

    st.dataframe(history, use_container_width=True)

else:
    st.info("Belum ada panggilan yang dilayani.")