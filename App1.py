import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Sistem Antrian Bank", layout="wide", page_icon="🏦")

# ─────────────────────────────────────────────
# STRUKTUR DATA QUEUE (berbasis Linked List)
# ─────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None  # kepala antrian
        self.rear = None   # ekor antrian
        self.size = 0

    def enqueue(self, data):
        """Tambah nasabah ke belakang antrian"""
        node_baru = Node(data)
        if self.rear is None:
            self.front = self.rear = node_baru
        else:
            self.rear.next = node_baru
            self.rear = node_baru
        self.size += 1

    def dequeue(self):
        """Panggil nasabah dari depan antrian"""
        if self.front is None:
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return data

    def peek(self):
        """Lihat nasabah paling depan tanpa menghapus"""
        if self.front:
            return self.front.data
        return None

    def is_empty(self):
        return self.size == 0

    def tampilkan(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "antrian" not in st.session_state:
    st.session_state.antrian = Queue()

if "nomor_urut" not in st.session_state:
    st.session_state.nomor_urut = 1

if "sedang_dilayani" not in st.session_state:
    st.session_state.sedang_dilayani = None

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "notif" not in st.session_state:
    st.session_state.notif = None


# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
    .block-container { padding: 2rem 3rem; }

    .header-bank {
        background: linear-gradient(135deg, #1a3a6b, #2563eb);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    .header-bank h1 { margin: 0; font-size: 1.8rem; }
    .header-bank p  { margin: 0.2rem 0 0; opacity: 0.8; font-size: 0.95rem; }

    .kartu {
        background: #f8faff;
        border: 1px solid #dbeafe;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }
    .kartu-judul {
        font-size: 1.05rem; font-weight: 700;
        color: #1e3a8a; margin-bottom: 1rem;
    }

    /* Tiket antrian */
    .tiket {
        background: white;
        border: 2px solid #bfdbfe;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .tiket-nomor {
        background: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.3rem 0.7rem;
        font-weight: 800;
        font-size: 1rem;
        min-width: 52px;
        text-align: center;
    }
    .tiket-pertama .tiket-nomor { background: #16a34a; }
    .tiket-info { flex: 1; }
    .tiket-nama { font-weight: 600; color: #1e293b; font-size: 0.95rem; }
    .tiket-meta { color: #64748b; font-size: 0.78rem; }

    /* Layanan aktif */
    .layanan-aktif {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 2px solid #16a34a;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .layanan-nomor {
        font-size: 3rem; font-weight: 900;
        color: #15803d; line-height: 1;
    }
    .layanan-nama {
        font-size: 1.1rem; font-weight: 600;
        color: #166534; margin-top: 0.3rem;
    }
    .layanan-label {
        font-size: 0.8rem; color: #4ade80;
        text-transform: uppercase; letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }

    /* Kosong */
    .antrian-kosong {
        text-align: center; padding: 2rem;
        color: #94a3b8; font-size: 0.9rem;
    }

    /* Riwayat */
    .item-riwayat {
        display: flex; align-items: center; gap: 0.6rem;
        padding: 0.4rem 0.8rem;
        background: #f1f5f9;
        border-radius: 8px;
        margin-bottom: 0.3rem;
        font-size: 0.85rem; color: #475569;
    }

    /* Stats */
    .stat-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stat-angka { font-size: 2rem; font-weight: 800; color: #2563eb; }
    .stat-label { font-size: 0.8rem; color: #64748b; margin-top: 0.2rem; }

    .notif-sukses {
        background: #f0fdf4; border: 1px solid #86efac;
        color: #166534; border-radius: 8px;
        padding: 0.5rem 1rem; font-size: 0.85rem;
        margin-bottom: 0.8rem;
    }
    .notif-info {
        background: #eff6ff; border: 1px solid #93c5fd;
        color: #1d4ed8; border-radius: 8px;
        padding: 0.5rem 1rem; font-size: 0.85rem;
        margin-bottom: 0.8rem;
    }
    .notif-gagal {
        background: #fef2f2; border: 1px solid #fca5a5;
        color: #b91c1c; border-radius: 8px;
        padding: 0.5rem 1rem; font-size: 0.85rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class="header-bank">
    <h1>🏦 Sistem Antrian Bank</h1>
    <p>Simulasi antrian nasabah menggunakan struktur data Queue (FIFO)</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATISTIK
# ─────────────────────────────────────────────

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-angka">{st.session_state.antrian.size}</div>
        <div class="stat-label">Menunggu</div>
    </div>""", unsafe_allow_html=True)
with col_s2:
    dilayani = "Ada" if st.session_state.sedang_dilayani else "Kosong"
    warna = "#16a34a" if st.session_state.sedang_dilayani else "#94a3b8"
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-angka" style="color:{warna}">{dilayani}</div>
        <div class="stat-label">Loket Saat Ini</div>
    </div>""", unsafe_allow_html=True)
with col_s3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-angka">{len(st.session_state.riwayat)}</div>
        <div class="stat-label">Selesai Dilayani</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LAYOUT UTAMA
# ─────────────────────────────────────────────

col_kiri, col_tengah, col_kanan = st.columns([1, 1.2, 1])


# ── Kolom Kiri: Form daftar ──
with col_kiri:
    st.markdown('<div class="kartu">', unsafe_allow_html=True)
    st.markdown('<div class="kartu-judul">📝 Daftar Antrian</div>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:0.75rem;color:#64748b;background:#eff6ff;padding:2px 8px;border-radius:4px;font-weight:600">Operasi: Enqueue</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    nama = st.text_input("Nama Nasabah", placeholder="Masukkan nama...", key="input_nama")
    keperluan = st.selectbox("Keperluan", [
        "💰 Setor Tunai",
        "🏧 Tarik Tunai",
        "💳 Buka Rekening",
        "📋 Administrasi",
        "💸 Transfer",
        "❓ Informasi"
    ], key="input_keperluan")

    if st.button("🎫 Ambil Nomor Antrian", use_container_width=True, type="primary"):
        if nama.strip():
            nomor = f"A{st.session_state.nomor_urut:03d}"
            waktu = datetime.now().strftime("%H:%M")
            data_nasabah = {
                "nomor": nomor,
                "nama": nama.strip(),
                "keperluan": keperluan,
                "waktu": waktu
            }
            st.session_state.antrian.enqueue(data_nasabah)
            st.session_state.nomor_urut += 1
            st.session_state.notif = ("sukses", f"Nomor antrian {nomor} berhasil diambil!")
            st.rerun()
        else:
            st.session_state.notif = ("gagal", "Nama nasabah tidak boleh kosong.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Tombol panggil
    st.markdown('<div class="kartu">', unsafe_allow_html=True)
    st.markdown('<div class="kartu-judul">🔔 Panggil Nasabah</div>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:0.75rem;color:#64748b;background:#eff6ff;padding:2px 8px;border-radius:4px;font-weight:600">Operasi: Dequeue</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.antrian.is_empty():
        berikutnya = st.session_state.antrian.peek()
        st.markdown(f"<small style='color:#64748b'>Berikutnya: <b>{berikutnya['nomor']} - {berikutnya['nama']}</b></small>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📢 Panggil Nasabah Berikutnya", use_container_width=True,
                 disabled=st.session_state.antrian.is_empty()):
        nasabah = st.session_state.antrian.dequeue()
        if nasabah:
            if st.session_state.sedang_dilayani:
                st.session_state.riwayat.append(st.session_state.sedang_dilayani)
            st.session_state.sedang_dilayani = nasabah
            st.session_state.notif = ("info", f"Memanggil {nasabah['nomor']} - {nasabah['nama']}")
            st.rerun()

    if st.session_state.sedang_dilayani:
        if st.button("✅ Selesai Dilayani", use_container_width=True):
            st.session_state.riwayat.append(st.session_state.sedang_dilayani)
            st.session_state.sedang_dilayani = None
            st.session_state.notif = ("sukses", "Nasabah selesai dilayani.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ── Kolom Tengah: Antrian & Loket ──
with col_tengah:

    # Notifikasi
    notif = st.session_state.notif
    if notif:
        tipe, pesan = notif
        kelas = {"sukses": "notif-sukses", "info": "notif-info", "gagal": "notif-gagal"}[tipe]
        ikon = {"sukses": "✅", "info": "🔔", "gagal": "❌"}[tipe]
        st.markdown(f'<div class="{kelas}">{ikon} {pesan}</div>', unsafe_allow_html=True)
        st.session_state.notif = None

    # Loket aktif
    st.markdown('<div class="kartu-judul">🏪 Loket Pelayanan</div>', unsafe_allow_html=True)
    if st.session_state.sedang_dilayani:
        n = st.session_state.sedang_dilayani
        st.markdown(f"""
        <div class="layanan-aktif">
            <div class="layanan-label">🟢 Sedang Dilayani</div>
            <div class="layanan-nomor">{n['nomor']}</div>
            <div class="layanan-nama">{n['nama']}</div>
            <div style="color:#4ade80;font-size:0.85rem;margin-top:0.3rem">{n['keperluan']}</div>
            <div style="color:#86efac;font-size:0.78rem;margin-top:0.2rem">⏰ Tiba: {n['waktu']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="layanan-aktif" style="background:#f8fafc;border-color:#e2e8f0">
            <div style="font-size:2.5rem">🪑</div>
            <div style="color:#94a3b8;font-size:0.9rem;margin-top:0.3rem">Loket kosong</div>
        </div>
        """, unsafe_allow_html=True)

    # Daftar antrian
    st.markdown('<div class="kartu-judul" style="margin-top:0.5rem">👥 Daftar Antrian</div>', unsafe_allow_html=True)
    daftar = st.session_state.antrian.tampilkan()
    if daftar:
        for i, nasabah in enumerate(daftar):
            kelas_tiket = "tiket tiket-pertama" if i == 0 else "tiket"
            label = " 🔜 Berikutnya" if i == 0 else ""
            st.markdown(f"""
            <div class="{kelas_tiket}">
                <div class="tiket-nomor">{nasabah['nomor']}</div>
                <div class="tiket-info">
                    <div class="tiket-nama">{nasabah['nama']}{label}</div>
                    <div class="tiket-meta">{nasabah['keperluan']} · {nasabah['waktu']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Visualisasi pointer Queue
        st.markdown(f"""
        <div style="display:flex;gap:0.5rem;margin-top:0.8rem;font-size:0.78rem;color:#94a3b8">
            <span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:4px;font-weight:600">FRONT → {daftar[0]['nomor']}</span>
            <span>·····</span>
            <span style="background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:4px;font-weight:600">REAR → {daftar[-1]['nomor']}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="antrian-kosong">🎉 Tidak ada nasabah yang menunggu</div>', unsafe_allow_html=True)


# ── Kolom Kanan: Riwayat ──
with col_kanan:
    st.markdown('<div class="kartu">', unsafe_allow_html=True)
    st.markdown('<div class="kartu-judul">📋 Riwayat Pelayanan</div>', unsafe_allow_html=True)

    if st.session_state.riwayat:
        for item in reversed(st.session_state.riwayat):
            st.markdown(f"""
            <div class="item-riwayat">
                <span style="background:#16a34a;color:white;border-radius:4px;padding:1px 6px;font-size:0.75rem;font-weight:700">{item['nomor']}</span>
                <span><b>{item['nama']}</b> · {item['keperluan'].split()[-1]}</span>
            </div>
            """, unsafe_allow_html=True)
        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state.riwayat = []
            st.rerun()
    else:
        st.markdown("<p style='color:#94a3b8;font-size:0.85rem;text-align:center;padding:1rem'>Belum ada nasabah yang selesai dilayani.</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Penjelasan Queue
    st.markdown('<div class="kartu">', unsafe_allow_html=True)
    st.markdown('<div class="kartu-judul">📖 Konsep Queue</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.82rem;color:#475569;line-height:1.7">
        <b>FIFO</b> — First In, First Out<br>
        Nasabah yang datang pertama dilayani pertama.<br><br>
        <b>Enqueue</b> → Tambah ke <code>REAR</code><br>
        <b>Dequeue</b> → Ambil dari <code>FRONT</code><br>
        <b>Peek</b> → Lihat <code>FRONT</code> tanpa hapus<br><br>
        <code>FRONT → [A001] → [A002] → [A003] → REAR</code>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)